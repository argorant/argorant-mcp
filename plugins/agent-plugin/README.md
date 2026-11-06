# Argorant for Hermes Agent

Use [Argorant][argorant] from [Hermes Agent](https://hermes-agent.nousresearch.com):
find leads, check every email, write and send campaigns, sort replies, from
the app or from your own AI. It works with your Argorant account, the same
credits, lists, mailboxes and campaigns you see in the app.

```
You:    How many Heads of Sales at software companies in Germany can I reach?

Hermes: Argorant has 475 matching people. Here are three with names hidden.
        Counting and previewing used no credits. Revealing all of them would
        use up to 475 credits. Want me to save the search as a list first?
```

This is an [Agent Plugins v1](https://agent-plugins.org/specification) package
with no code of its own:

| File | What it does |
| --- | --- |
| `plugin.json` | Package manifest. Marks the Argorant server `untrusted`, so Hermes asks before any tool that spends, sends or changes something |
| `mcp.json` | Connects to Argorant's hosted MCP server at `https://mcp.argorant.com/mcp` |
| `skills/argorant/SKILL.md` | Which tool answers which question, and what needs your yes first |

## Requirements

- Hermes Agent 0.23.0 or newer
- Node.js 20.18.1 or newer, with `npx` on your `PATH`
- An Argorant account. [Create one for free][signup]; new accounts get free
  contact credits after confirming their email. [Pricing][pricing]

## Install

```bash
hermes plugins install argorant --no-enable
hermes plugins enable argorant
```

Or straight from this repository:
`hermes plugins install argorant/argorant-mcp/plugins/agent-plugin --no-enable`.

Start a new session. The first time the server starts, your browser opens
Argorant's sign-in page. Sign in and approve the connection. The token is kept
and refreshed, so you sign in once. If the tools do not appear after you sign
in, run `/reload-mcp`.

Ask Hermes to check your Argorant account first. A successful account check
confirms the connection.

### Hermes on a server

The sign-in sends your browser back to a callback port on the machine that runs
Hermes. On a remote host, forward the port that the sign-in prints
(`ssh -N -L <port>:127.0.0.1:<port> user@host`) before you approve. Or add the
server with Hermes's own OAuth client instead of this plugin, as shown on
[argorant.com/hermes-agent][hermes-page]:

```bash
hermes mcp add --url https://mcp.argorant.com/mcp --auth oauth argorant
hermes mcp test argorant
```

## What you can do

| Area | Tools |
| --- | --- |
| Account | `argorant_account`: who is connected, credits left, today's limits (free) |
| Find leads | `argorant_count_people`, `argorant_preview_people`, `argorant_company_people`, `search` (free, names hidden) |
| Contacts | `argorant_reveal_people`, `argorant_create_export`, `argorant_find_email`, `argorant_enrich` (credits, you approve first) |
| Lists | `argorant_create_list`, `argorant_list_lists`, `argorant_export_list` |
| Check emails you have | `argorant_quote_verification`, `argorant_start_verification` |
| Campaigns | `argorant_create_campaign`, `argorant_set_campaign_emails`, `argorant_add_campaign_leads`, `argorant_set_campaign_senders`, `argorant_send_test_email`, `argorant_launch_campaign`, `argorant_campaign_analytics` |
| Replies | `argorant_inbox`, `argorant_inbox_thread`, `argorant_inbox_classify`, `argorant_inbox_reply` |
| Mailboxes and credits | `argorant_list_inboxes`, `argorant_quote_inboxes`, `argorant_order_inboxes`, `argorant_quote_credits`, `argorant_buy_credits` |

The server has about 100 tools. The tool list comes from the hosted server at
run time, so it can change without a new release of this plugin. Every tool
description links to its page in the [tool reference][tools].

## What it will not do without you

- **No spending without a yes.** Counts and previews are free. Revealing,
  exporting, finding emails and adding new people to a campaign use contact
  credits, and the skill asks before each step.
- **No email without a yes.** A campaign is a draft until you approve the
  launch, and a reply to a lead is shown to you before it goes out.
- **Hermes asks too.** The server is marked `untrusted`, so Hermes asks before
  every tool the server does not mark read-only, and refuses those in
  unattended runs such as cron jobs.

## Disclosure

- Every tool call goes to Argorant's hosted server (`mcp.argorant.com`) and
  acts on your Argorant account. The tool set is served by that server at run
  time and is not covered by the pinned commit.
- Sign-in runs the pinned `mcp-remote@0.1.49` through `npx`, which opens a
  browser and a local callback port on first use and stores the OAuth tokens
  under `~/.mcp-auth`. You can see and remove the connection in Argorant under
  Settings, Integrations.
- Some tools spend contact credits. `argorant_launch_campaign` and
  `argorant_inbox_reply` send real email from your connected mailboxes.
  `argorant_buy_credits` and `argorant_order_inboxes` can charge the card saved
  in your workspace after your yes; with `pay_with: "link"` they return a
  payment link instead.
- Results include text other people wrote (replies, job titles, company
  details). The server labels reply text, and the bundled skill treats it as
  data.

## Support

[argorant.com][argorant] · [Tool reference][tools] ·
[support@argorant.com](mailto:support@argorant.com) ·
[Privacy](https://argorant.com/privacy) · [Terms](https://argorant.com/terms)

[argorant]: https://argorant.com
[signup]: https://app.argorant.com/signup
[pricing]: https://argorant.com/pricing
[hermes-page]: https://argorant.com/hermes-agent
[tools]: https://docs.argorant.com/docs/agents/tools
