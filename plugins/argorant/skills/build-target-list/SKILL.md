---
name: build-target-list
description: Size a market and build a list of B2B buyers with Argorant. Use when the user describes who they sell to, asks how many people or companies fit (for example "how many heads of procurement at manufacturers in Germany"), wants to see example prospects, wants to find companies that sell to a group such as restaurants or dentists, asks who works at a company domain, or wants to save, grow, rename, delete or reuse a lead list.
---

# Build a target list

Argorant counts the market, shows example people with names hidden, and saves the whole search as a private lead list. Counting, previewing and saving are free and show no contact details, so the user sees the market before spending anything.

## Ground rules

- Counting, previewing and saving cost nothing. Say so, so the user feels free to explore.
- Revealing contact details, exporting and adding new people to a campaign cost credits. Those steps live in the get-contacts and launch-campaign skills, and each one shows the price and waits for a yes.
- Never send, buy, delete or change anything without the user's explicit yes in this chat.
- Never ask for a password or any other secret in the chat.
- Speak in plain words. Say credits and daily limits, never internal terms. If someone asks where the data comes from, point to https://argorant.com/privacy and do not guess or name sources.

## Steps

1. **Turn the request into filters.** Use title (several titles with commas match any of them, and short forms such as CFO work both ways), seniority, departments, industry for broad sectors, keywords for company tags, country (countries or regions such as DACH, Nordics, EMEA or North America), and company_domain. Every filter has an exclude twin, such as exclude_title, exclude_industry, exclude_country, exclude_seniority, exclude_departments, exclude_keywords and exclude_company_domain. Use them when the user says "but not" or "without".
2. **Companies that sell to a group.** When the user wants companies that serve restaurants, construction, dentists, salons, hotels, logistics, trades, retailers or small businesses, set company_category and sells_to, or write it in q, for example "software companies selling to restaurants". This returns the companies that sell, never their customers. Say that if the user seems to expect the customers.
3. **Count first** with `argorant_count_people`. Read back the number and the industry_note, which says how a plain word such as "logistics" was understood. The number counts people, not companies, and it is not a company's total staff.
4. **Preview** with `argorant_preview_people` to check that the search finds the right people. Show 5 to 10 rows as a short table (initials, job, company, place). If the rows look wrong, tighten the filters and count again. Prefer company_normalized, the short name people use, when you mention a company.
5. **One company.** For "who works at stripe.com", use `argorant_company_people`. It shows how many people Argorant has there, how many have a work email, and example roles with names hidden.
6. **Quick lookups.** `search` counts people for a domain or a few plain words, and `fetch` opens one of its results. For any search that combines job, place and company, use the count and preview tools instead.
7. **Save the list** with `argorant_create_list` when the user says "save them" or "make a list". Pass the same filters you counted with, so the whole search is saved, not just the rows shown. Only when the user clearly wants just the people on screen, pass their record_ids with only_these=true. Give the list a clear name.
8. **Wait for it to fill.** Saving runs in the background. Check with `argorant_list_status` and tell the user when it is ready and how many people it holds.
9. **Grow, never duplicate.** "Add more" or "add the rest" means the same search, or a wider one, into the SAME list_id. Never create a second list for it.
10. **Manage lists.** `argorant_list_lists` shows every saved list and saved search. `argorant_rename_list` renames one. `argorant_delete_list` deletes one for good, so ask first and pass confirmed=true only after a clear yes.

## Daily limits

Counts, previews and company lookups count toward daily safety limits. They cost nothing and reset every day. If one is reached, say so plainly and suggest continuing tomorrow or narrowing the search.

## What good output looks like

- A one-line answer with the count first ("About 4,200 marketing directors at US software companies").
- A small preview table, never a wall of raw fields.
- A clear next step, for example "Save this as a list?" or "Reveal 10 of them? That is up to 10 credits."
