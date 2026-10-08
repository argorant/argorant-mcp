# Argorant for Claude, ChatGPT and other AI assistants

Argorant fills your sales pipeline from the chat. Describe who you sell to, and Argorant finds the companies and people that fit among over 600 million business contacts, gets their work emails, runs campaigns from your own mailboxes and brings every reply back into the conversation.

Prices are shown first. Nothing is bought, sent, cancelled or deleted without your yes.

This repository holds the Argorant connector (a hosted remote MCP server at `https://mcp.argorant.com/mcp`) and the Argorant plugin for Claude. There is nothing to install and no API key to paste. You sign in with your Argorant account, and new accounts start with a free trial at https://argorant.com.

## What Argorant does for you

- **Builds your target list.** Counts your market for free, shows example people with names hidden, leaves out the roles, industries or countries you exclude, and saves the whole search as a private list.
- **Gets contact details.** Work emails and, where available, phone numbers for the people you pick. You only pay for emails that work, and people you already unlocked are free again. It also finds one person's email from their name and company website, or checks a list you already have.
- **Runs your campaigns.** Writes the emails and follow-ups, adds a personal first line for each contact, and launches from your own mailboxes only when you clearly say launch.
- **Brings replies back.** Shows interested replies first and answers or forwards them in the same email thread once you approve the text.
- **Gets you mailboxes to send from.** Connects Google Workspace, Microsoft 365 or almost any other mailbox through Argorant's own secure form, or sets up new mailboxes on new domains after a full price quote, paid through a payment link.
- **Keeps you in control of spend.** Shows credits left and the price of every step before it runs.

## Connect

**Claude.** Add the Argorant plugin from the directory, or open Customize, Connectors, Add custom connector, and enter `https://mcp.argorant.com/mcp`. Then sign in with your Argorant account.

**ChatGPT.** Open Settings, Apps and Connectors, Advanced, turn on Developer Mode, then create a connector with `https://mcp.argorant.com/mcp` and sign in.

**Cursor and other MCP clients.** Add the server from `mcp.json`.

```json
{
  "mcpServers": {
    "argorant": {
      "url": "https://mcp.argorant.com/mcp"
    }
  }
}
```

## Claude plugin

The folder [`plugins/argorant`](plugins/argorant) holds the Argorant plugin for Claude. It pairs this connector with skills that turn its tools into finished outcomes, so Claude knows the right order of steps, shows prices first and asks before anything is spent or sent.

In Claude Code, add it with `claude plugin marketplace add argorant/argorant-mcp` and then `claude plugin install argorant@argorant`.

## Try it

- "How many heads of procurement work at manufacturers in Germany?"
- "Find software companies that sell to restaurants and show me their founders."
- "Find the work email of Jane Doe at acme.com."
- "Write a 3-email campaign for my list and personalize the first line for each person."
- "Show me today's interested replies and help me answer them."

## Safety and privacy

- You sign in with OAuth, and Argorant only acts inside your own account.
- Searching, counting, previewing and saving lists are free and show no contact details. Contact details appear only when you choose to reveal or export them, after the price is shown.
- Sending email, buying credits or mailboxes, cancelling and deleting always wait for your explicit yes.
- Claude and ChatGPT never ask for passwords or card details. Mailboxes connect through Argorant's own form, and purchases are paid on Argorant's own payment page.
- Daily safety limits protect every account. They cost nothing and reset each day.

Read more in the privacy policy at https://argorant.com/privacy and the terms at https://argorant.com/terms.

## Documentation

- Getting started with AI assistants at https://docs.argorant.com/docs/agents
- Claude setup at https://docs.argorant.com/docs/agents/claude
- ChatGPT setup at https://docs.argorant.com/docs/agents/chatgpt
- Every tool at https://docs.argorant.com/docs/agents/tools
- Security at https://docs.argorant.com/docs/agents/security
- Support at support@argorant.com

## For developers

- Sign-in discovery is at `https://mcp.argorant.com/.well-known/oauth-protected-resource` and `https://mcp.argorant.com/.well-known/oauth-authorization-server`. Dynamic client registration is supported.
- `mcp.json` declares the remote server for Cursor and other clients that read that format.
- `server.json` is the entry for the official MCP Registry (`io.github.argorant/argorant-mcp`, remote streamable HTTP).
- `argorant_mcp/` holds the connector's source.
