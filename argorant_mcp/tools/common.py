"""Shared tool plumbing for the public Argorant MCP server."""
from __future__ import annotations

from contextvars import ContextVar
from typing import Any, Callable, Dict, Optional

import anyio

from ..backend_client import BackendClient, BackendError

_identity: ContextVar[Optional[Dict[str, Any]]] = ContextVar("mcp_identity", default=None)


def set_identity(identity: Optional[Dict[str, Any]]):
    return _identity.set(identity)


def reset_identity(token) -> None:
    _identity.reset(token)


class ToolError(Exception):
    def __init__(self, code: str, message: str, retry_after: Optional[int] = None):
        self.code = code
        self.message = message
        self.retry_after = retry_after
        super().__init__(message)


def current_identity() -> Dict[str, Any]:
    ident = _identity.get()
    if not ident:
        raise ToolError("unauthorized", "No authenticated Argorant connection for this request.")
    return ident


def error_dict(error: ToolError) -> Dict[str, Any]:
    out = {"ok": False, "error": error.code, "message": error.message}
    if error.retry_after:
        out["retry_after_seconds"] = error.retry_after
    return out


async def backend_call(api_key: str, fn: Callable[[BackendClient], Any]) -> Any:
    def _do():
        try:
            return fn(BackendClient(api_key))
        except BackendError as exc:
            raise ToolError(exc.code, exc.message, retry_after=exc.retry_after)

    return await anyio.to_thread.run_sync(_do)

