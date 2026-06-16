"""MCP service storage (its own DB; entirely separate from the VeriMails backend DB).

Holds: registered OAuth clients (DCR), authorization codes, access/refresh tokens, the
identity→product-credential connection mapping, consumed grant jtis (replay defense),
and per-token spend tallies.
"""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

Base = declarative_base()

# Ensure the sqlite directory exists for the default path.
if settings.database_url.startswith("sqlite:///"):
    _path = settings.database_url.replace("sqlite:///", "", 1)
    os.makedirs(os.path.dirname(_path) or ".", exist_ok=True)

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    # Import models so they register on Base before create_all.
    from .identity import models  # noqa: F401
    Base.metadata.create_all(engine)


def session():
    return SessionLocal()
