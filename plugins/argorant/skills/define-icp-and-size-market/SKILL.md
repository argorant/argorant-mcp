---
name: define-icp-and-size-market
description: Turn a website or a one-line offer into ideal customer profile hypotheses, count each segment with Argorant for free, compare them by size and fit, and pick the best 2 or 3 to target first. Use when the user asks who to sell to, wants an ICP, asks which market or segment to start with, gives a website and asks who would buy, or wants to size a market before building a list.
---

# Define the ICP and size the market

The goal is a short ranked list of 2 or 3 segments the user can build lists and campaigns for today, each with a real count from Argorant and a clear reason why that buyer needs the offer now. Counting and previewing are free, so test several hypotheses instead of guessing one.

## Ground rules

- Counting, previewing and saving cost nothing. Say so, so the user explores freely.
- Never spend credits, send, buy or delete anything in this skill. Revealing contacts and launching are separate steps that show the price or the text and wait for a yes.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. Say credits and daily limits. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.
- Separate what you know from what you assume. A segment is a hypothesis until the count and the preview back it up, and until replies prove it.

## Step 1. Understand the offer

Work from what the user gives you.

- **A website.** If you can browse, read the home page, the pricing page, case studies and the customer logos. If you cannot browse, `argorant_enrich` with the company domain alone returns the company profile for free. Ask the user to fill gaps.
- **A one-line offer.** Ask at most three short questions, all in one message. Who bought it so far, what problem it solves in their words, and what a typical deal is worth.

Write down, in one or two lines each, the problem solved, the result a buyer gets, the proof the user has (customers, numbers, a case) and the price level. Use only what the user or the website states.

## Step 2. Write 4 to 6 segment hypotheses

A segment is one buyer role at one kind of company in one place. For each, fill this frame.

| Part | What to decide | Filters it becomes |
| --- | --- | --- |
| Company type | Industry, or company keywords, or "sells to" a group | industry, keywords with keyword_scope, company_category with sells_to |
| Size | Company size band | employee_range such as 11-50 or 51-200 |
| Place | Countries or regions | country such as DACH, Nordics, North America, state, city |
| Buyer | The person who feels the problem and can say yes | title with title_match, seniority, departments |
| Trigger | Why now | Used in the copy, not as a filter |
| Out | Who looks similar but never buys | exclude_title, exclude_industry, exclude_keywords, exclude_company_domain |

Good hypotheses differ on one axis at a time, so the comparison teaches something. For example, the same buyer in two company sizes, or two buyer roles at the same companies.

Example for an offer "bookkeeping software for construction firms".

1. Owners and founders at construction companies with 11 to 50 people in the US.
2. Finance managers and controllers at construction companies with 51 to 200 people in the US.
3. Owners of trades businesses (electrical, plumbing, HVAC) with 1 to 10 people in Texas and Florida.
4. Office managers at general contractors in Canada.
5. Accounting firms that sell to construction, as a partner channel.

## Step 3. Count every hypothesis

Call `argorant_count_people` once per segment with its filters. Read back the number and the industry_note, which says how a plain word such as "construction" was understood. The number counts people, not companies.

- Use title_match=words (the default) for normal roles. Use exact when a title like "Owner" must not match "Product Owner". Use contains only for special cases.
- Use keywords for niches that are not an industry, such as "freight forwarding" or "dental lab". keyword_scope=company looks at company tags and descriptions (the default), people looks at people's skills, any looks at both.
- For companies that sell to a group, set company_category and sells_to, for example company_category=software and sells_to=restaurants. This returns the companies that sell, never their customers.
- `argorant_company_people` with one known good customer's domain shows which roles exist there. Use it to check which title the buyer really has.

## Step 4. Preview to check fit

Call `argorant_preview_people` with limit 10 for each segment that has a usable count. Look at the rows (initials, job, company, place) and mark false positives, such as recruiters, students, consultants, freelancers, or the wrong industry. Add excludes and count again until at least 8 of 10 rows are people the user would gladly email.

## Step 5. Score and pick 2 or 3

Show one table with one line per segment and score each from 1 to 5.

| Segment | People | Fit (pain and budget) | Reachability (clear title, has email) | Proof the user has | Score |
| --- | --- | --- | --- | --- | --- |

Decision rules.

- Size. A segment below about 300 people is a good test but not a campaign on its own. Above about 50,000, narrow it by size, place or a keyword before building a list.
- Fit beats size. A smaller segment where the user already has a customer and a case usually replies better than a big vague one.
- Prefer segments where one role clearly owns the problem. Committees are slow.
- Pick 2 or 3 that differ, so the first campaigns teach which one works. Say why each was picked in one line.

## Step 6. Hand off

Offer the next step for the chosen segments.

- Save each as a list with the advanced-list-building skill ("Save these 3 segments as lists? Saving is free.").
- Write the first sequence per segment with the cold-email-copywriting skill, using the trigger you wrote down as the angle.

## What good output looks like

- One sentence on what the offer is and who it helps.
- A ranked table of 4 to 6 segments with real counts and a one-line reason each.
- A clear pick of 2 or 3 and one question to move on, such as "Save these as lists?"
