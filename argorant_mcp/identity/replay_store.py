"""Single-use / replay store for backend bridge grants.

A grant is only single-use if this tracking actually exists: the grant's ``jti`` is
inserted into a UNIQUE-PK table inside the /token transaction; a second attempt collides
and is rejected. Freshness (120s) is enforced separately by the HMAC signature check, so
even a never-seen jti past its TTL is refused upstream.
"""
from __future__ import annotations

import time

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from ..db import session
from .models import ConsumedGrant


def consume(jti: str) -> bool:
    """Atomically mark a grant jti as used. Returns False if already used (replay) or empty."""
    if not jti:
        return False
    s = session()
    try:
        s.add(ConsumedGrant(jti=jti, consumed_at=int(time.time())))
        s.commit()
        return True
    except IntegrityError:          # primary-key collision → already consumed
        s.rollback()
        return False
    finally:
        s.close()


def purge_expired(max_age_s: int = 120) -> int:
    """Housekeeping only — expired jtis can never be replayed (signature TTL already rejects them)."""
    cutoff = int(time.time()) - max_age_s
    s = session()
    try:
        result = s.execute(delete(ConsumedGrant).where(ConsumedGrant.consumed_at < cutoff))
        s.commit()
        return result.rowcount or 0
    finally:
        s.close()
