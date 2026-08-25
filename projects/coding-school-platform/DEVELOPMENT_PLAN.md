# coding-school-platform Development Plan

Last updated: 2026-05-26

## Current role

Coding school CRM + learning portal.

## Portfolio priority

High

## Detected context

- Classification: Coding-school CRM + learning portal
- Detected stack: Product direction
- Current tracked URL: https://coding-school-platform.vercel.app
- Tracker note: Queued CRM plan: functional parity with teacher schedule, student check-ins, AI Zoom-note tag extraction, progress graphs, parent dashboard, and Codology lesson linkage.

## Existing direction artifacts

- `CURRICULUM_SOURCE_OF_TRUTH.md`
- `CODERSCHOOL_CRM_RESEARCH_AND_PLAN.md`
- `PRODUCT_DIRECTION.md`
- `TEACHER_HIRING_LOCATION_PLAN.md`
- `docs/plans/2026-05-26-coding-school-crm.md`

## Development phases

1. Implement structured curriculum data from `CURRICULUM_SOURCE_OF_TRUTH.md`, with teacher mastery modules before student modules.
2. Implement teacher login and today schedule from demo seed data.
3. Add student after-class check-ins with curriculum tags, teacher-reviewed evidence, AI entitlement gating, and local tag parser.
4. Render accomplishment badges, progress graph from evidence/progress events, and parent weekly dashboard.
5. Connect Codology/Algorithm Academy lesson recommendations, starting with Basic 13 and Linear Search.

## Vercel / hosting plan

Keep Vercel demo public; first MVP should be no-real-student-data demo mode.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
