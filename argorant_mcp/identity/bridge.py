"""The product-agnostic IdentityBridge contract.

Any product the shared identity layer serves implements two endpoints (here we call the
VeriMails ones, configured per-product):

  GET  {product}/oauth/bridge/consent?req=<signed>     — authenticate the product's user,
       show consent, redirect back to our callback with a signed single-use grant.
  POST {product}/oauth/bridge/provision-credential     — server-to-server: grant -> the
       user's product API credential.
  POST {product}/oauth/bridge/revoke-credential        — server-to-server: deactivate a
       per-connection credential on disconnect.

Both token types are HMAC-signed with a per-product shared secret. This module holds only
the generic plumbing; product specifics (URLs, secret, branding, scopes) come from a
``BridgeConfig``.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


@dataclass(frozen=True)
class BridgeConfig:
    product: str                 # "verimails"
    display_name: str            # "VeriMails"
    shared_secret: str
    consent_url: str
    provision_url: str
    revoke_url: str
    timeout_s: float = 30.0


def _b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _b64u_decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def sign(secret: str, payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    body = _b64u(raw)
    sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
    return body + "." + _b64u(sig)


def verify(secret: str, token: str, max_age: int) -> Optional[Dict[str, Any]]:
    if not token or not secret:
        return None
    try:
        body_b64, sig_b64 = token.split(".", 1)
        expected = hmac.new(secret.encode(), body_b64.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _b64u_decode(sig_b64)):
            return None
        payload = json.loads(_b64u_decode(body_b64))
        if max_age and (time.time() - float(payload.get("iat", 0))) > max_age:
            return None
        return payload
    except Exception:
        return None


class IdentityBridge:
    """Client-side driver for the bridge contract above."""

    def __init__(self, cfg: BridgeConfig):
        self.cfg = cfg

    # ── Step 1: build the signed request + the URL we send the browser to ──
    def build_consent_url(self, *, rid: str, client_name: str, scope: str,
                          callback: str, issuer: str, state: str, request_ttl: int) -> str:
        req = sign(self.cfg.shared_secret, {
            "typ": "bridge_request",
            "rid": rid,                 # our authorize-request id (binds the later grant)
            "client_name": client_name,
            "scope": scope,
            "callback": callback,       # our AS callback; backend pins redirect to `issuer`
            "issuer": issuer,
            "state": state,
            "iat": int(time.time()),
            "ttl": request_ttl,
        })
        return f"{self.cfg.consent_url}?req={httpx.QueryParams({'req': req})['req']}"

    # ── Step 2: validate the grant the backend sent back to our callback ──
    def verify_grant(self, grant: str, max_age: int) -> Optional[Dict[str, Any]]:
        payload = verify(self.cfg.shared_secret, grant, max_age=max_age)
        if not payload or payload.get("typ") != "bridge_grant":
            return None
        return payload

    # ── Step 3: server-to-server exchange grant -> product credential ──
    def provision_credential(self, *, grant: str, connection_ref: str) -> Dict[str, Any]:
        with httpx.Client(timeout=self.cfg.timeout_s) as client:
            resp = client.post(
                self.cfg.provision_url,
                headers={"Authorization": f"Bearer {self.cfg.shared_secret}"},
                json={"grant": grant, "connection_ref": connection_ref},
            )
        resp.raise_for_status()
        return resp.json()   # {user_id, email, api_key, api_key_id}

    # ── Disconnect: deactivate one per-connection credential ──
    def revoke_credential(self, *, product_credential_id: str) -> Dict[str, Any]:
        with httpx.Client(timeout=self.cfg.timeout_s) as client:
            resp = client.post(
                self.cfg.revoke_url,
                headers={"Authorization": f"Bearer {self.cfg.shared_secret}"},
                json={"api_key_id": product_credential_id},
            )
        resp.raise_for_status()
        return resp.json()
