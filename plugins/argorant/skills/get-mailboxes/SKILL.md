---
name: get-mailboxes
description: Get mailboxes to send campaigns from with Argorant. Use when the user has no sending mailbox, wants to connect Google Workspace, Microsoft or another email provider such as Zoho or Fastmail, wants new mailboxes on new domains so their main domain stays protected, asks what new mailboxes cost, wants to order them, follow an order, stop a domain renewal, cancel mailboxes, or pause or disconnect a mailbox.
---

# Get sending mailboxes

Campaigns send from mailboxes connected to Argorant. The user can connect mailboxes they already have, or Argorant sets up new mailboxes on new domains, ready to send, so the main company domain stays protected.

## Ground rules

- Never ask for a mailbox password, an app password, card details or any other secret in the chat. Mailboxes from other providers connect through the link to Argorant's own form, and purchases are paid on Argorant's own payment page. If the user pastes a password anyway, do not repeat it or pass it to any tool, and suggest they change it.
- Show the full price before any order, and order only after the user's explicit yes in this chat.
- You never open, fill in or pay a payment page. Give the user the payment link and let them pay.
- Never cancel, stop a renewal or disconnect without a clear yes.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## See what is connected

`argorant_list_inboxes` lists connected mailboxes with their health and daily sending limits.

## Connect mailboxes the user already has

- **Google Workspace.** Call `argorant_connect_google_workspace` without emails. It returns a client ID and permissions that the Workspace admin pastes in Google Admin under domain-wide delegation. Walk the user through that. Then call it again to list the mailboxes, and once more with the addresses the user picks, or an empty list for all. No passwords are involved.
- **Microsoft 365.** Send the user to the Mailboxes page in the Argorant app at https://app.argorant.com/inboxes, where they sign in with Microsoft.
- **Any other provider** such as Zoho, Fastmail, Yahoo, iCloud or a web host. Call `argorant_connect_smtp_mailbox` or `argorant_test_smtp_mailbox` with the address and server details only. Through Claude they return a link to Argorant's mailbox form, where the user enters the password and the mailbox is tested and connected. Give the user that link. Many providers need an app password instead of the normal one, so mention that.

## Order new mailboxes

1. Ask how many cold emails a day the user wants to send, or how many mailboxes, and which website or brand the new domains should be based on.
2. Call `argorant_quote_inboxes`. It checks nothing out and charges nothing. If the user wants other names, `argorant_suggest_inbox_domains` suggests available domains with first-year and renewal prices.
3. Show the full quote in plain words. That means every domain with its first-year and renewal price, the number of mailboxes, the amount due today, the recurring total, what is included and how it is paid. Offer nothing the quote does not list. The quote is valid for 24 hours.
4. Ask "Order this for the amount due today?" and wait for a clear yes.
5. Call `argorant_order_inboxes` with confirmed=true. Through Claude it returns a payment link that the workspace owner opens and pays. Give the link and say that setup starts once the payment went through.
6. Follow progress with `argorant_inbox_order_status`. New mailboxes wait about 24 hours after setup before they start sending.

## Change or end mailboxes

- `argorant_update_inbox` changes a mailbox's daily limit, display name or timezone, or pauses it with active=false.
- `argorant_disconnect_inbox` takes a mailbox off every campaign. Ordered mailboxes keep being billed until their bundle is cancelled.
- `argorant_set_inbox_domain_renewal` stops or turns back on a domain's yearly renewal. Nothing is charged now, and the domain keeps working until its expiry date.
- `argorant_cancel_inbox_bundle` cancels a bundle of ordered mailboxes. Billing stops now with no refund, and the mailboxes work until the paid period ends. Ask why, using one of the reasons the tool lists, and only the workspace owner can cancel.

## What good output looks like

- One clear path for the user's situation, not every option at once.
- Prices in a short table before any order.
- A payment link or a connect link to click, never a request for a secret.
