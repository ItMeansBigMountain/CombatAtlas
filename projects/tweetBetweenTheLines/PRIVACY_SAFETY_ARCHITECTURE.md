# Privacy, Consent, Clinical-Safety, and Explainability Architecture

Status: production design baseline; security, privacy, legal, accessibility, and qualified clinical review remain launch gates.

## Safety invariants

1. Social activity may support reflection, never diagnosis, treatment, eligibility, employment, insurance, credit, policing, or crisis prediction.
2. Consent is specific to tenant, person, source, data category, purpose, policy version, and time. Product access is not blanket consent.
3. Provider credentials never enter raw stores, analytics stores, logs, telemetry, model prompts, or exports.
4. Tenant identity is mandatory on every object, key, query, queue message, cache key, and audit event. Authorization denies on missing or mismatched tenant context.
5. Every derived value retains input lineage and analyzer provenance and is removable when an ancestor is revoked or deleted.
6. Archive bytes are hostile until validated inside a network-denied sandbox.
7. Sensitive insights are private by default, reviewable, correctable, and never shared automatically.

## Threat and privacy model

Protected assets include identity bindings, provider tokens, archives, messages/posts/searches, normalized events, derived features, profile cards, self-report answers, exports, deletion keys, and audit records. Adversaries include credential thieves, malicious co-tenants, compromised connectors, archive authors, abusive insiders, model providers, prompt-injection content, and users attempting inference about another person.

| Threat | Required control | Verification |
| --- | --- | --- |
| OAuth interception/account mix-up | Authorization Code + PKCE, exact redirect allowlist, one-use signed state bound to tenant/user/provider, short expiry | negative callback and replay tests |
| Token disclosure | envelope-encrypted token vault, per-tenant data-encryption keys, KMS-wrapped keys, no token reads by analytics role | IAM test and prompt/log canary scan |
| Cross-tenant access | tenant-scoped RLS/partition keys, service authorization, tenant-bound object paths and cache keys | adversarial two-tenant integration suite |
| Archive traversal, bombs, malware | isolated worker, no network, CPU/RAM/time quotas, compressed/uncompressed/entry limits, MIME sniffing, path canonicalization, malware scan | malformed ZIP corpus and sandbox escape review |
| Prompt injection in imported text | imported content is quoted data, fixed schemas, no tools/URLs from model, aggregate/minimized payload, output validation | injection red-team corpus |
| Membership/inversion or model retention | no training on user data by default, zero-retention provider contract, minimized aggregates, output suppression | vendor/config attestation |
| Insider browsing | least privilege, JIT audited production access, break-glass approval, immutable access logs, alerts | quarterly access review |
| Re-identification/export leakage | user-bound export authorization, encrypted expiring download, no unrelated tenant data, step-up auth | export isolation tests |
| Incomplete revocation/deletion | lineage graph, descendant invalidation, queue cancellation, cache purge, crypto-erasure, retryable evidence | deletion reconciliation job |

Logs contain opaque IDs, action, actor class, policy decision, timestamp, and outcome; never tokens, raw text, answers, filenames, URLs with secrets, or prompt bodies. Audit tombstones prove an action occurred without preserving personal data.

## Data planes and tenant isolation

Use physically/logically distinct services and credentials:

- Identity plane: account, passkey/social identity binding, sessions, tenant memberships.
- Consent plane: append-only receipts and superseding revocation receipts.
- Secret plane: encrypted provider tokens only; connector role may decrypt just-in-time.
- Quarantine/raw plane: encrypted imports with short, user-visible retention.
- Normalized plane: provenance-rich personal events partitioned by tenant and subject.
- Feature plane: deterministic aggregates; no secrets or raw archive references in model payloads.
- Insight plane: evidence references, uncertainty, model provenance, review state.
- Audit plane: append-only non-content events and deletion tombstones.

A service receives a verified `{tenantId, subjectId, actorId, purpose}` context. Database policies and object paths enforce the same context; application filters alone are insufficient. Background jobs carry signed, expiring tenant context and idempotency keys. Support access never bypasses row policies.

## Consent receipts

Each source/category/purpose grant produces a receipt containing: receipt ID, tenant, subject, source/provider identity, authorized categories, exact OAuth scopes or archive categories, purpose, grant time, policy/UI-copy version, locale, acquisition path, retention choice, and status. Store evidence of the choice, not dark-pattern telemetry. Optional analysis and optional sensitive insights default off and cannot be required for basic export/import features.

Scope changes create a new receipt. Revocation records effective time and reason category, invalidates OAuth tokens, stops ingestion jobs, blocks new analysis, and starts descendant deletion/rebuild. Re-consent never silently resurrects deleted data.

## Processing and explainability

`token reference -> connector -> quarantined raw -> normalized event -> deterministic feature -> optional model payload -> insight`

Only the connector can resolve token references. The model gateway accepts a typed payload containing tenant-bound aggregate evidence, never token/raw references. It rejects unknown fields and scans canaries. Every insight records:

- evidence spans or aggregate IDs and deletion lineage;
- deterministic feature schema/version;
- provider, model, model version, prompt version, input digest, generation time;
- confidence/calibration statement, known limitations, locale, and review status;
- why shown, source coverage, missing-data caveat, and user correction state.

Model or prompt upgrades do not overwrite provenance. Reprocessing creates a new version; rollback and comparison remain possible until retention/deletion removes ancestors.

## Export, revocation, and deletion lineage

Exports include consent receipts, raw data when retained, normalized events, features, insights, model provenance, corrections, and a machine-readable manifest/checksums. Provider tokens, internal security metadata, and other users' data are excluded. Require step-up authentication and an encrypted, short-lived download.

Lineage edges are explicit from source/receipt through every descendant. Source revocation executes in this order: stop jobs and revoke token; hide insights; delete/invalidate insights and caches; delete features; delete normalized events; delete raw objects; crypto-erase source keys; supersede/delete consent details according to legal retention; retain only a non-personal audit tombstone. Account deletion repeats across all sources, backups via key destruction, exports, queues, telemetry, and vendors. A reconciliation job reports pending/failed steps without restoring content. Legal holds require a disclosed, narrowly scoped policy and must not silently preserve data.

## Archive sandbox

Upload to quarantine, never directly to an application server. Before parsing: enforce allowlisted formats, MIME/magic agreement, per-file and aggregate byte limits, entry-count and expansion-ratio limits, path normalization, nested-archive depth, symlink/device-file rejection, malware scanning, schema bounds, encoding limits, and duplicate handling. Parse in an ephemeral unprivileged container with read-only runtime, isolated temp volume, no network, seccomp/capability restrictions, and hard CPU/memory/time quotas. Promote validated records only; delete quarantine failures on the declared schedule. Do not execute HTML, formulas, scripts, links, media metadata, or archive-supplied code.

## Mental-health and personality boundary

Observational social data may say “language in this selected slice included more strain terms,” with evidence and uncertainty. It must not label a disorder, risk score, personality type as fact, treatment need, or causal explanation. Absence of a signal is not wellbeing evidence. Crisis status must never be inferred from posts.

Personality assessment requires an optional, separately consented self-report flow. Prefer openly usable, validated instruments such as IPIP item sets, but verify the exact item set, scoring key, translations, validation population, and license before shipping. Do not present social-media inference as an instrument score.

Screeners such as PHQ-9 or GAD-7 may be evaluated only as separately consented self-report experiences after confirming current licensing/terms, intended population, scoring implementation, locale validation, accessibility, privacy, and professional governance. Results are screening information, not diagnosis. Release requires qualified professional review, jurisdiction-specific copy, a locale-aware crisis/escalation path, and clear emergency limitations. If answers indicate possible immediate danger, show local emergency/crisis options and encourage contacting a qualified professional; do not claim monitoring, dispatch responders automatically, or rely on an LLM for triage. Minors, third-party assessment, workplace use, and clinical integration are out of scope until separately governed.

## Bias and multilingual evaluation

No locale launches from translation alone. Create consented, representative evaluation sets with human annotation guidance and report by locale/dialect, gender (where voluntarily supplied), age band, disability/access needs, and other legally/ethically approved cohorts. Measure coverage, false-positive/negative rates, calibration, abstention, evidence faithfulness, harmful stereotyping, diagnostic-language leakage, and inter-cohort disparity. Establish minimum sample sizes and preregistered thresholds; block release when any cohort fails rather than averaging it away. Small cohorts are “insufficient evidence,” not passes. Use native-language reviewers, challenge code-switching/slang, test right-to-left UI, and provide an abstain/no-insight path.

## Required launch evidence

- Threat model reviewed after architecture changes and at least annually.
- Automated tenant-isolation, consent, revocation, export, delete/reconciliation, archive-fuzz, prompt-canary, and diagnostic-language tests.
- Data inventory, retention schedule, processor/subprocessor contracts, incident response, DPIA/appropriate jurisdictional assessment, and user-facing privacy copy.
- Model cards and provenance registry with rollback, zero-retention configuration evidence, bias/multilingual report, and red-team findings.
- Qualified legal/privacy and, for any screener or health-adjacent feature, clinical review sign-off.

Fail closed: missing consent, tenant context, provenance, locale validation, crisis flow, professional review, or evaluation evidence means no processing or release.
