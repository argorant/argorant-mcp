---
description: Write a 3-step cold email sequence with spintax and safe fallbacks, reviewed before anything is saved or launched
argument-hint: "[campaign name or audience, and what you offer]"
---

Use the cold-email-copywriting skill, and the sequences-and-subsequences skill for timing. The request is $ARGUMENTS

If the audience, the offer, a piece of proof or the ask is missing, ask for all of it in one short message, or read the user's website first if they gave one.

Write a 3-step sequence with a different angle per step, lowercase subject lines, heavy spintax in every sentence and a fallback on every merge field such as {{first_name|there}}. Never write placeholders or invent facts. Show each email rendered for one example contact and once with every fallback. Then run the copy-reviewer agent and apply its fixes. Save the emails to a campaign with argorant_set_campaign_emails only after the user's yes to the text. Never launch in this command. Launching needs a separate explicit yes to "Launch it now?".
