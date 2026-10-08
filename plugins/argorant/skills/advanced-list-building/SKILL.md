---
name: advanced-list-building
description: Build precise, clean B2B lead lists with Argorant using include and exclude on every filter, title matching (whole words, exact, contains), keyword scope (company tags or people's skills), companies that sell to a group, regions, saved searches versus fixed lists, growing one list with the rest, dedupe, preview checks for false positives, valid-only hygiene and list size planning against mailbox capacity. Use when the user wants a better or bigger list, wants to leave people out, gets wrong people in a preview, asks how many contacts they need, or wants to add more people to an existing list or campaign.
---

# Advanced list building

A good list is narrow enough that every person on it would recognise the problem, and big enough to keep the mailboxes busy for the campaign's length. This skill gets there with free counts and previews before any credit is spent.

## Ground rules

- Counting, previewing and saving lists are free. Revealing, exporting and adding new people to a campaign cost credits, so say the most it can cost and wait for a yes before those.
- Never send, buy, delete or change anything without the user's explicit yes in this chat.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. Say credits and daily limits. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## The filters

Every list filter takes several values with commas, meaning any of them, and has an exclude twin. Include and exclude work together, also on the same kind of filter.

| Filter | Include | Exclude | Notes |
| --- | --- | --- | --- |
| Job title | title | exclude_title | CFO also finds Chief Financial Officer. title_match and exclude_title_match say how a title matches |
| Seniority | seniority | exclude_seniority | Owner, Founder, Partner, C-Level, VP, Director, Manager, Senior, Entry, Intern |
| Department | departments | exclude_departments | Sales, Marketing, Engineering, Product, Finance, Human Resources, Operations, Legal, Customer Success, IT, Design, Data, Research, Executive |
| Industry | industry | exclude_industry | Broad sectors. Plain words are matched to Argorant's industries, and industry_note says how |
| Company keywords | keywords | exclude_keywords | Niches and tags. keyword_scope says where to look |
| Place | country, state, city | exclude_country, exclude_state, exclude_city | country takes regions such as Europe, EMEA, DACH, Nordics, Benelux, APAC, LATAM, North America, GCC |
| Company | company_domain | exclude_company_domain | Use exclude_company_domain for current customers, partners and competitors |
| Company size | employee_range | none | 1-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10000+ |
| Who they sell to | company_category with sells_to | none | Returns the sellers, never their customers |

Revenue ranges, a place with a radius, estimated gender and estimated income exist too. One that is not ready yet is refused with a plain message, never ignored, so tell the user and continue without it.

## Title matching

- **words** (the default). Every word must appear as a whole word. "Data" does not match "Database". Right for almost every search.
- **exact.** The whole title must be one of the values, ignoring case. "CEO" does not match "Founder & CEO". Use it for short ambiguous titles such as Owner, Partner or President.
- **contains.** The text may appear anywhere, also inside a word. Slower. Use it for word stems such as "procure" to catch procurement and procuring.

Patterns that work.

- Owners of small firms without product people. title="Owner, Founder, Managing Director" with title_match=exact, plus exclude_title="Product Owner".
- Heads of a function without assistants. title="Head of Marketing, Marketing Director, VP Marketing", exclude_title="Assistant, Intern, Coordinator".
- When an exclude must match differently from the include, set exclude_title_match on its own.

## Keyword scope

- **company** (the default) looks at the company's tags, industry and description. Use it for what the company does, such as "freight forwarding" or "dental lab".
- **people** looks at people's skills and profile text. Use it for what the person does, such as "Salesforce" or "SAP".
- **any** looks at both, plus job title and company name. Widest, so check the preview carefully.

## Companies that sell to a group

Set company_category (software, payments, pos_payments, business_fintech, accounting_software, payroll_hr_software, formation, association, marketplace, investors) and sells_to (restaurants, construction, dentists, salons, auto_repair, hotels, logistics, trades, retailers, smb), or write it in q, for example "software companies selling to restaurants". This finds the sellers, never their customers. Such a search cannot yet be saved as a whole. Preview or reveal the people and save them with record_ids.

## Steps

1. **Count** with `argorant_count_people`. Read back the number and the industry_note.
2. **Preview** with `argorant_preview_people`, limit 10. Mark every row the user would not email and name why (wrong role, wrong industry, too small, a recruiter or consultant).
3. **Fix false positives** with the matching exclude, then count and preview again. Stop when at least 8 of 10 rows fit. Typical fixes are exclude_title="Recruiter, Talent, Consultant, Freelance, Student, Intern", exclude_industry="Staffing and Recruiting", or title_match=exact for short titles.
4. **Save** with `argorant_create_list`, passing the same filters you counted with and a clear name such as "US construction owners 11-50, Oct". Saving runs in the background. `argorant_list_status` says when it is ready and how many people it holds.
5. **Grow the same list.** For "add the rest" or a wider search, call `argorant_create_list` with the list_id of the existing list. People already in it are skipped. Never create a second list for the rest.
6. **Add to the campaign** with `argorant_add_campaign_leads` and that list_id, after saying the most it can cost. Adding the same list again later adds only the people not yet in the campaign.

## Saved search or fixed list

- **Saved search.** `argorant_create_list` with filters saves the whole search. Use it for an evergreen segment. `argorant_list_lists` with kind=saved_searches shows them.
- **Fixed list.** `argorant_create_list` with record_ids and only_these=true saves exactly the people chosen. Use it when the user picked people by hand or for a sells_to search. kind=lists shows them.
- `argorant_rename_list` renames, `argorant_delete_list` deletes for good after a clear yes.

## Dedupe and hygiene

- A list skips people already in it. A campaign skips people already in it, and the same person under two addresses joins once.
- Exports skip people exported before unless exclude_previously_exported is false. People already unlocked are free again.
- Leave out current customers, open deals and partners with exclude_company_domain. For people or domains that must never be contacted, use `argorant_block` after a yes. `argorant_blocklist` shows the list.
- Add valid addresses only. When `argorant_add_campaign_leads` answers needs_choice, ask "Add only the N valid addresses (recommended)?" Catch-all, unknown and risky addresses bounce more often, and bounces hurt the sender's reputation.
- One contact per company for small firms, two or three for larger ones with different roles. More than that from one company feels like spam. Narrow by title or seniority if the preview shows many people per company.

## Size the list to the mailboxes

Plan with 5 cold emails per mailbox per day, the volume Argorant sizes new mailboxes for. Connected mailboxes show their own daily limit in `argorant_list_inboxes`.

- Emails a day = mailboxes x 5.
- Each contact gets one email per step, so new contacts a day is about emails a day divided by the number of steps.
- Contacts needed for a month = new contacts a day x sending days (about 22 weekdays).

Example. 100 mailboxes send 500 emails a day. With a 3-email sequence that is about 165 new contacts a day, or about 3,600 a month on weekdays. A list of 1,000 would run dry in a week, and a list of 50,000 would take over a year, so build about 4,000 and grow the same list later.

Say these numbers to the user before saving, and suggest the get-mailboxes skill when the list needs more capacity than they have.

## What good output looks like

- The count first, then a 10-row preview with false positives marked and the fix applied.
- The final filters in one short line, so the user can reuse them.
- A size check against the mailboxes and one clear next step.
