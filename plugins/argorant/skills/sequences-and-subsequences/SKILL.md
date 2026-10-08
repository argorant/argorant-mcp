---
name: sequences-and-subsequences
description: Plan follow-up timing and structure for Argorant campaigns, keep follow-ups in the same thread, stop on reply, and set up keyword-triggered subsequences that send a different set of emails when a reply mentions something like pricing, later or a colleague, including how negations are handled. Use when the user asks how many follow-ups to send, when to send them, wants a branch when someone replies with a keyword, wants follow-ups to stop or continue after a reply, or wants to change the steps of a running campaign.
---

# Sequences and subsequences

The main sequence reaches people who have not answered. Subsequences catch people who answered with a clear signal and give them the right next email automatically. Real conversations still go to the reply inbox, where a person answers.

## Ground rules

- Saving steps sends nothing. A launch sends real emails and needs the user's explicit yes in this chat.
- A running campaign refuses copy with placeholders unless the user clearly wants the text sent as written.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## The main sequence

- **Steps.** 3 emails is the default, 4 at most for cold outreach. More steps rarely add replies and raise complaints.
- **Timing.** delay_days counts from the email before. A good default is day 0, day 3, day 7 or 8. For senior buyers or long sales cycles, 0, 4, 10.
- **Same thread.** Follow-ups stay in the same thread by default, with "Re:" before the first subject. Leave their subject empty. Start a new thread (same_thread=false with its own subject) only for a deliberate fresh start, such as a fourth email two weeks later.
- **Angles.** Each step brings a new reason to talk. See the cold-email-copywriting skill.
- **Stop on reply** is on by default, so any reply ends that person's emails. Keep it on. With stop_on_reply=false emails keep going unless the reply starts a subsequence or asks to stop, which only makes sense for automatic replies the user wants to ignore.

Save the steps with `argorant_set_campaign_emails` as [{subject, body}, {body, delay_days 3}, {body, delay_days 4}]. The whole sequence is replaced on every call, so always send all steps.

## Subsequences

A subsequence is a set of 1 to 8 follow-up emails that starts when a reply contains a keyword. A campaign can have up to 5. When a reply matches, that person leaves the main emails and gets the first matching subsequence, in the same thread.

How matching works.

- A keyword also counts in capitals, as a plural, with a small typo or inside a short sentence. "interested" matches "Interested!", "intrested" and "very interested", but never "interesting".
- A keyword after "not" or "no" never counts. "not interested" does not start the "interested" branch, and "no meeting" does not start a "meeting" branch.
- Replies asking to stop never start one. Quoted text from earlier emails is ignored.
- The order of the list decides which subsequence wins when several match. Put the most specific first.
- The first email goes out delay_days after the reply, where 0 means the next sending window. Its subject is `Re: {{thread_subject}}` unless you set one.

Save with `argorant_set_campaign_subsequences` as [{name, keywords [..], emails [{body, delay_days}]}]. An empty list removes them all. `argorant_get_campaign` shows the current ones.

## Subsequences that work

| Name | Keywords | What it sends |
| --- | --- | --- |
| Later | later, next quarter, next month, after the summer, busy right now | One short email 30 to 45 days later that picks the thread back up with a new reason |
| Pricing | pricing, price, cost, how much | Only when the user has a public price or a clear range. A short answer and a call to fit it. Otherwise leave this to a person |
| Wrong person | not the right person, wrong person, colleague, someone else | A thank you and a question about who owns the topic. A person still checks these in the inbox |
| Info | more info, send details, deck, brochure | A short summary in plain text and one question. No attachment, no link unless the user gives one |

Keep positive replies ("yes", "interested", "let's talk") with a person in the reply inbox. A booked meeting needs a human answer, not an automatic one.

Example.

```
[
  {"name": "Later",
   "keywords": ["later", "next quarter", "next month", "busy right now"],
   "emails": [{"body": "{Hi|Hey} {{first_name|there}},\n\n{You mentioned|You said} the timing was better {around now|about now}, so {picking this back up|coming back to this}.\n\n{Still worth a short call?|Worth 15 minutes next week?}\n\n{{sender_first_name}}", "delay_days": 40}]}
]
```

## Changing a running campaign

- New copy applies to emails not yet sent. People who already got a step are not sent it again.
- Removing a step drops it for everyone who has not reached it.
- To pause while editing, use `argorant_launch_campaign` with action=pause after a yes, and launch again after a new yes.

## What good output looks like

- The sequence as a short table (step, day, angle) before the full text.
- Each subsequence with its keywords, what it sends and one example reply that would trigger it, plus one that would not.
