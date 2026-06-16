"""Product-agnostic OAuth 2.1 Authorization Server + Resource Server core.

No VeriMails-specific assumptions live here. A product is plugged in by supplying an
``IdentityBridge`` (see ``bridge.py``) plus branding/scope config. This package is the
intended seed of a shared Palmstone identity service (Cliqte, MadeMySong, ...).
"""
