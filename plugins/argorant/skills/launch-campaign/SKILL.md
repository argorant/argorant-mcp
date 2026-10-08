---
name: launch-campaign
description: Write, set up and launch a cold email campaign with Argorant, sent from the user's own mailboxes. Use when the user wants to create a campaign or sequence, write or fix the emails and follow-ups, add a personal first line for each contact, add leads from a list, choose sending mailboxes, launch, pause or stop a campaign, change sending settings, or see how a campaign is doing.
---

# Launch a campaign

Argorant runs the campaign from the user's own mailboxes. A campaign starts as a draft, and nothing is sent until the user clearly says launch.

## Ground rules

- A launch sends real emails to real people. Launch only after the user's explicit yes to launching this campaign, in this chat. "Looks good" about a draft is not a yes to launch. Ask "Launch it now?" and wait.
- Adding new people from Argorant to a campaign costs 1 credit per person, like a reveal. People already unlocked and the user's own rows are free. Say the most it can cost and wait for a yes.
- Never delete, stop or remove anything without a clear yes.
- Never ask for a password or any other secret in the chat. Mailboxes are connected with the get-mailboxes skill.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## Steps

1. **Start or reuse.** `argorant_list_campaigns` shows existing campaigns. To start a new one, call `argorant_create_campaign`. It is created as a draft with bounce protection and stop on reply switched on.
2. **Write the emails** with `argorant_set_campaign_emails`. The first email needs a subject. Each follow-up has delay_days and stays in the same thread by default. Keep emails short, plain and specific to what the user sells. Write final text only. Never leave placeholders such as [link], [Name], TBD or XX. If a detail is missing, ask the user or leave it out.
3. **Variables and fallbacks.** Double braces insert contact data, such as {{first_name}}, {{company_normalized}} and {{title}}. Prefer {{company_normalized}}, the short name people say. A contact without a value waits at that email instead of getting a blank, so add a fallback after a | sign when the email should still go out, for example {{company_normalized|your team}} or {{first_name|there}}.
4. **Spintax is different.** Single braces such as {Hi|Hello|Hey} pick one option at random for each email, to vary wording. Never mix the two up. {{company_normalized|your team}} is a fallback, {Hi|Hello} is spintax.
5. **Personal first lines (optional).** Call `argorant_set_campaign_personalization` with 1 to 5 {{custom_...}} variables, each with one instruction and one fallback that reads well for anyone. Then use `argorant_campaign_personalization_status` to get the next contacts and the facts Argorant has about each company. Write each line only from facts you looked up, never invent a detail, a number or a customer. Show the user 5 example lines inside their sentences and wait for a yes. Then save them with `argorant_set_lead_custom_fields`, up to 200 per call, and use keep_fallback for contacts without usable facts. Put the variable into the email text exactly as defined.
6. **Reply branches (optional).** `argorant_set_campaign_subsequences` starts a different set of follow-ups when a reply contains a keyword, such as "pricing" or "interested". A keyword after "not" or "no" never counts.
7. **Add the people** with `argorant_add_campaign_leads`, from a saved list_id or from rows the user gives. Say the most it can cost first. Call it without grades the first time. If the answer is needs_choice, ask "Add only the N valid addresses (recommended)?" and offer the other kinds with their counts. Catch-all, unknown and risky addresses bounce more often, and bounces hurt the sender's reputation. Then call again with the user's choice. To add more later, grow the SAME list and add it again.
8. **Choose the mailboxes.** `argorant_list_inboxes` shows what is connected. Set them with `argorant_set_campaign_senders`. If none are connected, switch to the get-mailboxes skill.
9. **Settings.** `argorant_update_campaign` changes the daily limit, sending window, timezone, weekends, the gap between emails, auto-pause on bounces and stop on reply. Keep the defaults unless the user asks.
10. **Check before launch.** Call `argorant_get_campaign`. Fix every copy warning with another `argorant_set_campaign_emails` call. Tell the user how many contacts would wait because a variable has no value. Then summarise in a few lines (emails, people, mailboxes, daily limit, first send window) and ask "Launch it now?"
11. **Launch** with `argorant_launch_campaign` and action=launch only after a clear yes. If the launch is refused, read out each problem it names and fix them. Use allow_placeholders=true only when the user clearly wants text sent exactly as written.
12. **Pause or stop.** action=pause holds the campaign, action=stop ends it for good. Ask before either.

## After launch

- `argorant_campaign_analytics` shows sends, replies, positive replies and bounces day by day.
- `argorant_list_campaign_leads` lists the people and their status. status=held shows who waits because a variable is empty.
- `argorant_remove_campaign_lead` takes one person out. `argorant_remove_campaign_sender` takes a mailbox off this campaign only.
- `argorant_delete_campaign` deletes a draft, paused or stopped campaign with its results. Ask first.
- Replies are handled in the work-reply-inbox skill.

## Deeper playbooks

For the copy itself use the cold-email-copywriting skill, for personal lines the personalization-at-scale skill, for follow-up timing and keyword branches the sequences-and-subsequences skill, for limits, pacing and bounces the deliverability-and-sending skill, and for results the campaign-analytics-and-optimization skill. Before asking "Launch it now?", offer the copy-reviewer agent for an independent check.

## What good output looks like

- The emails shown as the recipient will read them, with one example contact filled in.
- A short pre-launch summary and one clear question.
- No launch, deletion or spend without the user's yes.
