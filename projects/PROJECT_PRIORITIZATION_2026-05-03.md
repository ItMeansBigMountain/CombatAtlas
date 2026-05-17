# Project Prioritization Update

- **Date:** 2026-05-03
- **Principle:** prioritize modern use-case apps that can generate money; do not waste cycles on apps now solved by normal LLM chat.

## Decisions

| Project | Decision | Reason |
| --- | --- | --- |
| Addictive mobile games | Raise priority | Unity background + mobile ads = direct monetization path. Build iOS/Android. |
| Bitcoin Bike | Lower priority | Not primarily a code app; hardware/business feasibility, not current software MVP. |
| Consumer Advocate App | Needs clarification | Currently meant ?terms/privacy policy simplifier.? Could be LLM-chat-solvable unless differentiated. |
| Honda Tech Upgrade | Keep/modernize | Maps to HondaBoyz; replace hardcoded service values with VIN/maintenance APIs. |
| Rubber Headphone Adapter | Remove | User called it garbage; removed from project dir and queue. |
| Social Media Analysis | Raise priority | Strong modern paid AI use case: archive upload + behavioral/psychology report + Stripe. |
| TikTok Clone | Keep strategically | Large ambition; useful as a long-term platform bet, but MVP must be narrow. |

## LLM-solvable risk filter

Before building, every app should answer:

1. Can ChatGPT already do this from a pasted prompt?
2. Does the app add data ingestion, automation, saved history, payments, privacy, reports, or recurring workflow?
3. Can it produce revenue within 30-60 days?
4. Is there a distribution channel?

If answer #2 and #3 are weak, downgrade the project.

## Consumer Advocate App clarification

Current meaning in the queue:

> Upload/paste terms & conditions, privacy policies, contracts, or product claims and get a plain-English risk summary.

Why it may be weak now:

- A user can paste T&C into an LLM directly.
- Monetization is unclear unless we add browser extension monitoring, saved company risk profiles, class-action/refund workflows, or consumer complaint automation.

Recommendation: keep as **low/blocked** until Affan decides whether it has a unique angle.
