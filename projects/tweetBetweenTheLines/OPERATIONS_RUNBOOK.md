# tweetBetweenTheLines operations runbook

Status: production operations baseline. This file records what must be true before the closed beta or production launch can be represented as operationally ready. It is intentionally conservative: local builds are evidence for bundle health, not for deployed operations.

## Release posture

Current decision: BLOCK for production and external closed beta until every item below has real evidence.

Allowed now:

- Local synthetic/consented-fixture verification.
- Durable public Expo web-MVP smoke verification at `https://tweetbetweenthelines.vercel.app`.
- Web/iOS/Android JavaScript bundle exports.
- UX review of consent, source coverage, evidence, corrections, revocation, export, delete, and non-diagnostic safety copy.

Not allowed to claim yet:

- Production-readiness claims beyond static web hosting; the durable Vercel alias verifies the Expo web MVP only.
- TestFlight verification.
- Android internal testing track verification.
- Complete source/platform coverage beyond the implemented and verified connector contracts.
- Diagnosis, crisis prediction, treatment, eligibility, employment, insurance, credit, policing, or complete mental-health assessment.

## Observability

Required telemetry rules:

- Log opaque IDs, tenant, actor class, action, decision, outcome, build/version, and latency buckets only.
- Never log provider tokens, refresh tokens, archive bytes, raw posts/messages/searches, prompt bodies, filenames, URLs with secrets, self-report answers, exports, or deletion keys.
- Use separate dashboards for ingestion, consent/revocation, archive sandbox, export/delete jobs, model gateway, and client app health.
- Alert on OAuth callback replay, archive sandbox failures, cross-tenant deny events, model-payload rejection, privacy job retry exhaustion, budget burn, and app crash spikes.

Minimum launch evidence:

- Web, iOS, and Android crash/error dashboards with source maps or symbolication.
- Synthetic canary proving a raw-content marker is not emitted to logs.
- Alert routing and on-call acknowledgement drill.

## Backups and restore

Required restore drill:

1. Restore identity, consent, raw/quarantine, normalized, feature, insight, audit, export, and job stores into an isolated environment.
2. Prove tenant isolation remains enforced after restore.
3. Execute source revocation and account deletion against the restored copy.
4. Reconcile descendants, cache entries, queued jobs, expiring exports, vector/search indexes, and backup retention/key-destruction state.
5. Produce non-personal audit tombstones and a user-facing completion receipt.

Backups must not resurrect deleted material. Crypto-erasure key destruction evidence is required before treating backup deletion as complete.

## Incident response

Severity examples:

- SEV-1: token exposure, cross-tenant data exposure, deletion failure that preserves data after claimed completion, malicious archive sandbox escape.
- SEV-2: OAuth replay attempt, privacy job retry exhaustion, model gateway raw-content leak prevention failure, unsupported diagnostic output reaching a user.
- SEV-3: degraded ingestion, delayed export, app crash spike, non-sensitive dashboard outage.

Required actions:

- Freeze affected source ingestion and model jobs.
- Preserve audit logs without preserving personal content.
- Rotate/revoke impacted provider tokens and keys.
- Notify users/regulators according to jurisdictional obligations after legal/privacy review.
- Publish a correction plan and regression tests before re-enable.

## Cost controls

Closed beta hard limits must be configured before inviting testers:

- Maximum testers by jurisdiction.
- Per-user archive imports per day.
- Per-user OAuth sync jobs per day.
- Per-source API quota and paid tier spend.
- Model gateway calls per tester and per cohort evaluation.
- Quarantine/raw retention and storage caps.
- Kill switch for archive parsing, connector sync, and model generation.

The executable domain function `estimateMonthlyCost` provides a deterministic budget check for synthetic scenarios; real provider billing dashboards must be linked before launch.

## Privacy request operations

Export and delete controls must require step-up authentication. Production must queue idempotent privacy jobs, display pending/failed/completed status, and issue completion receipts. A delete completion receipt is not valid until descendants, caches, queues, exports, vendors, and backup/key-retention state have reconciled.

## Closed beta protocol

Participant admission requires:

- Explicit closed-beta consent.
- Synthetic data or data from the consenting participant only.
- Age gate and supported jurisdiction.
- Acceptance of non-diagnostic safety copy.
- Agreement that source coverage labels are incomplete and may change.

Use `selectClosedBetaParticipants` to fail closed in tests and scripts. Never use scraped, third-party, or non-consented fixtures.

## Deployment checklist

Web:

- Production build and mobile/desktop browser smoke.
- HTTPS deploy URL, OAuth callback, monitoring, rollback.

IOS:

- Signed EAS/native production build.
- Simulator and physical-device smoke.
- Keychain, associated domains, privacy manifest, screenshots, TestFlight.

Android:

- Signed app bundle.
- Emulator and physical-device smoke.
- Keystore, app links, Data Safety, screenshots, internal testing track.

Shared:

- Unit, integration, contract, and end-to-end tests.
- Accessibility and safe-area checks.
- Slow-network, retry, expired-session, revocation, export, delete, and telemetry tests.
- No embedded secrets in any web bundle or mobile package.
