---
name: get-contacts
description: Get work emails and phone numbers for B2B prospects with Argorant, with the price shown first. Use when the user wants to reveal or unlock contact details from a search, find one person's work email from their name and company website, find emails for a spreadsheet of names, look up a person or company, export a list as a CSV file, or check whether the email addresses on their own list work.
---

# Get contact details

Argorant returns work emails that work, and phone numbers where available, for the people the user picks. Only emails that work are charged. People this account already unlocked are free again.

## Ground rules

- Before anything that spends credits, say what it costs and the most it can cost, then wait for a clear yes. Repeat this for every new spend, not once per chat.
- Never buy, send or delete anything without the user's explicit yes in this chat.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. Say credits and daily limits, never internal terms. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.
- `argorant_account` shows the credits left. Check it before a large spend and say whether the account has enough.

## Current prices

The tools state the price in every answer, and their numbers win over this list.

- Revealing a person costs 1 credit when their work email is new to this account and works. Nothing is charged for people without a working email or people already unlocked.
- Phone numbers are only included when the user asks for them. Each phone number returned costs 10 credits, nothing when none is found, and phones need the Pro plan or higher.
- Finding one email from a name and company website costs 1 credit when an email is found, also when the company accepts every address and the best guess is returned unconfirmed, and 0.25 credits when nothing is found.
- Exporting costs 1 credit for each person with a working email. People exported before are skipped unless the user wants them again.
- Checking the user's own email list costs half a credit per new address. Addresses checked recently are free.

## Reveal people from a search

1. Run the search from the build-target-list skill first, so the user has seen the count and a preview.
2. Say how many people you will reveal and the most it can cost, for example "Reveal 10 people? Up to 10 credits, plus 10 credits per phone number if you want phones."
3. After the yes, call `argorant_reveal_people` with the same filters and a limit. Show name, job, company and email in a short table, then pass on the result's summary of what it cost.
4. A daily safety limit caps reveals. It costs nothing. If it is reached, say so and offer an export or a saved list instead.

## Find a specific person's email

- For one named person at one company, use `argorant_find_email` with first name, last name and company domain, after telling the user the price. Never repeat a lookup that came back not_found, and never loop it over many people.
- When the status is catch_all, the company's mail server accepts every address, so the email is Argorant's best guess and unconfirmed. Say that clearly.
- For more than 5 people, use `argorant_find_emails`. Tell the user how many people there are, the price per result and the most it can cost, and ask them to approve a spending limit. Pass it as max_credits. Check progress with `argorant_find_emails_status` about every 30 seconds and show results with include_results=true. If the job pauses at the spending limit, ask before raising it with `argorant_manage_find_emails`. Cancelling there stops further charges.
- `argorant_enrich` looks up one person by email, or by name plus company domain, or a company by domain alone. A person lookup costs 1 credit when the email is new and works. A company lookup is free. A name finds the closest match, so check the result before relying on it.

## Export a CSV file

1. For a search, use `argorant_create_export`. For a saved list, use `argorant_export_list`. Searches with exclusions, special title matching or range filters export up to 50,000 people at a time, so save larger ones as a list and export the list.
2. Before starting, say the most it can cost and whether phones are included, and wait for a yes. Asking twice can start a second export, so call it once.
3. Follow it with `argorant_export_status`, or `argorant_export_batch_status` when the export was split into several files. Offer email_when_done so Argorant emails the user when the file is ready.
4. `argorant_download_export_preview` shows the first part of a finished file as text. The full file is downloaded in the Argorant app.

## Check the user's own email list

1. Call `argorant_quote_verification` with up to 1,000 addresses. It checks nothing and spends nothing.
2. Show the counts and the most it can cost, and ask for a yes.
3. Call `argorant_start_verification` with that quote and the approved number as approved_maximum_charge. Argorant never charges more than that.
4. Follow it with `argorant_verification_status`. Only valid means an address was confirmed to work. Unknown, risky and catch-all do not mean that. The full results and a CSV file are in the Argorant app at the link the result gives.

## What good output looks like

- The price before the action, the actual cost after it.
- Contacts in a compact table. Unconfirmed emails are marked as unconfirmed.
- No raw JSON and no internal field names.
