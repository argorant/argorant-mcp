"""Argorant product adapter for the shared OAuth/MCP identity core."""
from __future__ import annotations

import hashlib

from ..config import settings
from ..identity.bridge import BridgeConfig, IdentityBridge

DISPLAY_NAME = "Argorant"

SCOPES = [
    "argorant:read_counts",
    "argorant:search_segments",
    "argorant:manage_lists",
    "argorant:create_exports",
    "argorant:unlock_contacts",
]


def build_bridge() -> IdentityBridge:
    return IdentityBridge(BridgeConfig(
        product="argorant",
        display_name=DISPLAY_NAME,
        shared_secret=settings.bridge_secret,
        consent_url=settings.consent_url,
        provision_url=settings.provision_url,
        revoke_url=settings.revoke_url,
    ))


def connection_ref(client_id: str, subject: str) -> str:
    digest = hashlib.sha256(f"argorant:{client_id}:{subject}".encode()).hexdigest()
    return digest[:32]
