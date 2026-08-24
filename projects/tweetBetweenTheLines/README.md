# tweetBetweenTheLines

> **Free the minds of the consumer with data.**

A privacy-first personal data liberation platform. Users connect supported accounts through official OAuth or import official account archives, choose what may be analyzed, and receive an explainable personal profile covering interests, language, attention, behavior, personality reflection, and non-diagnostic wellbeing signals.

## Current state

Historical prior art exists in `ItMeansBigMountain/tweetBetweenTheLines`; the modern production rebuild is now active as a TypeScript/Expo universal product. See:

- [`PRODUCT_DIRECTION.md`](PRODUCT_DIRECTION.md)
- [`PRODUCT_ARCHITECTURE.md`](PRODUCT_ARCHITECTURE.md)
- [`PRIVACY_SAFETY_ARCHITECTURE.md`](PRIVACY_SAFETY_ARCHITECTURE.md) — production threat/privacy model, consent and deletion lineage, archive sandbox, explainability, bias evaluation, and clinical-safety gates
- [`PLATFORM_OAUTH_ARCHIVE_MATRIX.md`](PLATFORM_OAUTH_ARCHIVE_MATRIX.md) — official-source OAuth/API and archive-import coverage decisions for the connector registry
- [`OPERATIONS_RUNBOOK.md`](OPERATIONS_RUNBOOK.md) — observability, backups/restore, incident response, cost controls, privacy requests, and closed-beta operations gates
- [`CLOSED_BETA_DEPLOYMENT_PLAN.md`](CLOSED_BETA_DEPLOYMENT_PLAN.md) — Git-based deployment flow, consented/synthetic E2E fixture policy, and per-platform release evidence ledger

## Current implementation slice

- `packages/domain` contains the tested, UI-independent personal-event normalization and profile snapshot domain.
- `packages/domain/src/safetyPolicy.ts` provides executable fail-closed contracts for consent receipts, separated processing planes, deletion lineage, insight-release gates, model provenance, and multilingual cohort readiness.
- `packages/domain/src/personalityWellbeing.ts` keeps licensed, reviewed self-report trait scoring separate from observational language reflections; unsupported locales abstain and all wellbeing output remains explicitly non-diagnostic with professional and emergency-help guidance.
- `packages/domain/src/operations.ts` provides executable production readiness, closed-beta participant, and cost-control gates that fail closed when deployment/operations evidence is missing.
- `apps/mobile` is the Expo Router universal client for iOS, Android, and web. It now includes explicit consent, honest source coverage, OAuth/deep-link handoff copy, official archive picking and validation, import progress, explainable evidence drill-down, corrections, per-source revocation, export/delete controls, crisis-resource UX, platform-specific token-storage disclosures, and an operations/beta-readiness panel that labels blocked release evidence honestly.
- Native session references use Keychain/Keystore through `expo-secure-store`; provider tokens remain server-side. Web access tokens must be delivered only through server-managed secure HttpOnly cookies and are never persisted by the client.
- Legacy Python/Django/Tweepy scripts remain source-history/prior-art only and must not be reused with their historical credentials.

## Local verification

```text
npm test
npm run typecheck -w @tweet-between-the-lines/mobile
npx expo export --platform web
npx expo export --platform ios --output-dir dist-ios
npx expo export --platform android --output-dir dist-android
npm audit --omit=dev --json
```

The three export commands verify JavaScript bundles, not signed store releases. Production web deployment, physical-device runs, TestFlight, Android internal-track verification, OAuth provider credentials, and server job/token endpoints remain release gates and must not be represented as complete until evidence exists.

## Non-negotiable boundaries

- User-owned data and user-controlled consent
- Official APIs/exports; no credential scraping
- Least-privilege OAuth and source-specific revocation
- Explainable metrics with provenance and uncertainty
- Export and complete deletion
- No mental-health diagnosis from social-media activity
- Validated self-report screening kept separate from observational signals
- Security, privacy, bias, multilingual, legal, and clinical review before public health-related claims

## Planned platform coverage

The connector registry will investigate Google/YouTube, Meta platforms, X, TikTok, Reddit, LinkedIn, Snapchat, Discord, Bluesky, Pinterest, Tumblr, Twitch, Spotify, and other material sources. Coverage will be labeled honestly as official API, official archive import, manual import, restricted, or unsupported.
