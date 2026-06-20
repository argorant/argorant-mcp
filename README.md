# Argorant MCP

**Verified B2B contact data for AI agents.** Search, count, preview, reveal, export, and build saved lists across **600M+ business contacts** — directly from Claude, ChatGPT, Cursor, and any MCP client.

- **MCP endpoint:** `https://mcp.argorant.com/mcp`
- **Transport:** Streamable HTTP · **Auth:** OAuth 2.1 (Dynamic Client Registration, account-scoped)
- **Website:** https://argorant.com · **Privacy:** https://argorant.com/privacy · **Terms:** https://argorant.com/terms

This is a **hosted remote connector** — no install, no API key paste. Clients connect to the endpoint and authenticate via OAuth. A standalone CLI also exists (`npx argorant`) for terminal/script use.

## Connect

**Claude** (claude.ai / Desktop): Settings → Connectors → *Add custom connector* → URL `https://mcp.argorant.com/mcp` → complete the OAuth login.

**ChatGPT** (Developer Mode): Settings → Apps & Connectors → Advanced → enable Developer Mode → Connectors → *Create* → URL `https://mcp.argorant.com/mcp`. The `search` + `fetch` tools make it usable as a Deep Research connector.

**Cursor / other MCP clients:** add the remote server from `mcp.json`:

```json
{
  "mcpServers": {
    "argorant": {
      "url": "https://mcp.argorant.com/mcp"
    }
  }
}
```

## Tools

Free (no credits, masked/aggregate only):

| Tool | What it does |
|---|---|
| `search` / `fetch` | ChatGPT-style coverage search + safe summary (masked previews, counts) |
| `argorant_account` | Connected account, scopes, limits |
| `argorant_count_people` | Count matching contacts by role, seniority, dept, industry, geo |
| `argorant_preview_people` | Masked preview rows (initials, role, company, location) |

Consume credits (require OAuth scope + permission; verification is live at this step and **only valid/deliverable contacts are billed**):

| Tool | What it does |
|---|---|
| `argorant_reveal_people` | Reveal real emails, phones, profile URLs for a small set |
| `argorant_create_export` / `argorant_export_list` | Async CSV export (large lists) |
| `argorant_create_list` / `argorant_list_status` | Build & inspect reusable saved lists |
| `argorant_export_status` / `argorant_export_batch_status` / `argorant_download_export_preview` | Track & fetch exports |

Tools are annotated with read-only vs. action hints. Reveal/export/list actions only run after OAuth, scope, permission, quota, and plan checks; without credits they are blocked by design.

## Data & privacy posture

- **OAuth + account-scoped.** Unauthenticated requests to `/mcp` return `401` with `WWW-Authenticate` pointing at protected-resource metadata.
- **Masked by default.** `search`/`fetch`/`preview` never return raw emails, phones, or profile URLs — only aggregate coverage and masked rows. Raw contact details require the scoped reveal/export tools and consume credits.
- **Verification is live.** Emails are verified at reveal/export time; you are billed only for deliverable contacts. Raw verification status is never exposed as a queryable field.
- **Hosts are separated:** `argorant.com` (marketing/docs), `app.argorant.com` (signed-in app), `mcp.argorant.com` (remote MCP + OAuth).

## OAuth discovery

```text
https://mcp.argorant.com/.well-known/oauth-protected-resource
https://mcp.argorant.com/.well-known/oauth-authorization-server
```

Dynamic Client Registration is supported at `/register` (grant types: `authorization_code`, `refresh_token`).

## Documentation

- Overview: https://argorant.com/docs/mcp/overview
- Connect guide: https://argorant.com/docs/mcp/connect
- Tool reference: https://argorant.com/docs/mcp/tools
- Claude setup: https://argorant.com/docs/mcp/claude · ChatGPT setup: https://argorant.com/docs/mcp/openai
- Security: https://argorant.com/docs/mcp/security
- CLI: https://argorant.com/docs/cli

## Registry metadata

- `mcp.json` — Open Plugins / Cursor remote-server declaration.
- `server.json` — official [MCP Registry](https://github.com/modelcontextprotocol/registry) entry (`io.github.argorant/argorant-mcp`, remote streamable-http).
