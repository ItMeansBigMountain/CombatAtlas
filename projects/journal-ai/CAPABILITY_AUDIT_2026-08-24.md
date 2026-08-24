# Journal AI capability audit — 2026-08-24

## Verdict

Journal AI is a working local demo, not a production-complete private journaling or AI service. The repository contains two disconnected clients plus an explicitly legacy Django API. The current code builds, the domain tests pass, and both documented Vercel URLs respond, but the live sites serve an older frontend bundle and do not contain the new mobile/privacy/meeting functionality.

## Evidence collected

- `frontend/journal-app`: `npm test` passed 4/4 test files; `npm run build` passed with TypeScript and Vite 8.2.2.
- `apps/mobile`: `npm run typecheck` passed; a fresh Expo web export completed with three static routes.
- Git: this project is a subdirectory of the HeRmEz monorepo on `main`; its only remote is `origin https://github.com/ItMeansBigMountain/HeRmEz.git`. The new mobile/domain/meeting work is staged or modified but not represented by a newer project commit than `df6d829a9`.
- Deployment: both `https://journal-ai-sooty.vercel.app` and `https://journal-app-five-delta.vercel.app` returned HTTP 200. Both served the same 7,988-byte `index-WSy9zez1.js`, which contains `Local-first demo` but does not contain `Private meeting capture`, `Delete permanently`, or `OAuth not configured`. This is not the current source build (`index-Dh3LuDCE.js`).

## Capability matrix and gaps

### Frontend/backend boundary

- The Vite app stores journal entries only in the in-memory `entries` array (`frontend/journal-app/src/main.ts:133`) and loses them on refresh.
- The Expo app stores journals, meetings, and mutation queues in device `AsyncStorage` (`apps/mobile/src/storage.ts:10-15`, `apps/mobile/app/index.tsx:31-40`). No code sends queued mutations to a backend; the queue only grows.
- No production backend exists outside `legacy-src`. The legacy Django code is explicitly imported for review (`legacy-src/persistent-gpt-api/IMPORT_NOTES.md`) and models chat sessions/messages, not the current journal, meeting, export, or deletion domain.
- There is no API contract, sync protocol, conflict handling, tenant boundary, database migration for journals, or server-side deletion/export implementation.

### Authentication and authorization

- Expo sign-in depends on an unset release variable and merely stores the entire successful callback URL as the session value (`apps/mobile/app/index.tsx:94-100`). It does not validate OAuth state/PKCE, parse and validate a token, refresh sessions, or bind data to an authenticated user.
- Web stores that callback URL in `AsyncStorage`; native uses SecureStore without biometric/user authentication (`apps/mobile/src/storage.ts:16-18`).
- Legacy Django is unsafe to activate as-is: chat list/create/detail/message routes do not require authentication and authorize using a caller-supplied `unique_identifier` query parameter (`legacy-src/persistent-gpt-api/core/views.py:68-212`). `custom_user_detail` requires authentication but does not restrict access to the current user (`views.py:40-61`).

### Persistence and privacy

- Expo journals are durable only at the local-device level. `AsyncStorage` is not encrypted storage for journal bodies or meeting metadata.
- The Vite meeting demo encrypts audio only in a process-memory map and generates a non-exportable key that is not retained (`frontend/journal-app/src/main.ts:239,252-257`); reload destroys both, so this is not durable encrypted storage.
- Expo records/imports a file but persists only a filename/job record. It neither encrypts nor deletes the actual recording URI after creating the job (`apps/mobile/app/index.tsx:56-85`). The UI claim `Encrypted locally` is therefore unsubstantiated for the Expo path (`index.tsx:118`).
- `deleteJournalEntry` blanks the body and retains a tombstone (`frontend/journal-app/src/journalDomain.ts:48-50`), while UI labels it `Delete permanently`. That can be a valid sync design, but permanent purge is not implemented because there is no sync/backend consumer.
- `eraseEverything` clears known app keys but has no confirmation, verification, operating-system backup policy, remote deletion, recording-file cleanup, or deletion receipt (`apps/mobile/app/index.tsx:102-105`).
- Export is domain text generation. Expo renders a selectable preview but provides no share/download action (`index.tsx:120`). Vite has no journal export/delete controls in its active UI.
- The legacy privacy response directly conflicts with the new privacy-first direction by claiming collected data is company property and may be sold (`legacy-src/persistent-gpt-api/core/views.py:236-247`). It must never be exposed as Journal AI policy.

### Model/provider and insight behavior

- There is no AI model or provider integration in either active client. `analyzeJournalEntry` is a deterministic English keyword lexicon (`frontend/journal-app/src/journalAnalysis.ts:23-99`). It has no provider configuration, timeout/retry, safety boundary, cost control, structured-output validation, or provenance metadata.
- The deterministic analysis does provide evidence words and avoids calling an API, but summaries such as “strongest signal” are heuristic and are not linked to source spans/entry IDs in persisted output.
- Meeting transcription is a timed state-machine simulation that inserts a literal placeholder segment (`frontend/journal-app/src/main.ts:316-333`). Expo stops at `normalizing`; no transcription service is called.
- Prompt-injection protections do not exist because no model boundary exists yet. Before adding one, journal/transcript content must be treated as untrusted data, separated from system instructions, length-limited, schema-validated, and tied to cited source IDs.

### Client security and correctness

- The Vite journal history interpolates raw user text into `innerHTML` (`frontend/journal-app/src/main.ts:183-201`), creating a DOM-XSS path. Meeting fields use `escapeHtml`, but journal history does not.
- Vite and Expo implement different persistence and feature sets rather than sharing a coherent runtime/service boundary.
- Generated `dist` trees and installed `node_modules` exist in the workspace; they are not listed by `git ls-files`, but release hygiene should remove or consistently ignore generated outputs before commit.

### Tests and release state

- Existing tests cover four domain modules and pass, but they are module-level assertions rather than API, browser, device, persistence-failure, auth, privacy-erasure, or security integration tests.
- Expo has no test script. Typecheck and web export pass; iOS/Android store builds, signing, submission, and physical-device QA were not demonstrated.
- No deployed backend health/auth/privacy flow was found or verified. The two live frontend aliases are healthy but stale relative to the current source.

## Remediation priority

1. Fix the raw journal DOM-XSS and remove unsupported `Encrypted locally` / `Delete permanently` claims.
2. Define one production architecture: authenticated API, encrypted durable journal/meeting stores, tenant ownership checks, sync/idempotency, and deletion/export receipts. Keep the legacy API disabled until its identifier-based authorization and privacy policy are replaced.
3. Implement OAuth authorization code + PKCE with one-time state, validated callback handling, secure token storage, refresh/revocation, and user-bound data.
4. Implement real downloadable/shareable export and complete local + remote erasure, including audio/transcript/summary/embedding/reflection scopes.
5. Add a model adapter only behind explicit consent and a strict untrusted-content boundary; return schema-validated, source-cited insights or an honest error—never fabricated output.
6. Add integration/security tests and deploy the exact verified source artifact. Verify the live bundle hash/features, backend health, migration, auth isolation, and deletion/export behavior before a completion claim.
