---
name: campaign-analytics-and-optimization
description: Read Argorant campaign results, judge reply, positive and bounce rates, find what holds a campaign back (list, copy, offer or delivery) and change one thing at a time with A/B variants. Use when the user asks how a campaign is doing, why replies are low, what to change, which variant wins, whether to scale up, or wants a weekly review of their campaigns.
---

# Campaign analytics and optimization

Numbers only help when they lead to one clear change. This skill reads the results, says which part of the campaign is the weak link, and proposes one change with a way to measure it.

## Ground rules

- Reading results changes nothing and costs nothing.
- Changing copy, settings or lists needs the user's yes. Pausing, stopping or launching needs an explicit yes in this chat.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.
- Do not judge too early. Below about 200 contacted people, say the numbers are early and give a direction, not a verdict.

## Step 1. Collect the numbers

1. `argorant_list_campaigns` gives every campaign with status, people, sends and replies.
2. `argorant_campaign_analytics` with campaign_id and days (30 by default) gives the day-by-day sends, replies, positive replies, bounces and unsubscribes, plus totals and the reply and bounce rates per person contacted.
3. `argorant_get_campaign` shows the copy, the mailboxes and anything that blocks sending.
4. `argorant_inbox` with campaign_id and folder=interested, replies or not_interested shows what people actually said. Read 10 to 20 replies, because their words explain the numbers.
5. `argorant_list_campaign_leads` with status=held shows contacts waiting because a merge field has no value.

## Step 2. Read the numbers

Rates are per person contacted. Use these rules of thumb for cold B2B email, and say they are rules of thumb.

| Measure | Healthy | Needs work | Act now |
| --- | --- | --- | --- |
| Bounce rate | below 2 percent | 2 to 5 percent | above 5 percent |
| Reply rate | above 3 percent | 1 to 3 percent | below 1 percent after 300 contacted |
| Positive share of replies | above 30 percent | 15 to 30 percent | below 15 percent |
| Unsubscribe rate | below 1 percent | 1 to 2 percent | above 2 percent |

## Step 3. Find the weak link

| What you see | Likely weak link | First change |
| --- | --- | --- |
| High bounces | The list | Add only valid addresses, check the user's own rows, see the deliverability-and-sending skill |
| Few replies of any kind, low bounces | Delivery or the first email | Check mailbox health and limits, then rewrite email 1 with a sharper problem and a new subject |
| Replies, but mostly "not interested" | The list or the offer | Tighten the filters to the buyers who did say yes, or change the angle |
| Many "wrong person" replies | The titles | Change title, title_match or seniority in the list |
| Many "send more info" and few meetings | The ask | Make the ask smaller and more concrete |
| Most replies come after email 2 or 3 | Email 1 is weak | Move the best angle to email 1 |
| Many contacts held | Merge fields without fallbacks | Add fallbacks or remove the field |

Look at who replied positively. Their titles, company sizes and industries show where to aim the next list. `argorant_inbox_thread` opens each conversation.

## Step 4. Change one thing and measure

- Change one thing at a time, so the result teaches something.
- For copy, use A/B variants. Each email in `argorant_set_campaign_emails` can carry variants as {label, subject, body}, and contacts are spread evenly across them. The results per variant are on the campaign's page in the Argorant app.
- Give each variant about 200 contacted people before you judge it. Call a winner only when the gap is clear, such as 4 percent against 2 percent, not 2.4 against 2.1.
- Keep the winner as the main text and test the next idea against it.
- For a list change, grow or build a new list with the advanced-list-building skill, and add only the new people.

## Step 5. Scale what works

When reply rate and positive share are healthy over 300 or more people, scale in this order.

1. Add the rest of the same search to the same list and to the campaign.
2. Add mailboxes, keeping 5 emails per mailbox per day, with the get-mailboxes skill.
3. Clone the winning copy for the next best segment from the define-icp-and-size-market skill.

## What good output looks like

- One line per campaign with contacted, reply rate, positive replies and bounce rate.
- The weak link named in one sentence with the evidence.
- One proposed change, how it will be measured, and a yes question.
