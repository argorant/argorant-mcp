---
name: account-and-credits
description: Check the Argorant account, credits and daily limits, buy a credit pack through a payment link, see past credit purchases, and set up webhooks that notify another app. Use when the user asks how many credits are left, what something will cost, whether they can afford a reveal or export, wants more credits, or wants Argorant to notify a URL when a reply arrives or an export is ready.
---

# Account and credits

Credits pay for revealing contact details, finding emails, exports, list checks and adding new people to a campaign. Searching, counting, previewing and saving lists are free.

## Ground rules

- Buy credits only after the user's explicit yes in this chat to one quoted pack and price.
- You never open, fill in or pay a payment page. Through Claude, buying always returns a payment link that the user opens and pays. A saved card is never charged from the chat.
- Never ask for card details, a password or any other secret in the chat.
- Daily limits are safety limits. They cost nothing and are not credits, so never call them credits.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## Check the account

Call `argorant_account` and tell the user, in one or two sentences, their plan, the credits left and how much of today's limits is used. When the user asks whether they can afford something, compare the credits left with the most that step can cost.

## Buy credits

1. `argorant_credit_packs` lists the one-time packs and their prices. Pack credits stay valid for 365 days.
2. When the user picks a pack, call `argorant_quote_credits`. Nothing is bought by this call.
3. Show the pack, the price, the currency and that it is paid through a payment link. Ask "Buy this pack?" and wait for a clear yes.
4. Call `argorant_buy_credits` with confirmed=true and the user's own words of approval in user_confirmation. Give the user the payment link. The credits are added once the payment went through.
5. `argorant_credit_purchases` shows past purchases and whether their credits were added.
6. Never retry with a new quote to get around a refusal or a limit.

## Webhooks

- `argorant_webhooks` lists the URLs Argorant notifies and every event the user can pick, such as reply.received or export.ready.
- `argorant_create_webhook` adds one after a yes. It needs the Pro plan. The signing secret is shown once, so tell the user to store it safely.
- `argorant_test_webhook` sends one test event. `argorant_delete_webhook` removes a webhook after a yes.

## What good output looks like

- The credit balance in one sentence, with the cost of the next step next to it.
- One clear payment link when the user wants to buy, never a card form in the chat.
