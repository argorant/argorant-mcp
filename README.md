# Argorant Public MCP

Hosted remote MCP server for Argorant.

- MCP endpoint: `https://mcp.argorant.com/mcp`
- Documentation: `https://argorant.com/docs/mcp/overview`
- Setup guide: `https://argorant.com/docs/mcp/connect`
- Tool reference: `https://argorant.com/docs/mcp/tools`
- ChatGPT setup: `https://argorant.com/docs/mcp/openai`
- Claude setup: `https://argorant.com/docs/mcp/claude`
- Security boundaries: `https://argorant.com/docs/mcp/security`
- Submission checklist: `https://argorant.com/docs/mcp/submission`

This is a hosted remote MCP connector. Claude, ChatGPT, and custom clients that
support remote MCP should connect to the endpoint directly; no npm package is
required for that flow. A local package can still be added later as an optional
bridge, but it should not be required for the public hosted connector.

The public server uses OAuth and account-scoped access. The first tools are
read-only by design:

- `search`
- `fetch`
- `argorant_account`
- `argorant_count_people`
- `argorant_preview_people`

`search` and `fetch` support ChatGPT apps, deep
research, and other clients that expect data-only search/fetch semantics. They
return aggregate coverage summaries and capped masked preview rows only.

Contact reveal, phone reveal, profile URLs, list creation, and exports are
disabled by default. Scoped reveal/export tools can only run after OAuth,
workspace permission, quota, plan, and audit checks. Use the signed-in
Argorant workspace for normal review and download workflows.

## Directory Readiness

Use the hosted endpoint for public review:

```text
https://mcp.argorant.com/mcp
```

Before submitting to ChatGPT, Claude, or an MCP directory, verify:

- The endpoint is reachable over public HTTPS.
- OAuth protected-resource and authorization-server metadata resolve on the MCP host.
- The connector manifest includes setup, security, privacy, terms, and submission links.
- Tools are read-only and return only counts, safe safe result links, or masked previews.
- Raw emails, phone numbers, profile URLs, reveal actions, exports, write actions, and destructive actions remain disabled by default.
- Reviewers have a normal member account and an owner/admin account for usage-limit testing.

## Discovery

Clients should discover OAuth metadata from the MCP host:

```text
https://mcp.argorant.com/.well-known/oauth-protected-resource
https://mcp.argorant.com/.well-known/oauth-protected-resource/mcp
https://mcp.argorant.com/.well-known/oauth-authorization-server
```

Unauthenticated requests to `/mcp` return a `401` response with a
`WWW-Authenticate` header that points to protected-resource metadata.

Argorant also publishes a connector manifest for client directories and setup
flows:

```text
https://mcp.argorant.com/manifest.json
https://mcp.argorant.com/.well-known/argorant-mcp.json
```

The manifest describes the MCP endpoint, docs, OAuth scopes, safe tools,
installation mode, and data-exposure defaults. It does not grant access by
itself.

## Local Service

The production service runs under systemd:

```bash
systemctl status argorant-public-mcp.service
systemctl restart argorant-public-mcp.service
```

The ASGI entrypoint is:

```text
argorant_mcp.app:app
```

Default runtime settings come from environment variables in systemd:

- `MCP_PUBLIC_BASE_URL`
- `MCP_PATH`
- `ARGORANT_BACKEND_BASE_URL`
- `ARGORANT_BACKEND_PUBLIC_URL`
- `ARGORANT_MCP_BRIDGE_SECRET`
- `MCP_DATABASE_URL`

## Smoke Checks

```bash
curl -sS https://mcp.argorant.com/ | python3 -m json.tool
curl -sS https://mcp.argorant.com/manifest.json | python3 -m json.tool
curl -sS https://mcp.argorant.com/.well-known/argorant-mcp.json | python3 -m json.tool
curl -sSI https://mcp.argorant.com/mcp
curl -sS https://mcp.argorant.com/.well-known/oauth-protected-resource | python3 -m json.tool
curl -sS https://mcp.argorant.com/.well-known/oauth-protected-resource/mcp | python3 -m json.tool
curl -sS https://mcp.argorant.com/.well-known/oauth-authorization-server | python3 -m json.tool
```

Expected behavior:

- `/` returns service metadata and links to docs.
- `/manifest.json` and `/.well-known/argorant-mcp.json` return connector metadata.
- `/mcp` returns `401` without a bearer token.
- OAuth discovery endpoints return JSON metadata.
- App, MCP, and API hosts stay separated:
  - `argorant.com` for marketing, docs, tools, and research pages.
  - `app.argorant.com` for login and the signed-in app.
  - `mcp.argorant.com` for remote MCP and OAuth metadata.
