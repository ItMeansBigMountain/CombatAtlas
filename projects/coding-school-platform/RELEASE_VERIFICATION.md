# Coding School Platform release verification

Last verified: 2026-08-25

## Scope

Algorithm Academy / Coding School Platform currently ships as:

- A dependency-free Python domain package in `coding_school/` for curriculum, demo accounts, evidence submission, teacher review, parent-safe progress, admin metrics, and portfolio iteration workflows.
- An Expo SDK 57 universal app in `app/` for web, iOS, and Android learner, teacher, and admin demo paths.

All learner data in this release is demo-only. Real student production data, billing, legal terms, public domains, Apple developer credentials, Google Play credentials, and store metadata require owner decisions/credentials before public launch.

## Verified commands

From `projects/coding-school-platform`:

```bash
python3 examples/linear_search.py
python3 examples/demo_workflow.py
python3 -m unittest discover -s tests -v
python3 -m compileall coding_school examples tests
```

From `projects/coding-school-platform/app`:

```bash
npm run typecheck
npm run build:web
npm run smoke:web
npm run build:android
npm run build:ios
npx expo-doctor
npm audit --audit-level=high
```

`npm run smoke:web` serves the current `app/dist/` web export on a local ephemeral port by default. Run it after `npm run build:web`, before native exports overwrite `dist/`. Override with `SMOKE_URL=<url> npm run smoke:web` to test a deployed web URL.

## Browser smoke coverage

The Playwright smoke test verifies:

- Mobile viewport: learner mission page loads.
- Secure coding preview iframe is sandboxed and script-free.
- Learner reflection can be saved as offline evidence.
- Teacher review queue shows the evidence and can approve mastery.
- Admin release console is reachable and shows demo-only operational gates.
- Desktop viewport preserves the approved learner progress count.
- No browser console/page errors occur during the smoke path.

## Cross-platform build coverage

Expo Metro exports pass for:

- Web static bundle in `app/dist/`.
- Android bundle export.
- iOS bundle export.

These prove the universal app compiles for all required targets. They are not signed store artifacts.

## Release blockers requiring owner credentials or decisions

- Production web domain and legal/privacy copy must be chosen before public traffic.
- Apple Developer account, bundle ID ownership, app privacy answers, screenshots, and TestFlight distribution are required for iOS release verification.
- Google Play Developer account, package name ownership, Data Safety answers, screenshots, and internal testing track are required for Android release verification.
- Real payments/billing are explicitly out of scope and must not be enabled without legal/payment choices.
- `npm audit --audit-level=high` passes with 0 high/critical findings, but Expo toolchain dependencies still report 10 moderate transitive `uuid` advisories where the offered fix is a breaking Expo downgrade.

## Rollback

The current web artifact is static. Roll back by redeploying the previous verified `app/dist/` build or reverting the release commit and rerunning `npm run build:web` before deployment.
