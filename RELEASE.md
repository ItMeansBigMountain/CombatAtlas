# CombatAtlas release and rollback

## Environments

- Pull requests: `.github/workflows/combatatlas-ci.yml` runs isolated web and Expo checks. Build artifacts are retained for 14 days.
- Production web: `.github/workflows/combatatlas-deploy.yml` deploys `projects/CombatAtlas` to the protected `combatatlas-production` GitHub Environment.
- Mobile preview: `.github/workflows/combatatlas-eas-preview.yml` is manual and uses the `preview` EAS profile. It queues internal iOS/Android builds only after `EXPO_TOKEN` is configured in the `combatatlas-preview` GitHub Environment.
- Mobile production: intentionally not automated. Store signing, receipt verification, production ad IDs, and review gates must be completed first.

Never copy credentials into workflow YAML. Vercel credentials are scoped as GitHub Environment secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID`. Expo uses only `EXPO_TOKEN` in the preview environment.

## Release

1. Require the `CombatAtlas CI` web and mobile jobs on pull requests.
2. Merge to `main`; the production workflow rebuilds from the lockfile, deploys a prebuilt Vercel artifact, and smoke-tests the returned URL.
3. Confirm the canonical alias externally: `curl --fail --location https://combatatlas-flame.vercel.app/`.
4. For an internal mobile preview, configure `EXPO_TOKEN` and the Expo project ID once, then dispatch `CombatAtlas EAS preview` with `ios`, `android`, or `all`. Copy the EAS install link from the workflow log to testers.

Current production deployment (2026-08-25):

- Canonical alias: https://combatatlas-flame.vercel.app
- Immutable deployment: https://combatatlas-5q5vngrjt-itmeansbigmountains-projects.vercel.app
- Vercel deployment status: Ready
- External probe: currently HTTP 404 because account-level Vercel deployment protection still gates the project. The workflow smoke test intentionally fails until the alias is public.

Current public remediation preview (2026-08-25):

- Commit: `459776158951a31179873ab0da0830c03b8fefcb`
- Temporary URL: https://temporary-quick-platinum-11g8xnv.vercel.app
- Vercel deployment ID: `dpl_5WeyCstT4wVquRwTfrWrBHFy7V7s`
- Vercel deployment status: Ready; anonymous preview expires at 2026-08-25 22:42 UTC unless claimed.
- External verification: HTTP 200; Playwright loaded the CombatAtlas UI, searched for `armbar`, opened `Armbar from Guard Chain`, and confirmed four practice steps plus its demonstration link.
- Rollback: no production alias was changed. Let the temporary deployment expire; the canonical production deployment remains untouched.

## Current mobile support boundary

Local Expo exports are verified for web, iOS, and Android. These exports are JavaScript bundles, not signed installable applications, and native device launch has not been verified. Until EAS credentials and project configuration are available:

1. iPhone testing is development-only through Expo Go: `cd projects/CombatAtlas/mobile && npm ci && npm start -- --tunnel`, then scan the QR with the iPhone Camera app.
2. Android is source/export-only; there is no APK, AAB, Play internal-testing URL, or verified native launch.
3. Do not describe either platform as a signed preview, App Store, or Play build until EAS returns install URLs and testers verify launch.


## Rollback

1. In Vercel, open the `combatatlas` project deployment list and select the last known-good Ready deployment.
2. Use **Promote to Production** to move both production aliases back atomically, or run `vercel promote <known-good-deployment-url> --token "$VERCEL_TOKEN"` from a secured operator shell.
3. Verify the canonical alias externally and exercise search plus a drill detail route.
4. Revert the bad Git commit in a new commit; do not rewrite `main` history. The normal CI/CD path redeploys the reverted state.

For mobile previews, revoke or expire the internal build from EAS and queue a new preview from the last known-good commit. Production store rollback remains a store-console operation and is outside this preview workflow.
