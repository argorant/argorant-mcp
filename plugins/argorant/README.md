# Argorant

Run your entire B2B outreach inside Claude. Tell Claude who you sell to, and Argorant finds the companies and people that fit, gets their work emails, writes and launches the campaign from your own mailboxes, and brings the replies back into the chat.

This plugin connects Claude to your Argorant account and adds skills that turn Argorant's tools into finished outcomes. Every step that spends credits, buys something or sends email shows the price or the text first and waits for your yes.

## What you can do

- **Build a target list.** Count your market for free, preview example people with names hidden, leave roles, industries or countries out, and save the whole search as a private list.
- **Get contact details.** Reveal work emails and, where available, phone numbers for the people you pick, find one person's email from their name and company website, find emails for a whole spreadsheet, export a CSV file, or check the addresses on a list you already have. You only pay for emails that work.
- **Launch a campaign.** Argorant drafts the emails and follow-ups, adds a personal first line for each contact, fills in names with safe fallbacks such as {{company_normalized|your team}}, and launches from your own mailboxes only when you clearly say launch.
- **Work the reply inbox.** See interested replies first, read the whole conversation, and answer or forward in the same email thread after you approve the text.
- **Get sending mailboxes.** Connect Google Workspace, Microsoft 365 or almost any other mailbox through a secure link, or order new mailboxes on new domains after a full price quote, paid through a payment link.
- **Check your account and credits.** See credits left and today's limits, buy a credit pack through a payment link, and set up webhooks.

## Try it

- "How many heads of procurement work at manufacturers in Germany?"
- "Find software companies that sell to restaurants and show me their founders."
- "Find the work email of Jane Doe at acme.com."
- "Write a 3-email campaign for my list and personalize the first line for each person."
- "Show me today's interested replies and help me answer them."

In Claude Code and Cowork, the commands `/argorant:prospect`, `/argorant:campaign` and `/argorant:replies` start the three main flows directly.

## Setup

1. Add the plugin, then connect Argorant from the plugin's Connectors tab. On Claude Team and Enterprise, an owner adds the connector first.
2. Sign in with your Argorant account and approve the permissions. New accounts start with a free trial at https://argorant.com.
3. To send campaigns, connect at least one mailbox or order new ones. The get-mailboxes skill walks you through it.

## Safety

- Nothing is sent, bought, cancelled or deleted without your explicit yes in the chat.
- Prices are shown before anything that spends credits or money.
- Claude never asks for passwords or card details. Mailboxes connect through Argorant's own form and purchases are paid on Argorant's own payment page.
- Searching, counting, previewing and saving lists are free.

## Data

The plugin itself contains only instructions and stores nothing. It talks to one service, the Argorant connector at https://mcp.argorant.com/mcp, which you sign in to with OAuth. What you ask for in the chat, such as search filters, campaign text, reply answers and contact rows you provide, is sent to your Argorant account to do the work. Argorant's handling of that data is described in its privacy policy at https://argorant.com/privacy and its terms at https://argorant.com/terms.

## Links

- Documentation at https://docs.argorant.com
- Pricing at https://argorant.com/pricing
- Support at support@argorant.com or https://argorant.com/contact
