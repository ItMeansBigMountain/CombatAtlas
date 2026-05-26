# stockNews Development Plan

Last updated: 2026-05-26

## Current role

Unified stockNews + wutHappened portfolio-aware news intelligence.

## Portfolio priority

High

## Detected context

- Classification: Active merged portfolio news app
- Detected stack: Product direction
- Current tracked URL: https://stocknews-sentiment.vercel.app
- Tracker note: Primary project for stockNews + wutHappened: user imports portfolio by OAuth/CSV/JSON/manual/vendor exports, gets relevant news, sentiment, risks, catalysts, and daily reports.

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`

## Development phases

1. Unify portfolio import UX: manual list, CSV, JSON, vendor export, future OAuth.
2. Tie news relevance and sentiment to holdings.
3. Create daily report cards with risks/catalysts/plain-English explanations.
4. Add optional Watson NLU/free model enrichment behind fallback/local heuristic.

## Vercel / hosting plan

Frontend/API already deployed; verify anonymous frontend and API endpoints.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
