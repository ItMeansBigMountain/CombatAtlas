# CombatAtlas release and rollback

## Environments

- Pull requests and manual dispatches: `.github/workflows/combatatlas-preview.yml` runs `npm test`, lint, and build, then creates and smoke-tests a Vercel preview.
- Production web: intentionally not automated. Promotion remains gated on Oyama's browser review and explicit approval of a preview.
- Mobile preview: local Expo export verification only. No EAS preview workflow or signed install link is currently configured.
- Mobile production: intentionally not automated. Store signing, receipt verification, production ad IDs, and review gates must be completed first.

Never copy credentials into workflow YAML. Vercel credentials are stored as GitHub repository secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID`.

## Release

1. Require the `CombatAtlas Preview` job on pull requests.
2. Open the workflow's Vercel preview URL and complete browser review. Do not promote it automatically.
3. After explicit production approval, promote the reviewed deployment and confirm the canonical alias externally: `curl --fail --location https://combatatlas-flame.vercel.app/`.
4. Mobile remains outside this web release path until an EAS preview workflow and signing prerequisites are configured.

Current production deployment (verified 2026-09-05; not changed by the preview workflow):

- Canonical alias: https://combatatlas-flame.vercel.app
- Immutable deployment: https://combatatlas-jt3jry0wo-itmeansbigmountains-projects.vercel.app
- Vercel deployment ID: `dpl_5MizirE9E4ubBcpmXL8BtiEFjVeX`
- Vercel deployment status: Ready
- External probe: HTTP 200 with title `CombatAtlas — Martial Arts Drill Database`.

Current verified CI preview (2026-09-05):

- Source commit: `e99119c2414744db89e7ca7053a998f35e5a9e5f`
- Workflow run: https://github.com/ItMeansBigMountain/CombatAtlas/actions/runs/33948067111
- Preview URL: https://combatatlas-cdz7crhhj-itmeansbigmountains-projects.vercel.app
- Vercel deployment ID: `dpl_6q6PfAHQh6MKuAxmY1QvMRqtL8bU`
- Verification: workflow passed; external HTTP 200; desktop 1440x900 and mobile 390x844 passed with no console errors, page errors, failed responses, or horizontal overflow.

Current public remediation preview (2026-08-25):

- Source commit: `c94856daa331084f332381735d1aff7fc148f632` (application remediation is in parent commit `459776158951a31179873ab0da0830c03b8fefcb`).
- Temporary URL: https://temporary-quick-peridot-4y06631.vercel.app
- Vercel deployment ID: `dpl_Gzw2RZCHU7nwvo3nBZcVjiNA1jUJ`
- Vercel deployment status: Ready; anonymous preview expires at 2026-08-25 23:26:05 UTC unless claimed.
- Deployment method: direct upload of the locally verified `dist` output. This deliberately allocated a new anonymous project/URL instead of reusing the stale `temporary-quick-platinum-11g8xnv` URL.
- External HTTP evidence: anonymous GET returned HTTP 200 `text/html`, title `CombatAtlas — Martial Arts Drill Database`, and `/assets/index-DmOkF31J.js` (not stale `/assets/index-BJT5b6Cu.js`).
- External Playwright evidence at 1440x900 and 390x844: Kendo showed only `Men Strike Footwork`; Historical European Martial Arts showed only `Longsword Zornhau Entry`; Brazilian Jiu-Jitsu showed exactly its three curated guides (`Armbar from Guard Chain`, `Triangle Choke Angle Cut`, `Rear Naked Choke Back Control`); Arnis/Kali/Eskrima showed only `Sinawali Double Stick Flow`; Fencing and Pencak Silat each showed zero options and the no-reviewed-guides message. Both viewports had zero console errors and `scrollWidth == clientWidth`.
- Local release verification: web `npm test`, `npm run lint`, and `npm run build` passed; mobile `npm test` passed 6/6, Expo Doctor passed 21/21, and web/iOS/Android Expo exports completed.
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
