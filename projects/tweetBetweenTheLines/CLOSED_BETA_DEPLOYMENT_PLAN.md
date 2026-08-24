# Closed beta and deployment evidence plan

Status: plan plus executable gate. No production deploy, TestFlight run, Android internal-track run, or live monitoring evidence exists yet.

## Environments

- `local-synthetic`: local developer machine, synthetic or explicitly consented fixture data only.
- `staging-consented`: production-like backend with test tenants, real OAuth credentials, no public marketing.
- `closed-beta`: invitation-only testers who passed consent, age, jurisdiction, and safety-copy checks.
- `production`: blocked until independent legal/privacy/security/safety approval and all platform store gates pass.

## Git-based deployment

Required Git flow before beta:

1. Protect `main` and require review plus passing CI.
2. CI runs domain tests, mobile typecheck, web export, iOS export, Android export, lint/whitespace, audit, and secret scans.
3. Merge to `main` deploys web staging automatically.
4. Tags `beta-web-*`, `beta-ios-*`, and `beta-android-*` map to immutable builds.
5. Rollback is a Git revert or prior immutable deploy promotion, not an untracked console edit.

## Synthetic and consented E2E fixtures

Use only:

- Generated posts/watch-history/search/activity records with no real person attached.
- A tester’s own official archive or OAuth data after explicit written consent.
- Dedicated test OAuth accounts where provider terms allow it.

Do not use:

- Scraped public profiles.
- Friends/family data without direct consent.
- Legacy credentials or archive files from old experiments.
- Paid/restricted platform APIs unless access and terms are verified.

## Real end-to-end scenarios

Each scenario must be run on web, iOS, and Android before closed beta can be called verified:

1. Sign in, consent to one source/category/purpose, connect OAuth with PKCE, and confirm server-side state is consumed exactly once.
2. Import an official archive fixture, show validation/progress, and reject malformed/traversal/oversized archives.
3. Generate a profile card from synthetic/consented records and inspect source-backed evidence.
4. Submit a correction and verify old evidence and correction remain separately provenance-linked.
5. Revoke a source and prove new ingestion stops and existing profile cards hide revoked evidence.
6. Download an export after step-up auth and verify the manifest/checksum excludes secrets and other tenants.
7. Delete account data and verify descendant deletion, cache purge, queue cancellation, backup/key reconciliation, and non-personal tombstone.
8. Exercise accessibility: screen reader labels, tab order, safe areas, contrast, reduced motion, dynamic text, and small-screen layout.
9. Exercise slow network, expired session, provider denial, offline retry, privacy job failure, and rollback paths.
10. Confirm telemetry contains opaque IDs only and no raw text/tokens/prompt bodies.

## Closed beta admission

A participant enters beta only if `selectClosedBetaParticipants` would accept them:

- Explicit beta consent: yes.
- Synthetic or participant-owned consented fixture: yes.
- Age gate: passed.
- Supported jurisdiction: yes.
- Non-diagnostic safety copy accepted: yes.

Rejected participants receive a plain-language reason. Rejection must not be worked around manually.

## Release evidence ledger

Use this ledger in reviews. `blocked` means the release must remain blocked.

| Area | Current evidence | Status |
| --- | --- | --- |
| Domain/security regression tests | Local Node test suite | verified locally |
| Web bundle | Expo web export | verified locally only |
| iOS bundle | Expo iOS JS export | verified locally only |
| Android bundle | Expo Android JS export | verified locally only |
| Production web URL | None | blocked |
| Real backend OAuth/code exchange | None | blocked |
| Signed iOS build/TestFlight | None | blocked |
| Signed Android bundle/internal track | None | blocked |
| Physical-device accessibility evidence | None | blocked |
| Observability dashboards/alerts | Runbook only | blocked |
| Restore drill/deletion reconciliation | Domain contracts only | blocked |
| Incident response drill | Runbook only | blocked |
| Provider cost dashboards/budgets | Domain estimator only | blocked |
| Legal/privacy/safety review | Not present | blocked |

## Copy rules

Allowed wording:

- “Source-backed reflection.”
- “This selected slice contains examples of strain language.”
- “Coverage depends on each platform’s official API or export and may be incomplete.”
- “Not a diagnosis or crisis-detection service.”

Blocked wording:

- “We diagnose depression/anxiety/personality from your posts.”
- “We detect if you are suicidal.”
- “We cover all of X/TikTok/Instagram/YouTube history.”
- “Deletion is complete” before reconciliation and backup/key evidence exists.
