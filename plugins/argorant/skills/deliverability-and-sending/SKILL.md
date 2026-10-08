---
name: deliverability-and-sending
description: Keep Argorant campaigns landing in the inbox. Covers mailbox capacity and daily limits, the gap between emails, sending windows and time zones, warm-up as the user's own choice, bounce protection and auto-pause, valid-only leads, the blocklist, and what to do when bounces or replies drop. Use when the user asks how much they can send, sets daily limits or sending times, asks about warm-up, spam, bounces, a paused campaign, mailbox health, or wants to send more.
---

# Deliverability and sending

Good deliverability comes from a few habits. Low volume per mailbox, clean lists with valid addresses only, plain short emails, steady pacing, and a fast stop when bounces rise. Argorant has safe defaults for all of these, and this skill explains when to keep them and when to change them.

## Ground rules

- Change mailbox or campaign settings only after the user's yes. A launch, a restart after auto-pause and any order of mailboxes each need their own explicit yes in this chat.
- Show the full price before any mailbox order and order only after a clear yes. Mailboxes are paid through a payment link the user opens.
- Never ask for a mailbox password, card details or any other secret in the chat.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## Capacity

- Plan with 5 cold emails per mailbox per day. New mailboxes from Argorant are sized for that. `argorant_list_inboxes` shows every connected mailbox with its health and its own daily limit.
- Never use the user's main company domain for cold email at volume. New mailboxes on separate domains protect it. The get-mailboxes skill quotes and orders them.
- New mailboxes wait about 24 hours after setup before they send.
- Capacity math. Emails a day = mailboxes x 5. With 3 steps, new contacts a day is about a third of that. For 300 new contacts a day with 3 steps you need about 900 emails a day, so about 180 mailboxes.

## Campaign settings

Change them with `argorant_update_campaign`, passing only the settings that change.

| Setting | Default | When to change |
| --- | --- | --- |
| daily_limit | 100 per campaign | Raise it to match mailboxes x 5 when the campaign has many mailboxes |
| per_mailbox_daily_limit | not set, each mailbox keeps its own limit | Set it to cap every mailbox in this campaign, such as 5 |
| gap_minutes_min and gap_minutes_max | 60 and 120 | Keep for Microsoft mailboxes. A random gap looks human |
| window_start and window_end | 09:00 to 17:00 | Morning starts such as 08:00 suit most B2B readers |
| timezone_mode | fixed | Use lead so each person gets the email in their own working hours |
| skip_weekends | on | Keep on for B2B |
| stop_on_reply | on | Keep on |
| auto_pause | on | Keep on |
| auto_pause_bounce_rate_pct | 10 | Lower to 5 for a careful start on a new list |
| auto_pause_min_sent | 100 | People contacted before the bounce rule applies |
| auto_pause_when_offline | on | Pauses when mailboxes go offline. auto_pause_offline_share_pct sets the share, 100 means all of them |
| include_unsubscribe | off | Turn on when the user's rules or the countries they send to call for an opt-out line |

Campaigns always send plain text. A paused campaign starts again only when a person launches it, so after an auto-pause find the cause first.

## Warm-up

Warm-up is the user's own choice and is never part of a mailbox order, so never offer, sell or price it. If the user asks for it, `argorant_update_inbox` with the mailbox address and settings `{"warmup": true}` turns it on after their yes, and `{"warmup": false}` turns it off. Warm-up sends at most 10 emails a day per mailbox and starts only after the mailbox's first 24 hours.

## Clean lists

- Add valid addresses only. When `argorant_add_campaign_leads` answers needs_choice, ask "Add only the N valid addresses (recommended)?". Catch-all, unknown and risky addresses bounce more often, and bounces hurt the sender's reputation.
- For the user's own lists, check them first with `argorant_quote_verification` and `argorant_start_verification`, after showing the price. Only valid means confirmed.
- Use `argorant_block` for anyone who asks not to be contacted and for domains that must never be emailed, after a yes. Matching people stop getting emails at once. `argorant_blocklist` shows the list.

## Copy that helps delivery

- Plain text, short, no images, no attachments, no link in the first email, no link shorteners.
- Heavy spintax so no two emails are identical.
- No spam phrases such as "free", "guarantee", "act now", "100%", "risk-free", and no ALL CAPS.
- Every merge field has a fallback or the user accepts that contacts without the value wait.

## When something goes wrong

| Sign | Likely cause | What to do |
| --- | --- | --- |
| Bounce rate above 2 to 3 percent | Addresses that are not valid, or an old list | Pause after a yes, add only valid addresses, check the user's own rows first |
| Campaign paused by itself | Bounce rule or mailboxes offline | Read `argorant_get_campaign` and `argorant_list_inboxes`, fix the cause, then ask before launching again |
| A mailbox shows poor health | Too much volume or many bounces | Lower its limit or pause it with `argorant_update_inbox` active=false after a yes, or take it off the campaign with `argorant_remove_campaign_sender` |
| Sends but almost no replies | Copy, list or delivery | See the campaign-analytics-and-optimization skill |
| Many unsubscribes or angry replies | Wrong audience or too many steps | Tighten the list, cut to 3 steps, block those who asked |

## What good output looks like

- The capacity math in one or two lines with the user's numbers.
- Only the settings that change, each with a one-line reason.
- A clear yes question before anything is changed, launched or ordered.
