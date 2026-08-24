# Cross-Platform Consumer Application Audit — 2026-08-24

Source of truth: [`CROSS_PLATFORM_APP_STANDARD.md`](CROSS_PLATFORM_APP_STANDARD.md)

## Scope and completion rule

The active product portfolio is defined by non-terminal Kanban work for consumer-facing products. Seven active consumer applications were found. None currently satisfies the release definition of done: a production web build and deployment, an iOS production build verified through TestFlight (or approved equivalent), and an Android App Bundle verified through an internal testing track, with simulator/emulator and physical-device smoke evidence.

A web deployment, responsive browser test, legacy Expo scaffold, or planned mobile shell is not evidence that iOS and Android release gates pass.

## Portfolio matrix

| Product | Current implementation | Required architecture decision | Principal platform gaps | Migration card |
|---|---|---|---|---|
| Wornly | Mature Next.js 16/React 19 web marketplace; PostgreSQL/Neon; Stripe Checkout/Connect; deployed web | Preserve the mature Next.js commerce/admin/backend and add an Expo Router native client. Extract typed domain, validation, API, auth-session, and design-token packages; do not move server commerce logic into clients. | No Expo workspace, native builds, EAS config, bundle IDs, native secure storage, app/universal links, push/background adapters, store metadata, TestFlight/internal-track evidence. Next.js/DOM/Tailwind and server-only Stripe/Neon code are web-only. Native payments must use an explicitly reviewed Stripe/platform-policy boundary; Stripe secrets/webhooks remain server-only. | `t_d0e291f9` |
| tweetBetweenTheLines | Research/product-direction documents only; no package manifest or client implementation | Start with the default Expo Router universal architecture and typed shared packages. | Entire web/iOS/Android client, EAS/store setup, OAuth PKCE redirect scheme and universal/app links, native token vault, archive/document picker and upload adapter, background import/sync status, notifications, privacy manifests, consent/export/delete and release evidence are absent. Browser cookie/token behavior must be separated from Keychain/Keystore. | `t_40bb4353` |
| Journal AI | Deployed Vite/TypeScript browser MVP in `frontend/journal-app`; no React/Expo dependencies; browser-local behavior | Replace/migrate the thin MVP into an Expo Router universal app while retaining the existing backend/transcription prior art behind typed contracts. | Vite/browser implementation is web-only. Missing native audio/recording permissions and consent UI, secure storage, deep links, offline persistence adapter, upload/background transcription handling, notifications, safe areas, EAS/store metadata, TestFlight/internal-track and physical-device evidence. | `t_173ca3b5` |
| MusicAI | Flask/templates/static-JS web application with server OAuth/token and analysis integrations; Playwright smoke package only | Preserve Flask as platform-neutral API/backend; build an Expo Router universal client and extract typed provider/auth/analysis contracts. | Templates and browser JS are web-only. Missing mobile PKCE/deep-link handoff, Keychain/Keystore session storage, provider app-link/playback adapters, offline cache, notifications/background refresh policy, EAS/store configuration and all native release evidence. Provider tokens and Watson/Genius credentials must stay server-side. | `t_177edb51` |
| BurnoutBoyz | Product-direction documents only; Honda Tech Upgrade is prior art, not the target app | Start with Expo Router universal architecture plus typed vehicle, maintenance, provenance, auth, validation, and API packages. | Entire implementation and release infrastructure absent. Requires camera/document upload adapters, secure VIN/receipt/token storage, connected-car OAuth PKCE/deep links, push reminders and background recall refresh policy, offline garage cache, permissions/privacy disclosures, EAS/store setup and three-target evidence. | `t_ceec824c` |
| Consumer Advocate | README-only scaffold; implementation not started | Start with Expo Router universal architecture and typed evidence/document/privacy packages. | Entire implementation and release infrastructure absent. Requires browser and native document/photo picker adapters, secure auth/storage, deep links, push/background processing status, accessibility, privacy/export/delete, EAS/store setup and three-target evidence. | `t_53c5396a` |
| Algorithm Academy | README/product-direction scaffold; implementation not started. Legacy Codology Expo 49 code is prior art, not evidence for this target. | Start with Expo Router universal architecture. Isolate the secure browser coding sandbox/editor behind a `.web` adapter and provide a native-friendly exercise/editor adapter; share curricula, progress, auth, API and validation contracts. | Entire implementation and release infrastructure absent. Legacy Expo 49 is outdated and lacks Expo Router/release evidence. Requires role-safe auth and secure storage, deep links, notifications, offline reading/progress queue, sandbox isolation, EAS/store setup and three-target evidence. | `t_a9d5db3e` |

## Mandatory acceptance gates on every migration card

Each listed card must remain incomplete until its own repository contains or links to verifiable evidence for all of the following:

1. Architecture: Expo Router universal app, or the documented Wornly/MusicAI shared-core split; typed API/auth/domain/validation contracts; platform-specific adapters kept narrow.
2. Web: production build, mobile/desktop browser smoke, OAuth/deep-link callback test, deployed URL, monitoring and rollback evidence.
3. iOS: EAS/native production build, simulator and physical-device smoke, Keychain and permissions checks, universal links, notifications/background behavior, privacy manifest and store assets, TestFlight verification.
4. Android: EAS/native AAB, emulator and physical-device smoke, Keystore and permissions checks, app links, notifications/background behavior, Data Safety and store assets, internal testing track verification.
5. Shared quality: unit/integration/contract/E2E tests; accessibility; responsive safe-area behavior; offline/slow/retry/expired-session states; consent/export/delete; no packaged secrets.
6. Capability adapters where applicable: uploads/camera/audio, OAuth, secure storage, push, background work and payments must each have web/iOS/Android behavior documented and tested.

## Explicit exceptions and exclusions

These are not consumer applications under this standard and must not be given fictional mobile release gates:

- RuneLite plugins, including Clan War Board, Who's Grinding and BIS Loadouts: desktop plugin artifacts. Their backend/service or informational web surfaces do not turn the plugin itself into an iOS/Android app. Any future separate companion app is in scope.
- Backend APIs/services, MCP servers, infrastructure, CLIs, cron jobs, data pipelines and internal automation: non-app artifacts.
- YouTube/faceless-content automation and operator dashboards used only as internal automation: non-app artifacts unless deliberately launched as a consumer product.
- Cox Elementary PTA: client website; treat as web-only only with the contractual exception recorded on its project/card. A future general-audience PTA mobile product would be in scope.
- Demonstrations, archived/legacy source, `_vercel_mvp*` snapshots, `_tmp`, `legacy-src`, templates and learning exercises: prior art, not active consumer releases. Re-activating one as a product puts it back in scope.

## Audit conclusion

All seven active consumer products already have a dedicated cross-platform migration/delivery card. The cards are the correct units of implementation work; duplicate migration cards were not created. This audit adds the architecture decision and missing adapter/release evidence to each card. Portfolio-level completion remains blocked until every applicable card has independently verified web, iOS and Android gates.