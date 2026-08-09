# Networked RuneLite plugin production-readiness gate

Use this before moving any RuneLite plugin with a custom backend from `in-progress` to `pr-review-pending`.

## Third-party data and consent

- Derive disclosures from actual request builders, registration payloads, telemetry event serialization, and backend persistence—not README claims.
- Separate service calls required for the core feature from optional analytics/telemetry. A required online board does not imply consent to combat/location telemetry.
- Any option that enables transmission must clearly name the destination and payload categories in-client. README disclosure alone is insufficient.
- Default optional telemetry off. When off, block enqueue and upload, clear buffered events, and test that no telemetry request occurs.
- Keep telemetry consent separate from public-profile visibility. A publication toggle must never silently enable collection.
- Document operator/contact, retention, deletion, processors/storage, what “private” means, and a stable privacy-policy location before production submission.

## Resilient API parsing

- Parse JSON with typed/validated Gson DTOs or guarded `JsonObject` access. Do not use substring searches for session tokens, arrays, capabilities, or expiry values.
- Reject missing/blank tokens, invalid timestamps, null/wrong-type collections, empty successful bodies, and unknown required shapes as controlled `IOException`/domain failures.
- Treat runtime parser exceptions as network refresh failures at the worker boundary.
- Every in-flight guard and loading indicator must be released on success, checked failure, unchecked parse failure, stale identity, cancellation, and shutdown. Prefer one worker-level completion/finally path that always schedules cleanup.
- Preserve identity-generation checks across async completion; malformed responses must not re-enable stale sessions or state.

## UI semantic integrity

- Button labels must describe the endpoint/action actually executed. A button labeled “Accept & schedule” must mutate/accept the selected record; pre-filling a new challenge form is not acceptance.
- If the service has no verified accept flow, use an honest label such as “Challenge this clan” and preserve the selected opponent without claiming acceptance.
- Disable submission controls while an action is in flight and show pending/success/failure inline. Retain entered values after failure and prevent double dispatch.

## Required tests

Use MockWebServer or an equivalent injected HTTP fixture to cover:

- compact and pretty valid JSON;
- reordered keys and escaped strings;
- malformed JSON and empty successful bodies;
- missing/null/wrong-type arrays and objects;
- invalid expiry values and blank session tokens;
- HTTP 4xx/5xx and delayed/reordered responses;
- loading/in-flight cleanup followed by a successful retry;
- shutdown/cancellation and A→B→A identity changes;
- telemetry disabled versus enabled request capture;
- double-click mutation suppression and control recovery.

A Swing paint smoke test and a green standalone Gradle build are not substitutes for these network/lifecycle tests.

## Submission gate

Before opening the Plugin Hub PR:

1. Run Java 11 `clean test assemble`.
2. Run the network/async matrix above.
3. Capture real requests for each privacy configuration and compare them with docs.
4. Validate leader authorization and acceptance workflow using consenting real clans/accounts; do not create synthetic production records.
5. Confirm metadata consistency, unique approved icon, production-pinned HTTPS endpoint, no developer/role-preview switches, and one immutable marker SHA.
6. Open the PR only at its user-approved position in the one-open-PR release queue.
