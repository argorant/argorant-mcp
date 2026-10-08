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
- "Who should I sell to? Here is our website."
- "Write a 3-step sequence for heads of logistics at manufacturers in DACH and review it before launch."

## Skills, agents and commands

Skills load on their own when a request fits.

| Skill | What it does |
| --- | --- |
| define-icp-and-size-market | Turns a website or a one-line offer into segment ideas, counts each for free and picks the best 2 or 3 |
| build-target-list | Counts a market, previews people with names hidden and saves the search as a list |
| advanced-list-building | Include and exclude on every filter, title matching, keyword scope, sells-to searches, saved searches, dedupe, valid-only lists and list size planning |
| get-contacts | Reveals work emails and phones, finds emails for names, exports CSV files and checks your own lists, price first |
| cold-email-copywriting | Short peer-level emails and 3-step sequences, lowercase subjects, spintax, safe fallbacks, A/B variants and a review checklist |
| personalization-at-scale | A personal line per contact from facts that were looked up, 5 examples first, fallback for the rest |
| sequences-and-subsequences | Follow-up timing, same-thread follow-ups, stop on reply and keyword-triggered branches |
| launch-campaign | Sets up the campaign, adds people and mailboxes, checks it and launches on your yes |
| deliverability-and-sending | Mailbox capacity, daily limits, pacing, warm-up as your choice, bounce protection and clean lists |
| campaign-analytics-and-optimization | Reads results, finds the weak link and tests one change at a time |
| work-reply-inbox | Interested replies first, full threads, answers and forwards after your yes, labels and blocklist |
| reply-handling-playbook | Answers by kind of reply, objection templates, meeting booking and handing over to a colleague |
| get-mailboxes | Connects your mailboxes or orders new ones on new domains after a full quote |
| account-and-credits | Credits, daily limits, credit packs through a payment link and webhooks |

Two agents help in the background. lead-researcher researches one contact or company from public facts and suggests a personal line with its source. copy-reviewer checks a sequence against the copywriting rules and the merge field and placeholder rules before launch. Both only read and never change anything.

In Claude Code and Cowork, six commands start the main flows directly.

| Command | What it starts |
| --- | --- |
| /argorant:icp | Ranked segments with real counts from a website or an offer |
| /argorant:prospect | A counted, previewed and saved lead list |
| /argorant:write-sequence | A reviewed 3-step sequence |
| /argorant:personalize | A personal line for every contact in a campaign |
| /argorant:campaign | A full campaign, launched only on your yes |
| /argorant:replies | Interested replies with draft answers |

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
