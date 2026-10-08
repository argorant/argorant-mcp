---
name: cold-email-copywriting
description: Write cold emails and 3-step sequences that get replies, in Argorant's format. Short, peer-level, specific, plain text, one clear ask, no fluff or apologies, lowercase internal-style subject lines, a different angle per step, heavy spintax {a|b} so no two sends match, merge fields with fallbacks {{var|fallback}}, never placeholders, A/B variants and a review checklist, with examples for several industries. Use when the user wants a cold email, a sequence, follow-ups, subject lines, better copy, a rewrite, A/B variants or a copy review.
---

# Cold email copywriting

A cold email works when the reader thinks "this person understands my situation and has something worth 15 minutes". It reads like a short note from a capable peer, not like marketing. This skill writes the copy, renders it as one contact will read it, and saves it with `argorant_set_campaign_emails` only when the user is happy.

## Ground rules

- Saving copy sends nothing. A launch sends real emails, so it needs the user's explicit yes in this chat, asked as "Launch it now?". "Looks good" about a draft is not that yes.
- Write final text only. Never leave placeholders such as [link], [Name], <company>, {link}, TBD or XX. If a detail is missing, ask the user or leave it out.
- Never invent customers, numbers, results, awards or claims. Use only what the user or their website states.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## Before writing, get five facts

Ask in one message for whatever is missing. Who the reader is (role, company type), the problem they have in their own words, what the user offers and the result it brings, one piece of proof (a customer type, a number, a case), and the ask (a call next week is the default). If there is a website, read it first and ask less.

## The rules of a good cold email

1. **Short.** 50 to 90 words for the first email, 30 to 60 for follow-ups. Three or four short paragraphs with a blank line between them, never one block.
2. **About them first.** Open with their situation, not with who you are. "We are a leading provider" never appears.
3. **Specific.** One concrete problem, one concrete result, one proof. Numbers only when the user gave them.
4. **Peer tone.** Confident and calm, like a colleague who knows the field. Never needy, never apologetic, no flattery.
5. **One ask.** One question that is easy to answer with yes, phrased like a person would say it, such as "Worth a look next week?".
6. **Plain text.** No images, no bold, no bullet lists, no tracking style. No links in the first email unless the user asks for one.
7. **Natural prose.** Write like a person typing on a phone. No headers, no `Label: text` lines, no colons that introduce lists. End on the ask or a short sign-off, never on a dangling one-line sweetener.
8. **Varied.** Every sentence gets spintax variants so no two sends are identical.

## Do and don't

| Don't | Do instead |
| --- | --- |
| "Hope this finds you well." | Start with their situation. "Most contractors your size still match supplier invoices by hand." |
| "Just checking in on my last email." | Bring a new reason. "One more thought on month end, since it came up with another firm this week." |
| "Sorry to bother you again." | No apology. Say the new point and ask. |
| "Would love to hop on a quick call!" | "Worth a short call next week?" |
| "No worries if not!" | Leave it out. End on the ask. |
| "Quick question" as a subject | "next week" or "invoices at {{company_normalized\|your firm}}" in lowercase |
| "We are the leading AI-powered platform for..." | "We built software that matches invoices to jobs on its own." |
| "Our solution helps businesses increase efficiency." | "Office managers close the month in an afternoon instead of three days." |
| A wall of text in one paragraph | Two or three short paragraphs with blank lines between them |
| "Book a time here [link]" | "Open to a call next week?" and no link in the first email |
| "Hi {{first_name}}" without a fallback | "{Hi\|Hey} {{first_name\|there}}," |
| "Thanks, and have a great day!" after the ask | End on the ask, then the sign-off |

Apologise only for a concrete factual error, such as a wrong name in the last email.

## Subject lines

- 1 to 4 words, lowercase, like an internal note between colleagues. Examples are "next week", "month end", "supplier invoices", "{{company_normalized|your team}} and invoices".
- Never "quick question", "following up", clickbait, emojis, ALL CAPS, fake "Re:" or "Fwd:" on a first email.
- Follow-ups stay in the same thread by default, so their subject is "Re:" plus the first subject. Leave their subject empty.
- Spin the subject too, for example {next week|month end}.

## Spintax and merge fields

Two different things, never mixed up.

- **Spintax** uses single braces and picks one option for each email, for example {Hi|Hey|Hello}. Options can nest. The same contact always sees the same pick for a step.
- **Merge fields** use double braces and insert contact data, for example {{first_name}}, {{last_name}}, {{company}}, {{company_normalized}}, {{title}} and the campaign's own {{custom_...}} lines. {{company_normalized}} is the name people say, so prefer it. {{sender_first_name}} inserts the sending mailbox's first name.
- **Fallbacks.** A contact without a value waits at that email instead of getting a blank. Add one fallback after a | sign when the email should still go out, for example {{first_name|there}} or {{company_normalized|your team}}. One fallback only, plain words, up to 80 characters. {{last_name|}} sends nothing in its place on purpose.
- A merge field can sit inside a spintax option, but then every option must read correctly with the real value and with the fallback.

Heavy spintax means every sentence has two to four interchangeable versions that say the same thing in different words. Keep each option the same meaning and the same length, so no variant is weaker.

## Grammar traps to check in every rendering

Render each email twice in your head, once with real values and once with every fallback. Check these.

- **a or an.** "a {{title|leader}}" breaks for "an Operations Manager". Rewrite so no article sits before a merge field.
- **Plurals and verbs.** "{{company_normalized|your team}} is" reads well, "{{company_normalized|your team}} are" does not for most names. Prefer sentences where the name is not the subject.
- **Possessives.** "{{company_normalized|your team}}'s" becomes "your team's", fine, but a name that ends in s, such as Atlas, turns into "Atlas's" and a name with "Inc" into "Acme Inc's". Avoid possessives on merge fields.
- **Capitals.** A fallback at the start of a sentence needs a capital, mid-sentence it needs none. Place fallbacks mid-sentence.
- **Spintax next to merge fields.** "{Hi|Hey} {{first_name|there}}," gives "Hey there," which works. "{Dear|Hi} {{first_name|there}}" gives "Dear there", which does not. Every option must work with the fallback.
- **Repeated words** across options and the next sentence, such as two sentences that both start with "We".

## A 3-step sequence with different angles

Each step needs its own reason to talk, never the same pitch reworded.

| Step | Day | Angle | Length |
| --- | --- | --- | --- |
| 1 | 0 | The problem they likely have, the result, one proof, one ask | 50 to 90 words |
| 2 | 3 | A new angle, such as a short customer story, a number, or a cost of doing nothing | 30 to 60 words |
| 3 | 4 to 5 after step 2 | A different door, such as the right person to talk to, a smaller first step, or a timing question | 20 to 40 words |

Example for bookkeeping software selling to owners of construction firms with 11 to 50 people.

```
Email 1
subject: {month end|supplier invoices}

{Hi|Hey} {{first_name|there}},

{Most|A lot of} {contractors|construction firms} {your size|with a team like yours} {still match|still check} supplier invoices against jobs {by hand|in spreadsheets}, and {month end|closing the month} {takes days|eats most of a week}.

{We built|We make} bookkeeping software that {does that matching on its own|matches every invoice to the right job automatically}. {Office managers|The people doing the books} {close the month in an afternoon|are done with month end in hours}.

{Worth a look next week?|Open to a short call next week?}

{{sender_first_name}}
```

```
Email 2, 3 days later, same thread
{Hi|Hey} {{first_name|there}},

{One more thought|A second angle}. {A roofing company with 30 people|A 30-person roofing firm} {found|caught} {two duplicate supplier payments|two invoices it had paid twice} in {its first month|the first month} with us.

{If that sounds familiar|If double payments ever slip through at {{company_normalized|your firm}}}, {a 15-minute call|15 minutes} {next week|one day next week} {would show you how|is enough to show how}.

{{sender_first_name}}
```

```
Email 3, 4 days later, same thread
{Hi|Hey} {{first_name|there}},

{Is the bookkeeping something you handle yourself|Do you look after the books yourself}, or {is there someone in the office|should I talk to someone else on your team} {I should speak to|who owns this}?

{{sender_first_name}}
```

The roofing story is only allowed because the user gave it. Without a real story, use a cost of doing nothing instead.

## First emails for other industries

```
IT services selling to law firms, managing partners, 10 to 50 lawyers
subject: {after hours|client files}

{Hi|Hello} {{first_name|there}},

{Firms your size|Law firms with 10 to 50 lawyers} {usually|often} {have one person|rely on one person} who {keeps the IT running|fixes laptops and backups} {next to their real job|on the side}.

{We take that off their desk|We run IT for firms like that}, {with a fixed monthly fee|for one fixed fee a month}, and {answer within the hour|pick up within an hour}, {also after hours|evenings included}.

{Worth a short call next week?|Open to 15 minutes next week?}

{{sender_first_name}}
```

```
Performance agency selling to e-commerce brands, founders, 11 to 50 people
subject: {paid social|ad costs}

{Hi|Hey} {{first_name|there}},

{Most|Many} {brands|online shops} {your size|at your stage} {see ad costs climb|watch cost per order rise} {once they pass the first few hundred orders a month|after the first growth phase}.

{We fix that for|We work with} {apparel and beauty brands|direct to consumer brands}, {mostly by|usually by} {rebuilding the creative testing|testing new creative every week}, not by {raising budgets|spending more}.

{Worth a look next week?|Open to a short call next week?}

{{sender_first_name}}
```

```
Freight forwarder selling to manufacturers, heads of logistics, DACH
subject: {shipments to the US|overseas freight}

{Hi|Hello} {{first_name|there}},

{Since the last rate changes|With rates moving every month}, {many manufacturers|a lot of manufacturers} {ship to the US|send goods overseas} {on whatever rate they got last year|without comparing routes}.

{We book sea and air freight|We handle sea and air freight} for {machine builders|industrial companies} in {Germany, Austria and Switzerland|the DACH region}, {with one contact person|with a single contact} {for every shipment|from pickup to delivery}.

{Worth comparing on your next shipment?|Open to comparing on your next shipment?}

{{sender_first_name}}
```

```
Recruiting firm selling to software companies, heads of engineering, 51 to 200 people
subject: {senior hires|backend roles}

{Hi|Hey} {{first_name|there}},

{Senior backend roles|Senior engineering roles} {at companies your size|at teams of 50 to 200} {often stay open|usually stay open} {for three months or more|well past a quarter}.

{We only recruit engineers|We place only engineers}, {and send|sending} {three vetted people|a shortlist of three} {within two weeks|in the first two weeks}, {paid only when someone starts|with no fee unless someone starts}.

{Any roles like that open right now?|Hiring for anything like that this quarter?}

{{sender_first_name}}
```

Every number and claim in these examples stands for facts the user must supply. Replace them with the user's real facts, or cut the sentence.

## A/B variants

Each email in `argorant_set_campaign_emails` can carry variants, a list of up to 9 extra versions as {label, subject, body}. Contacts are spread evenly across the main text and its variants. The results per variant are on the campaign's page in the Argorant app.

- Test one thing at a time, such as two angles for email 1 or two subject lines. Spintax is for variety, variants are for learning.
- Two variants are enough. Each needs about 200 contacted people before you judge it.
- Name variants by what differs, such as "angle cost" and "angle speed".

## Save and check

1. Show each email rendered for one real contact, then once with every fallback, before saving.
2. Save with `argorant_set_campaign_emails`. The first email needs a subject. Follow-ups take delay_days and same_thread, which is true by default.
3. Read the result's warnings and fix every one with another call. Allow text to go out as written with allow_placeholders=true only when the user clearly wants that.
4. Call `argorant_get_campaign` and tell the user how many contacts would wait at an email because a merge field has no value (variable_coverage).
5. Offer the copy-reviewer agent for an independent check before launch.

## Review checklist

Go through every line before saving. Each answer must be yes.

1. Subject is 1 to 4 lowercase words, not "quick question", not clickbait, follow-ups thread as "Re:".
2. The first sentence is about the reader, not the sender.
3. One problem, one result, one proof, all from facts the user gave.
4. One ask, phrased like a person, easy to say yes to.
5. First email 50 to 90 words, follow-ups 30 to 60, short paragraphs with blank lines.
6. No "hope this finds you well", "just checking in", "sorry to bother", "would love to", "no worries", "quick question", no apology.
7. No placeholders, no links in the first email unless asked, plain text only.
8. Every merge field has a fallback, or the user accepts that contacts without the value wait.
9. Spintax uses single braces, merge fields double braces, and every option reads correctly with real values and with fallbacks.
10. No a or an before a merge field, no possessive on a merge field, no grammar break in any rendering.
11. Each step has its own angle.
12. No `Label: text` lines, no headers, no dangling sweetener line after the ask.
