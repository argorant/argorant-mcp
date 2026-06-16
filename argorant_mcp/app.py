"""ASGI entrypoint for the public Argorant MCP server."""
from __future__ import annotations

import os

from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from .config import settings
from .db import init_db
from .identity import server as idsrv
from .products import argorant as product
from .tools import common as tools_common
from .tools import register_all

_host = settings.public_base_url.split("://", 1)[-1].rstrip("/")
_transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[_host, f"{_host}:443", "127.0.0.1:8012", "localhost:8012"],
    allowed_origins=[
        settings.issuer,
        "https://claude.ai",
        "https://chatgpt.com",
        "https://chat.openai.com",
        "http://localhost:6274",
        "http://127.0.0.1:6274",
    ],
)

mcp = FastMCP(
    name="Argorant",
    stateless_http=True,
    json_response=True,
    transport_security=_transport_security,
)
register_all(mcp)

idsrv.configure(
    bridge=product.build_bridge(),
    scopes=product.SCOPES,
    connection_ref=product.connection_ref,
)

ALLOWED_ORIGINS = {o.strip() for o in os.getenv("MCP_ALLOWED_ORIGINS", "").split(",") if o.strip()}


def _connector_manifest() -> dict:
    return {
        "schema_version": "2026-06-02",
        "name": "Argorant",
        "service": "argorant-mcp",
        "description": (
            "OAuth-protected MCP server for Argorant B2B contact coverage, "
            "aggregate counts, masked previews, scoped contact reveal, and tracked exports."
        ),
        "mcp_endpoint": settings.canonical_resource,
        "issuer": settings.issuer,
        "documentation_url": "https://argorant.com/docs/mcp/overview",
        "connect_url": "https://argorant.com/docs/mcp/connect",
        "tools_url": "https://argorant.com/docs/mcp/tools",
        "openai_setup_url": "https://argorant.com/docs/mcp/openai",
        "claude_setup_url": "https://argorant.com/docs/mcp/claude",
        "security_url": "https://argorant.com/docs/mcp/security",
        "submission_url": "https://argorant.com/docs/mcp/submission",
        "privacy_policy_url": "https://argorant.com/privacy",
        "terms_url": "https://argorant.com/terms",
        "logo_url": "https://argorant.com/favicon.svg",
        "publisher": {
            "name": "Argorant",
            "website": "https://argorant.com",
            "support_url": "https://argorant.com/docs/mcp/overview",
            "privacy_policy_url": "https://argorant.com/privacy",
            "terms_url": "https://argorant.com/terms",
        },
        "hosts": {
            "marketing": "https://argorant.com",
            "app": "https://app.argorant.com",
            "mcp": settings.issuer,
        },
        "directory_listing": {
            "category": "Sales intelligence",
            "tagline": "Search verified B2B contact coverage from AI agents.",
            "summary": (
                "Argorant lets AI clients search company and people coverage, "
                "count matching segments, preview masked rows, and create scoped "
                "lead reveal/export workflows through an OAuth-protected remote MCP server."
            ),
            "audience": [
                "Revenue teams building AI SDR workflows",
                "Sales operations teams comparing account coverage",
                "Developers adding B2B data to agents",
            ],
            "example_use_cases": [
                "Count engineering leaders at a target account",
                "Preview coverage before exporting in the Argorant app",
                "Save a reusable lead list from an AI search",
                "Reveal a small approved contact set with account quota controls",
                "Create a tracked verified export for a larger segment",
                "Check whether a company has enough contacts for a campaign",
            ],
        },
        "installation": {
            "type": "hosted_remote_mcp",
            "requires_package_install": False,
            "connector_url": settings.canonical_resource,
            "package_status": "not_required_for_hosted_remote_mcp",
            "note": (
                "Use the hosted MCP endpoint directly in clients that support remote MCP. "
                "A local npm bridge is not required for Claude, ChatGPT, or custom clients "
                "that can connect to remote OAuth-protected MCP servers."
            ),
        },
        "auth": {
            "type": "oauth2",
            "protected_resource_metadata": f"{settings.issuer}/.well-known/oauth-protected-resource",
            "protected_resource_metadata_for_mcp_path": f"{settings.issuer}/.well-known/oauth-protected-resource/mcp",
            "authorization_server_metadata": f"{settings.issuer}/.well-known/oauth-authorization-server",
            "scopes": product.SCOPES,
        },
        "tools": [
            {
                "name": "search",
                "description": "Search Argorant coverage for companies, markets, roles, and locations.",
                "data_exposure": "aggregate counts and safe result links",
            },
            {
                "name": "fetch",
                "description": "Open a safe Argorant result with coverage summaries and capped masked preview rows.",
                "data_exposure": "aggregate counts and masked previews",
            },
            {
                "name": "argorant_account",
                "description": "Check the connected Argorant account and usage state.",
                "data_exposure": "account metadata",
            },
            {
                "name": "argorant_count_people",
                "description": "Count matching B2B contacts by company, title, location, seniority, and department filters.",
                "data_exposure": "aggregate counts",
            },
            {
                "name": "argorant_preview_people",
                "description": "Preview matching segments with masked people rows for planning AI SDR workflows.",
                "data_exposure": "masked previews",
            },
            {
                "name": "argorant_reveal_people",
                "description": "Reveal a small approved set of raw contacts through workspace permissions and quota controls.",
                "data_exposure": "raw emails, phones, and profile URLs when scoped and permitted",
                "required_scope": "argorant:unlock_contacts",
            },
            {
                "name": "argorant_create_export",
                "description": "Create tracked async lead export jobs or batches from filters.",
                "data_exposure": "export job metadata; raw CSV available after scoped download",
                "required_scope": "argorant:create_exports",
            },
            {
                "name": "argorant_create_list",
                "description": "Save a reusable lead list from filters or selected record IDs.",
                "data_exposure": "list metadata only",
                "required_scope": "argorant:manage_lists",
            },
            {
                "name": "argorant_list_status",
                "description": "Check saved lead list metadata.",
                "data_exposure": "list metadata only",
                "required_scope": "argorant:manage_lists",
            },
            {
                "name": "argorant_export_list",
                "description": "Create a tracked async export from a saved lead list.",
                "data_exposure": "export job metadata; raw CSV available after scoped download",
                "required_scope": "argorant:manage_lists argorant:create_exports",
            },
            {
                "name": "argorant_export_status",
                "description": "Check a lead export job status.",
                "data_exposure": "export status metadata",
                "required_scope": "argorant:create_exports",
            },
            {
                "name": "argorant_export_batch_status",
                "description": "Check a multi-file export batch status.",
                "data_exposure": "export batch status metadata",
                "required_scope": "argorant:create_exports",
            },
            {
                "name": "argorant_download_export_preview",
                "description": "Return a capped text preview of a completed export CSV for small agent handoffs.",
                "data_exposure": "raw export rows, capped and only when scoped and permitted",
                "required_scope": "argorant:create_exports",
            },
        ],
        "safe_defaults": {
            "raw_emails": False,
            "phone_numbers": False,
            "profile_urls": False,
            "exports": False,
            "contact_reveal": False,
            "write_actions": False,
            "destructive_actions": False,
            "open_web_actions": False,
            "note": (
                "Search/fetch/count/preview return aggregate counts and masked previews. "
                "Raw contact fields, exports, contact reveal, write actions, destructive actions, "
                "and open-web actions are disabled by default."
            ),
        },
        "scoped_capabilities": {
            "exports": "available only through scoped export tools with signed-in Argorant workspace permissions",
            "contact_reveal": "available only through scoped reveal tools with quota and account checks",
            "write_actions": "limited to scoped list/export creation tools; no destructive writes",
            "note": (
                "Scoped tools require explicit OAuth scopes plus Argorant workspace permissions, "
                "plan limits, quota checks, and audit logs. They are not safe defaults."
            ),
        },
        "quotas": {
            "mode": "account_scoped",
            "member_accounts": "daily count, preview, reveal, and export-row limits",
            "admin_owner_accounts": "can be configured for unlimited access",
        },
        "chatgpt_compatibility": {
            "data_only_search_fetch": True,
            "responses_api_server_url": settings.canonical_resource,
            "recommended_require_approval": "for_reveal_and_export_tools",
            "tool_annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": False,
            },
            "note": (
                "The search and fetch tools are read-only tools for ChatGPT apps, "
                "deep research, and other MCP clients that expect search/fetch semantics. "
                "They return aggregate counts and masked previews. Raw contact reveal and "
                "exports are separate scoped tools that should require user approval."
            ),
        },
        "claude_compatibility": {
            "remote_mcp_url": settings.canonical_resource,
            "custom_connector": True,
            "oauth_required": True,
            "organization_setup": "Team and Enterprise owners add the connector before members connect.",
        },
        "submission_readiness": {
            "public_https_endpoint": True,
            "oauth_metadata": True,
            "protected_resource_metadata": True,
            "privacy_policy": True,
            "terms": True,
            "read_only_public_tools": True,
            "test_prompts_url": "https://argorant.com/docs/mcp/submission",
            "review_security_url": "https://argorant.com/docs/mcp/security",
        },
    }


async def health(request) -> JSONResponse:
    return JSONResponse({
        "service": "argorant-mcp",
        "status": "ok",
        "resource": settings.canonical_resource,
        "issuer": settings.issuer,
        "documentation": "https://argorant.com/docs/mcp/overview",
        "connect": "https://argorant.com/docs/mcp/connect",
        "tools": "https://argorant.com/docs/mcp/tools",
        "manifest": f"{settings.issuer}/manifest.json",
        "well_known_manifest": f"{settings.issuer}/.well-known/argorant-mcp.json",
        "metadata": {
            "protected_resource": f"{settings.issuer}/.well-known/oauth-protected-resource",
            "protected_resource_for_mcp_path": f"{settings.issuer}/.well-known/oauth-protected-resource/mcp",
            "authorization_server": f"{settings.issuer}/.well-known/oauth-authorization-server",
        },
        "bridge_configured": bool(settings.bridge_secret),
    })


async def manifest(request) -> JSONResponse:
    return JSONResponse(_connector_manifest())


def _challenge_headers() -> dict:
    prm = f"{settings.issuer}/.well-known/oauth-protected-resource"
    scope = " ".join(product.SCOPES)
    return {"WWW-Authenticate": f'Bearer resource_metadata="{prm}", scope="{scope}"'}


class GatewayMiddleware:
    def __init__(self, app, mcp_path: str):
        self.app = app
        self.mcp_path = mcp_path

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}

        origin = headers.get("origin")
        if origin and ALLOWED_ORIGINS and origin not in ALLOWED_ORIGINS and origin != settings.issuer:
            await self._send_json(send, 403, {"error": "forbidden_origin", "origin": origin})
            return

        if path == self.mcp_path or path.startswith(self.mcp_path + "/"):
            auth = headers.get("authorization", "")
            token = auth[7:] if auth.lower().startswith("bearer ") else ""
            identity = idsrv.validate_access_token(token)
            if not identity:
                await self._send_json(send, 401, {"error": "invalid_token"}, _challenge_headers())
                return
            ctx_token = tools_common.set_identity(identity)
            try:
                await self.app(scope, receive, send)
            finally:
                tools_common.reset_identity(ctx_token)
            return

        await self.app(scope, receive, send)

    @staticmethod
    async def _send_json(send, status: int, body: dict, extra_headers: dict | None = None):
        import json as _json
        raw = _json.dumps(body).encode()
        headers = [(b"content-type", b"application/json")]
        for key, value in (extra_headers or {}).items():
            headers.append((key.encode(), value.encode()))
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": raw})


def _build_app():
    init_db()
    app = mcp.streamable_http_app()
    for route in idsrv.routes():
        app.router.routes.append(route)
    app.router.routes.append(Route("/", health, methods=["GET"]))
    app.router.routes.append(Route("/healthz", lambda req: PlainTextResponse("ok"), methods=["GET"]))
    app.router.routes.append(Route("/manifest.json", manifest, methods=["GET"]))
    app.router.routes.append(Route("/.well-known/argorant-mcp.json", manifest, methods=["GET"]))
    app.add_middleware(GatewayMiddleware, mcp_path=settings.mcp_path)
    return app


app = _build_app()
