"""OAuth discovery documents required by the MCP authorization spec.

- RFC 9728 Protected Resource Metadata  → /.well-known/oauth-protected-resource
- RFC 8414 Authorization Server Metadata → /.well-known/oauth-authorization-server
  (also served at /.well-known/openid-configuration for OIDC-discovery clients)

The MCP server co-hosts its authorization server, so both point at the same origin.
"""
from __future__ import annotations

from typing import Dict, List


def protected_resource_metadata(*, resource: str, issuer: str, scopes: List[str]) -> Dict:
    # RFC 9728 §3
    return {
        "resource": resource,
        "authorization_servers": [issuer],
        "scopes_supported": scopes,
        "bearer_methods_supported": ["header"],
        "resource_documentation": "https://argorant.com/docs/mcp/overview",
    }


def authorization_server_metadata(*, issuer: str, scopes: List[str]) -> Dict:
    # RFC 8414 §2 (subset MCP requires) + PKCE advertisement + RFC 9207 iss.
    return {
        "issuer": issuer,
        "authorization_endpoint": f"{issuer}/authorize",
        "token_endpoint": f"{issuer}/token",
        "registration_endpoint": f"{issuer}/register",          # RFC 7591 DCR
        "revocation_endpoint": f"{issuer}/revoke",
        "scopes_supported": scopes,
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],            # PKCE — MUST be present
        "token_endpoint_auth_methods_supported": ["none", "client_secret_post"],
        "authorization_response_iss_parameter_supported": True,  # RFC 9207
        "client_id_metadata_document_supported": False,
    }
