# tweetBetweenTheLines Production Architecture

> Mission: **Free the minds of the consumer with data.**

## Decision

Build a new TypeScript/Expo universal product and preserve the Python/Django/Tweepy code as source-history and algorithm prior art. Do not continue the old Python app as the production surface.

The production product should be a privacy-first personal data liberation app: users connect official accounts or import official platform archives, choose which sources/categories may be analyzed, and receive explainable, source-backed profile cards they can export, revoke, or delete.

## Prior-art audit

| Source | Useful history to preserve | Production decision |
| --- | --- | --- |
| `ItMeansBigMountain/tweetBetweenTheLines` / local Python scripts | Historical tweet timeline retrieval, keyword search, word scoring, trend lookup, TextBlob polarity/subjectivity experiments, simple graph/dashboard concepts. | Keep as `legacy-src`/audit reference only. Rewrite ingestion and analysis because the code is interactive, script-oriented, depends on old Tweepy patterns, and contains hardcoded legacy Twitter credentials that must not be reused. |
| `tweetDeleter` Django experiment | Early web dashboard/navigation idea for login + dashboard. | Preserve UX idea only; do not build production on the Django app. It lacks the consent/source ledger, token vault, deletion lineage, and universal mobile/web target. |
| `social-media-analysis` | Personal Presence Intelligence framing, archive import path, normalized social schema, safety copy around no diagnosis, local/free vs paid LLM tier ideas. | Fold into this product direction. `tweetBetweenTheLines` is now the active product name/surface, with `social-media-analysis` serving as research source material. |
| `watsonAI` | IBM Watson NLU adapter pattern: entities, keywords, categories, concepts, emotion, sentiment, syntax; compatibility shim for older tone output. | Keep as optional analysis adapter. Production must use provider-neutral interfaces and store model/provider/version provenance for every generated card. |
| `MusicAI` | One-account/multi-provider connection model, provider registry, least-privilege OAuth scopes, PKCE/state helpers, encrypted token store, provider status rows, analysis cache keyed by input hash/analyzer version. | Reuse patterns for social connectors: provider registry, OAuth state/PKCE, encrypted token vault, provider identities, durable cache. Do not couple MusicAI and this app directly yet. |
| `Journal AI` | Reflection cards, signal lexicons, gentle next-step language, no-diagnosis boundary, user-reviewed insight flow, cited/provenance-aware meeting intelligence direction. | Reuse insight style: deterministic features first, LLM interpretation second, evidence and uncertainty on every claim, user review before sensitive derived insights become durable. |
| `_vercel_mvp_safe/tweetbetweenthelines` | Minimal Vite deployment shell. | Archive only; it has no source app beyond built output/package metadata and should not drive production architecture. |

## Build vs rewrite map

### Build new

- TypeScript monorepo with workspaces:
  - `apps/mobile`: Expo Router universal app for iOS, Android, and web.
  - `packages/domain`: deterministic, UI-independent personal-event normalization and profile snapshot logic.
  - Future `packages/connectors`: source registry, OAuth/archive import contracts.
  - Future `packages/security`: token vault, consent receipts, delete/export workflows.
- Normalized event schema:
  - `source`, `sourceRecordId`, `occurredAt`, `kind`, `text`, `metadata`.
  - Provenance and deletion lineage are first-class fields.
  - Derived features are deterministic before any model/LLM narrative.
- Profile cards:
  - `attention`, `language`, `wellbeing-pattern`, and `provenance` cards in the first slice.
  - Every card includes confidence and evidence items.
  - Wellbeing language must remain non-diagnostic.

### Reuse by translation, not copy-paste

- Python keyword search -> TypeScript deterministic keyword/topic extraction.
- TextBlob polarity/subjectivity idea -> provider-neutral `SignalAdapter` later; the first slice uses transparent lexicons.
- Twitter trend lookup -> future public-trend connector; never require user credentials for global trend browsing.
- Watson NLU -> optional adapter with explicit model/provider/version provenance.
- MusicAI encrypted token storage -> social token vault design.
- Journal AI signal cards -> profile/reflection card copy and safety boundaries.

### Retire or quarantine

- Any hardcoded Twitter/X credentials in legacy files. Treat them as compromised historical secrets and rotate/revoke outside this repo if still active.
- Interactive `input()` scripts as product code.
- Old direct Tweepy scraping/timeline assumptions that do not match current official access restrictions.
- Claims that infer diagnosis from social-media behavior.

## Production architecture

1. Identity and consent
   - User signs in with passkey or trusted OAuth.
   - Each source creates a consent receipt: scopes/import category, timestamp, policy version, revocation state.
   - Scope ledger is visible to the user.

2. Source acquisition
   - Official OAuth/API where allowed.
   - Official user archive import for restricted platforms.
   - Manual/user-provided import where official history APIs are unavailable.
   - Every connector declares coverage honestly: `official-api`, `official-archive`, `manual-import`, `restricted`, or `unsupported`.

3. Storage boundary
   - Encrypted token vault is separate from analytics prompts.
   - Raw imports are separate from normalized events.
   - Derived features/cards include source lineage and can be reprocessed or deleted by source.

4. Analysis pipeline
   - Validate imports for file type, size, zip bombs, schema, and malware risk.
   - Normalize to personal events.
   - Extract deterministic features: keywords, signal counts, rhythms, source stats.
   - Generate profile cards with evidence, confidence, model/provider version, and uncertainty.
   - Optional LLM/NLU adapters must not see tokens and must cite aggregate evidence/source spans.

5. User control
   - Source-specific revoke.
   - Export raw + normalized + derived profile data.
   - Complete deletion and cryptographic deletion workflow.
   - Rebuild snapshots after revocation; revoked sources must disappear from evidence.

6. Safety and review gates
   - No diagnosis from social behavior.
   - Validated self-report screening stays separate from observational signals.
   - Legal/privacy/health-claim review before public health-related claims.
   - Bias, multilingual, security, and red-team review before broad launch.

## Implemented first slice

This card established a tested TypeScript domain slice:

- `packages/domain/src/index.ts`
  - `normalizePersonalEvent(input)` creates deterministic event ids, provenance, deletion lineage, keywords, word counts, and signal counts.
  - `buildProfileSnapshot(inputs, options)` filters revoked sources, emits mission-bound profile snapshots, and creates evidence-backed cards without diagnosis language.
- `packages/domain/tests/profileSnapshot.test.ts`
  - Verifies provenance/feature extraction.
  - Verifies non-diagnostic profile cards.
  - Verifies revocation removes source evidence and preserves deletion lineage.
- `packages/domain/src/safetyPolicy.ts` and `packages/domain/tests/safetyPolicy.test.ts`
  - Encode per-tenant/per-source consent receipts, token/raw/feature/model-payload separation, ordered descendant deletion, non-diagnostic insight-release gates, model provenance, and multilingual cohort thresholds.
- `PRIVACY_SAFETY_ARCHITECTURE.md`
  - Defines the production threat/privacy model, tenant enforcement, archive sandbox, revocation/export/delete lineage, explainability, bias evaluation, and professional/legal/clinical launch gates.
- `apps/mobile/app/index.tsx`
  - Expo Router universal starter screen wired to the domain package with sample cards.

## Next implementation slices

1. Connector registry and coverage matrix for Google/YouTube, Meta, X, TikTok, Reddit, LinkedIn, Snapchat, Discord, Bluesky, Pinterest, Tumblr, Twitch, Spotify/media.
2. X/Twitter official archive parser behind the normalized event schema.
3. Consent receipt and source revocation domain tests.
4. Encrypted token-vault package modeled after MusicAI but generalized for all providers.
5. Import sandbox tests for malformed JSON/CSV/ZIP cases.
6. Profile card UI components for evidence drill-down, confidence, export, revoke, and delete.
