---
description: Add a fact-based personal line for every contact in a campaign, 5 examples first, fallback for the rest
argument-hint: "[campaign name, and what the line should say]"
---

Use the personalization-at-scale skill. The request is $ARGUMENTS

If no campaign is named, list the campaigns with argorant_list_campaigns and ask which one.

Agree the variable with the user (name, instruction, fallback and the sentence it goes into) and save it with argorant_set_campaign_personalization. Research the first contacts from the facts in argorant_campaign_personalization_status, the company website and argorant_company_people, and use the lead-researcher agent for thin or important ones. Never invent a fact. Show 5 example lines inside their sentences with the fact and source, and wait for a yes. Then save in batches of up to 200 with argorant_set_lead_custom_fields, using keep_fallback when the facts are thin, and report the progress after each batch. This sends nothing and costs no credits.
