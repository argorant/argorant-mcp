"""MCP tool modules."""

from . import account, search


def register_all(mcp) -> None:
    account.register(mcp)
    search.register(mcp)

