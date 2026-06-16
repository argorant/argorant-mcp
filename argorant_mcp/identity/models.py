"""OAuth + connection ORM models for the MCP identity store.

Product-agnostic: the only product-specific value is ``Connection.product_credential``
(an opaque per-connection API credential the bridge handed us) and
``product_credential_id`` (the backend id used to revoke it). Nothing else assumes VeriMails.
"""
from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, Boolean

from ..db import Base


class OAuthClient(Base):
    """A registered MCP client (RFC 7591 Dynamic Client Registration)."""
    __tablename__ = "oauth_clients"

    client_id = Column(String, primary_key=True)
    client_secret = Column(String, nullable=True)        # null for public clients (PKCE only)
    client_name = Column(String, nullable=True)
    redirect_uris = Column(Text, nullable=False)         # JSON list
    grant_types = Column(Text, nullable=True)            # JSON list
    token_endpoint_auth_method = Column(String, default="none")
    created_at = Column(Integer, nullable=False)


class AuthCode(Base):
    """A short-lived OAuth authorization code. It carries the backend bridge *grant*
    forward to /token, where HMAC + 120s freshness + PKCE + rid-match + jti-consume are
    all validated together before any credential is provisioned."""
    __tablename__ = "auth_codes"

    code = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    code_challenge = Column(String, nullable=False)      # PKCE S256 challenge
    code_challenge_method = Column(String, default="S256")
    scope = Column(String, default="")
    resource = Column(String, nullable=True)             # RFC 8707 audience requested
    rid = Column(String, nullable=False)                 # binds to the bridge grant's rid
    grant = Column(Text, nullable=False)                 # the signed backend bridge grant
    created_at = Column(Integer, nullable=False)
    used = Column(Boolean, default=False)


class Connection(Base):
    """A durable identity↔product-credential link for one (client, subject) pairing."""
    __tablename__ = "connections"

    id = Column(String, primary_key=True)                # connection_ref (stable per client+subject)
    client_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    email = Column(String, nullable=True)
    product_credential = Column(String, nullable=False)  # opaque; NEVER returned to the agent
    product_credential_id = Column(String, nullable=True)
    created_at = Column(Integer, nullable=False)
    revoked = Column(Boolean, default=False)


class AccessToken(Base):
    """An opaque bearer access token issued by THIS authorization server."""
    __tablename__ = "access_tokens"

    token = Column(String, primary_key=True)             # opaque random
    connection_id = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    scope = Column(String, default="")
    audience = Column(String, nullable=False)            # canonical resource this token is valid for
    issued_at = Column(Integer, nullable=False)
    expires_at = Column(Integer, nullable=False)
    revoked = Column(Boolean, default=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String, primary_key=True)
    connection_id = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    scope = Column(String, default="")
    audience = Column(String, nullable=False)
    issued_at = Column(Integer, nullable=False)
    expires_at = Column(Integer, nullable=False)
    revoked = Column(Boolean, default=False)


class ConsumedGrant(Base):
    """Single-use guard for backend bridge grants (replay defense)."""
    __tablename__ = "consumed_grants"

    jti = Column(String, primary_key=True)               # UNIQUE PK == single-use guarantee
    consumed_at = Column(Integer, nullable=False)


class SpendEvent(Base):
    """Per-connection credit spend, summed over a rolling window for the spend cap.
    Tracking on the CONNECTION (not the access token) means refreshing a token cannot
    reset the cap."""
    __tablename__ = "spend_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    connection_id = Column(String, index=True, nullable=False)
    amount = Column(Integer, nullable=False)
    ts = Column(Integer, nullable=False)
    tool = Column(String, nullable=True)
