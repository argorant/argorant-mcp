"""Account and connector health tools."""
from __future__ import annotations

from typing import Any, Dict

from mcp.types import ToolAnnotations

from .common import ToolError, backend_call, current_identity, error_dict

_READ = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


def register(mcp) -> None:
    @mcp.tool(
        name="argorant_account",
        description="Check the connected Argorant account and connector limits. COST: free.",
        annotations=_READ,
    )
    async def argorant_account() -> Dict[str, Any]:
        ident = current_identity()
        try:
            return await backend_call(ident["product_credential"], lambda client: client.account())
        except ToolError as exc:
            return error_dict(exc)

