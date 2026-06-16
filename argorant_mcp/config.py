"""Environment-driven settings for the public Argorant MCP server."""
from __future__ import annotations

import os
from dataclasses import dataclass


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    public_base_url: str = _env("MCP_PUBLIC_BASE_URL", "https://mcp.argorant.com")
    mcp_path: str = _env("MCP_PATH", "/mcp")

    host: str = _env("MCP_HOST", "127.0.0.1")
    port: int = _env_int("MCP_PORT", 8012)

    backend_base_url: str = _env("ARGORANT_BACKEND_BASE_URL", "http://127.0.0.1:8000")
    backend_public_url: str = _env("ARGORANT_BACKEND_PUBLIC_URL", "https://argorant.com")
    backend_timeout_s: float = float(_env("ARGORANT_BACKEND_TIMEOUT", "60"))

    bridge_secret: str = _env("ARGORANT_MCP_BRIDGE_SECRET", "")

    access_token_ttl_s: int = _env_int("MCP_ACCESS_TOKEN_TTL", 3600)
    refresh_token_ttl_s: int = _env_int("MCP_REFRESH_TOKEN_TTL", 30 * 86400)
    auth_code_ttl_s: int = _env_int("MCP_AUTH_CODE_TTL", 300)
    grant_ttl_s: int = _env_int("MCP_BRIDGE_GRANT_TTL", 120)
    request_ctx_ttl_s: int = _env_int("MCP_BRIDGE_REQUEST_TTL", 600)

    max_preview: int = _env_int("MCP_MAX_PREVIEW", 10)
    owner_max_preview: int = _env_int("MCP_OWNER_MAX_PREVIEW", 100)
    database_url: str = _env("MCP_DATABASE_URL", "sqlite:////opt/argorant-public-mcp/data/mcp.db")

    @property
    def canonical_resource(self) -> str:
        return self.public_base_url.rstrip("/") + self.mcp_path

    @property
    def issuer(self) -> str:
        return self.public_base_url.rstrip("/")

    @property
    def consent_url(self) -> str:
        return self.backend_public_url.rstrip("/") + "/api/oauth/bridge/consent"

    @property
    def provision_url(self) -> str:
        return self.backend_base_url.rstrip("/") + "/api/oauth/bridge/provision-credential"

    @property
    def revoke_url(self) -> str:
        return self.backend_base_url.rstrip("/") + "/api/oauth/bridge/revoke-credential"


settings = Settings()

