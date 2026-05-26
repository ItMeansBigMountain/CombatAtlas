# journal-ai Development Plan

Last updated: 2026-05-26

## Current role

Plan-only/static review shell needing focused MVP.

## Portfolio priority

Medium

## Detected context

- Classification: Plan/spec folder with static review shell
- Detected stack: Product direction
- Current tracked URL: https://journal-ai-sooty.vercel.app
- Tracker note: Add production settings, health checks, hosted DB/env separation; Convert shell into focused MVP with one high-friction user outcome; Privacy-first onboarding, gentle prompts, local/demo mode before accounts

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`

## Development phases

1. Pick one concrete user outcome.
2. Build a no-login static Vercel MVP with seed/demo data.
3. Add one interactive flow and clear CTA.
4. After review, add accounts/payments/API integrations only if needed.

## Vercel / hosting plan

Use existing static Vercel shell; replace placeholder content with real MVP flow.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
