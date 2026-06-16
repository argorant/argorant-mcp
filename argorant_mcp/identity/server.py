"""Product-agnostic OAuth 2.1 Authorization Server (+ resource-server token validation).

Implements the subset the MCP spec requires: RFC 9728 + RFC 8414 discovery, RFC 7591 DCR,
authorization-code + PKCE(S256), RFC 8707 resource/audience binding, RFC 9207 iss,
refresh-token rotation, RFC 7009 revocation. User authentication + consent are delegated
to the product via the IdentityBridge; this server issues its OWN opaque tokens and holds
the {token → connection → product credential} mapping.
"""
from __future__ import annotations

import base64
import hashlib
import json
import secrets
import time
from typing import Any, Dict, List, Optional

from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse, Response
from starlette.routing import Route

from ..config import settings
from ..db import session
from . import bridge as bridge_mod
from . import replay_store
from .metadata import authorization_server_metadata, protected_resource_metadata
from .models import AccessToken, AuthCode, Connection, OAuthClient, RefreshToken


# ─────────────────────────── wiring (set by app.py at startup) ───────────────────────────
_bridge: Optional[bridge_mod.IdentityBridge] = None
_scopes: List[str] = []
_connection_ref = None  # callable(client_id, subject) -> str


def configure(*, bridge: bridge_mod.IdentityBridge, scopes: List[str], connection_ref) -> None:
    global _bridge, _scopes, _connection_ref
    _bridge, _scopes, _connection_ref = bridge, scopes, connection_ref


# ─────────────────────────── small helpers ───────────────────────────
def _now() -> int:
    return int(time.time())


def _rand(n: int = 32) -> str:
    return secrets.token_urlsafe(n)


def _as_sign(payload: Dict[str, Any]) -> str:
    """Sign our internal /authorize state (HMAC, operator-held secret)."""
    return bridge_mod.sign(settings.bridge_secret, payload)


def _as_verify(token: str, max_age: int) -> Optional[Dict[str, Any]]:
    return bridge_mod.verify(settings.bridge_secret, token, max_age=max_age)


def _pkce_ok(verifier: str, challenge: str) -> bool:
    if not verifier or not challenge:
        return False
    digest = hashlib.sha256(verifier.encode()).digest()
    calc = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return secrets.compare_digest(calc, challenge)


def _oauth_error(error: str, desc: str, status: int = 400) -> JSONResponse:
    return JSONResponse({"error": error, "error_description": desc}, status_code=status)


def _redirect_error(redirect_uri: str, error: str, state: str, desc: str = "") -> RedirectResponse:
    sep = "&" if "?" in redirect_uri else "?"
    q = f"error={error}&iss={_q(settings.issuer)}"
    if state:
        q += f"&state={_q(state)}"
    if desc:
        q += f"&error_description={_q(desc)}"
    return RedirectResponse(url=f"{redirect_uri}{sep}{q}", status_code=302)


def _q(value: str) -> str:
    from urllib.parse import quote
    return quote(value or "", safe="")


def _scope_string(raw: Optional[str]) -> str:
    """Return a validated public scope string.

    The backend has internal scopes such as argorant:admin. The public OAuth
    server must never mint unadvertised scopes just because a client requested
    them.
    """
    requested = [s for s in str(raw or "").split() if s]
    if not requested:
        requested = list(_scopes)
    allowed = set(_scopes)
    unknown = sorted(set(requested) - allowed)
    if unknown:
        raise ValueError(" ".join(unknown))
    # Preserve the configured order for stable consent/token displays.
    requested_set = set(requested)
    return " ".join(scope for scope in _scopes if scope in requested_set)


# ─────────────────────────── discovery ───────────────────────────
async def well_known_prm(request: Request) -> JSONResponse:
    return JSONResponse(protected_resource_metadata(
        resource=settings.canonical_resource, issuer=settings.issuer, scopes=_scopes))


async def well_known_asm(request: Request) -> JSONResponse:
    return JSONResponse(authorization_server_metadata(issuer=settings.issuer, scopes=_scopes))


# ─────────────────────────── RFC 7591 Dynamic Client Registration ───────────────────────────
async def register(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return _oauth_error("invalid_client_metadata", "Body must be JSON")
    redirect_uris = body.get("redirect_uris")
    if not isinstance(redirect_uris, list) or not redirect_uris:
        return _oauth_error("invalid_redirect_uri", "redirect_uris is required")
    for uri in redirect_uris:
        if not (uri.startswith("https://") or uri.startswith("http://localhost") or uri.startswith("http://127.0.0.1")):
            return _oauth_error("invalid_redirect_uri", f"redirect_uri must be https or loopback: {uri}")

    auth_method = body.get("token_endpoint_auth_method", "none")
    client_id = "mcp-" + _rand(16)
    client_secret = None if auth_method == "none" else _rand(32)
    s = session()
    try:
        s.add(OAuthClient(
            client_id=client_id,
            client_secret=client_secret,
            client_name=str(body.get("client_name") or "MCP Client")[:200],
            redirect_uris=json.dumps(redirect_uris),
            grant_types=json.dumps(body.get("grant_types") or ["authorization_code", "refresh_token"]),
            token_endpoint_auth_method=auth_method,
            created_at=_now(),
        ))
        s.commit()
    finally:
        s.close()

    out = {
        "client_id": client_id,
        "client_id_issued_at": _now(),
        "redirect_uris": redirect_uris,
        "grant_types": body.get("grant_types") or ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": auth_method,
        "client_name": body.get("client_name"),
    }
    if client_secret:
        out["client_secret"] = client_secret
    return JSONResponse(out, status_code=201)


def _load_client(client_id: str) -> Optional[OAuthClient]:
    s = session()
    try:
        return s.query(OAuthClient).filter(OAuthClient.client_id == client_id).first()
    finally:
        s.close()


# ─────────────────────────── /authorize ───────────────────────────
async def authorize(request: Request) -> Response:
    p = request.query_params
    if p.get("response_type") != "code":
        return _oauth_error("unsupported_response_type", "Only response_type=code is supported")
    client_id = p.get("client_id", "")
    redirect_uri = p.get("redirect_uri", "")
    client = _load_client(client_id)
    if not client:
        return _oauth_error("invalid_client", "Unknown client_id")
    if redirect_uri not in json.loads(client.redirect_uris):
        return _oauth_error("invalid_request", "redirect_uri not registered for this client")

    code_challenge = p.get("code_challenge", "")
    if not code_challenge or p.get("code_challenge_method", "S256") != "S256":
        # Don't redirect for PKCE errors; surface directly.
        return _oauth_error("invalid_request", "PKCE required: code_challenge with method S256")

    try:
        scope = _scope_string(p.get("scope"))
    except ValueError as exc:
        return _oauth_error("invalid_scope", f"Unsupported scope(s): {exc}")
    resource = p.get("resource", settings.canonical_resource)
    client_state = p.get("state", "")
    rid = _rand(12)

    # Sign all the context we need back at the callback into our internal state.
    internal_state = _as_sign({
        "typ": "as_state",
        "rid": rid,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "cc": code_challenge,
        "ccm": "S256",
        "scope": scope,
        "resource": resource,
        "cstate": client_state,
        "iat": _now(),
    })

    consent_url = _bridge.build_consent_url(
        rid=rid,
        client_name=client.client_name or "An application",
        scope=scope,
        callback=f"{settings.issuer}/authorize/callback",
        issuer=settings.issuer,
        state=internal_state,
        request_ttl=settings.request_ctx_ttl_s,
    )
    return RedirectResponse(url=consent_url, status_code=302)


async def authorize_callback(request: Request) -> Response:
    p = request.query_params
    internal_state = p.get("state", "")
    ctx = _as_verify(internal_state, max_age=settings.request_ctx_ttl_s)
    if not ctx or ctx.get("typ") != "as_state":
        return _oauth_error("invalid_request", "Invalid or expired authorization state")

    redirect_uri = ctx["redirect_uri"]
    client_state = ctx.get("cstate", "")

    if p.get("error"):
        return _redirect_error(redirect_uri, p.get("error", "access_denied"), client_state)

    grant = p.get("grant", "")
    if not grant:
        return _redirect_error(redirect_uri, "access_denied", client_state, "No grant returned")

    # Mint an authorization code carrying the grant forward to /token (validated there).
    code = _rand(24)
    s = session()
    try:
        try:
            scope = _scope_string(ctx.get("scope"))
        except ValueError as exc:
            return _redirect_error(redirect_uri, "invalid_scope", client_state, f"Unsupported scope(s): {exc}")

        s.add(AuthCode(
            code=code,
            client_id=ctx["client_id"],
            redirect_uri=redirect_uri,
            code_challenge=ctx["cc"],
            code_challenge_method=ctx["ccm"],
            scope=scope,
            resource=ctx.get("resource"),
            rid=ctx["rid"],
            grant=grant,
            created_at=_now(),
            used=False,
        ))
        s.commit()
    finally:
        s.close()

    sep = "&" if "?" in redirect_uri else "?"
    q = f"code={_q(code)}&iss={_q(settings.issuer)}"
    if client_state:
        q += f"&state={_q(client_state)}"
    return RedirectResponse(url=f"{redirect_uri}{sep}{q}", status_code=302)


# ─────────────────────────── /token ───────────────────────────
async def token(request: Request) -> JSONResponse:
    form = await request.form()
    grant_type = form.get("grant_type")
    if grant_type == "refresh_token":
        return _token_refresh(form)
    if grant_type == "authorization_code":
        return _token_auth_code(form)
    return _oauth_error("unsupported_grant_type", f"grant_type={grant_type!r} not supported")


def _authenticate_client(form, client: OAuthClient) -> bool:
    if client.token_endpoint_auth_method == "none":
        return True
    return bool(client.client_secret) and secrets.compare_digest(
        str(form.get("client_secret", "")), client.client_secret)


def _token_auth_code(form) -> JSONResponse:
    """THE composed validation path: single code use → PKCE → audience → grant HMAC+120s
    freshness → rid match → jti single-use consume → provision → issue tokens."""
    code_val = form.get("code", "")
    client_id = form.get("client_id", "")
    redirect_uri = form.get("redirect_uri", "")
    code_verifier = form.get("code_verifier", "")

    client = _load_client(client_id)
    if not client:
        return _oauth_error("invalid_client", "Unknown client_id", status=401)
    if not _authenticate_client(form, client):
        return _oauth_error("invalid_client", "Client authentication failed", status=401)

    s = session()
    try:
        # (1) Authorization code: must exist, belong to this client, be unused, unexpired.
        ac = s.query(AuthCode).filter(AuthCode.code == code_val).first()
        if not ac or ac.used:
            return _oauth_error("invalid_grant", "Authorization code invalid or already used")
        if ac.client_id != client_id or ac.redirect_uri != redirect_uri:
            return _oauth_error("invalid_grant", "client_id / redirect_uri mismatch")
        if _now() - ac.created_at > settings.auth_code_ttl_s:
            return _oauth_error("invalid_grant", "Authorization code expired")
        ac.used = True                      # single-use: burn it now, inside this txn
        s.commit()

        # (2) PKCE S256.
        if not _pkce_ok(code_verifier, ac.code_challenge):
            return _oauth_error("invalid_grant", "PKCE verification failed")

        # (3) RFC 8707 audience: requested resource must match ours (or default to ours).
        requested_resource = form.get("resource") or ac.resource or settings.canonical_resource
        if requested_resource.rstrip("/") != settings.canonical_resource.rstrip("/"):
            return _oauth_error("invalid_target", "resource does not match this MCP server")

        # (4) Bridge grant: HMAC signature + 120s freshness.
        grant = _bridge.verify_grant(ac.grant, max_age=settings.grant_ttl_s)
        if not grant:
            return _oauth_error("invalid_grant", "Bridge grant invalid or expired (120s)")

        # (5) rid match: grant must belong to THIS authorize flow.
        if grant.get("rid") != ac.rid:
            return _oauth_error("invalid_grant", "Grant does not match authorization request")

        # (6) jti single-use consume (replay defense). Atomic; False == already used.
        if not replay_store.consume(grant.get("jti", "")):
            return _oauth_error("invalid_grant", "Grant already redeemed")

        subject = str(grant.get("sub"))
        conn_ref = _connection_ref(client_id, subject)

        # (7) Server-to-server: exchange the grant for the user's per-connection credential.
        try:
            provisioned = _bridge.provision_credential(grant=ac.grant, connection_ref=conn_ref)
        except Exception as exc:  # noqa: BLE001 - surface as OAuth error, don't leak internals
            return _oauth_error("server_error", f"Could not provision credential: {exc}", status=502)

        # (8) Upsert the connection (mapping the agent never sees).
        conn = s.query(Connection).filter(Connection.id == conn_ref).first()
        if conn:
            conn.product_credential = provisioned["api_key"]
            conn.product_credential_id = str(provisioned.get("api_key_id") or "")
            conn.email = provisioned.get("email")
            conn.revoked = False
        else:
            conn = Connection(
                id=conn_ref, client_id=client_id, subject=subject,
                email=provisioned.get("email"),
                product_credential=provisioned["api_key"],
                product_credential_id=str(provisioned.get("api_key_id") or ""),
                created_at=_now(), revoked=False,
            )
            s.add(conn)

        # (9) Issue our own opaque access + refresh tokens, audience-bound to this server.
        access = _rand(32)
        refresh = _rand(32)
        try:
            scope = _scope_string(ac.scope)
        except ValueError as exc:
            return _oauth_error("invalid_scope", f"Unsupported scope(s): {exc}")

        s.add(AccessToken(token=access, connection_id=conn_ref, client_id=client_id, subject=subject,
                          scope=scope, audience=settings.canonical_resource, issued_at=_now(),
                          expires_at=_now() + settings.access_token_ttl_s, revoked=False))
        s.add(RefreshToken(token=refresh, connection_id=conn_ref, client_id=client_id, subject=subject,
                           scope=scope, audience=settings.canonical_resource, issued_at=_now(),
                           expires_at=_now() + settings.refresh_token_ttl_s, revoked=False))
        s.commit()

        return JSONResponse({
            "access_token": access,
            "token_type": "Bearer",
            "expires_in": settings.access_token_ttl_s,
            "refresh_token": refresh,
            "scope": scope,
        })
    finally:
        s.close()


def _token_refresh(form) -> JSONResponse:
    refresh_val = form.get("refresh_token", "")
    client_id = form.get("client_id", "")
    client = _load_client(client_id)
    if not client or not _authenticate_client(form, client):
        return _oauth_error("invalid_client", "Client authentication failed", status=401)

    s = session()
    try:
        rt = s.query(RefreshToken).filter(RefreshToken.token == refresh_val).first()
        if not rt or rt.revoked or rt.client_id != client_id or _now() > rt.expires_at:
            return _oauth_error("invalid_grant", "Refresh token invalid or expired")
        conn = s.query(Connection).filter(Connection.id == rt.connection_id).first()
        if not conn or conn.revoked:
            return _oauth_error("invalid_grant", "Connection revoked")

        try:
            scope = _scope_string(rt.scope)
        except ValueError as exc:
            return _oauth_error("invalid_scope", f"Unsupported scope(s): {exc}")

        rt.revoked = True  # OAuth 2.1: rotate refresh tokens for public clients
        new_access = _rand(32)
        new_refresh = _rand(32)
        s.add(AccessToken(token=new_access, connection_id=rt.connection_id, client_id=client_id,
                          subject=rt.subject, scope=scope, audience=settings.canonical_resource,
                          issued_at=_now(), expires_at=_now() + settings.access_token_ttl_s, revoked=False))
        s.add(RefreshToken(token=new_refresh, connection_id=rt.connection_id, client_id=client_id,
                           subject=rt.subject, scope=scope, audience=settings.canonical_resource,
                           issued_at=_now(), expires_at=_now() + settings.refresh_token_ttl_s, revoked=False))
        s.commit()
        return JSONResponse({
            "access_token": new_access, "token_type": "Bearer",
            "expires_in": settings.access_token_ttl_s, "refresh_token": new_refresh, "scope": scope,
        })
    finally:
        s.close()


# ─────────────────────────── /revoke (RFC 7009) + disconnect ───────────────────────────
async def revoke(request: Request) -> Response:
    form = await request.form()
    tok = form.get("token", "")
    s = session()
    try:
        at = s.query(AccessToken).filter(AccessToken.token == tok).first()
        rt = s.query(RefreshToken).filter(RefreshToken.token == tok).first()
        conn_id = (at.connection_id if at else None) or (rt.connection_id if rt else None)
        if at:
            at.revoked = True
        if rt:
            rt.revoked = True
        # Treat revocation as a disconnect: invalidate the connection AND deactivate the
        # per-connection product credential at the backend (best-effort).
        if conn_id:
            conn = s.query(Connection).filter(Connection.id == conn_id).first()
            if conn and not conn.revoked:
                conn.revoked = True
                if conn.product_credential_id:
                    try:
                        _bridge.revoke_credential(product_credential_id=conn.product_credential_id)
                    except Exception:
                        pass  # best-effort; token is already revoked locally
        s.commit()
    finally:
        s.close()
    return PlainTextResponse("", status_code=200)  # RFC 7009: 200 regardless


# ─────────────────────────── resource-server token validation ───────────────────────────
def validate_access_token(token_value: str) -> Optional[Dict[str, Any]]:
    """Return identity {connection_id, subject, scope, product_credential} for a valid token
    bound to THIS server's audience, else None. Used by the MCP transport middleware."""
    if not token_value:
        return None
    s = session()
    try:
        at = s.query(AccessToken).filter(AccessToken.token == token_value).first()
        if not at or at.revoked or _now() > at.expires_at:
            return None
        if at.audience.rstrip("/") != settings.canonical_resource.rstrip("/"):
            return None
        conn = s.query(Connection).filter(Connection.id == at.connection_id).first()
        if not conn or conn.revoked:
            return None
        return {
            "connection_id": conn.id,
            "subject": conn.subject,
            "scope": at.scope,
            "product_credential": conn.product_credential,
            "email": conn.email,
        }
    finally:
        s.close()


def routes() -> List[Route]:
    return [
        Route("/.well-known/oauth-protected-resource", well_known_prm, methods=["GET"]),
        Route("/.well-known/oauth-protected-resource/mcp", well_known_prm, methods=["GET"]),
        Route("/.well-known/oauth-authorization-server", well_known_asm, methods=["GET"]),
        Route("/.well-known/openid-configuration", well_known_asm, methods=["GET"]),
        Route("/register", register, methods=["POST"]),
        Route("/authorize", authorize, methods=["GET"]),
        Route("/authorize/callback", authorize_callback, methods=["GET"]),
        Route("/token", token, methods=["POST"]),
        Route("/revoke", revoke, methods=["POST"]),
    ]
