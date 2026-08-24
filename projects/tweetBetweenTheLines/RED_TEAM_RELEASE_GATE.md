# Independent red-team release gate

Date: 2026-08-24
Scope: domain contracts for OAuth/PKCE, token vault, tenant isolation, archives, model boundary, deletion, provenance, inference/bias, account access, mental-health safety, and privileged abuse.

## Decision

**BLOCK for production deployment.** The implemented domain controls and 36-test suite can satisfy the executable `buildReleaseGate` only after deployment evidence confirms model provenance, deletion reconciliation, multilingual cohort readiness, and safety approval. No production service or operational evidence exists in this repository, so those gates must not be inferred from unit tests.

## Confirmed high findings remediated

| ID | Finding | Evidence | Remediation |
|---|---|---|---|
| RT-01 | Cross-tenant export: untyped feature/insight arrays could carry another subject's data | `redTeam.test.ts`: cross-tenant feature and insight injection | Every exported feature/insight must carry the exact tenant and subject binding; mismatch fails closed. |
| RT-02 | Prompt injection and secret smuggling could enter analytics payloads through nested aggregate evidence | `redTeam.test.ts`: instruction and refresh-token payloads | Recursive serialized boundary rejects secret markers and instruction/tool-call patterns; accepted payloads are labeled untrusted aggregate data. |
| RT-03 | Archive path validation did not normalize Unicode before traversal checks | `redTeam.test.ts`: full-width-dot traversal and NUL filename | NFKC normalization plus NUL/traversal rejection before parsing. |
| RT-04 | Model provenance accepted empty/fabricated identifiers and arbitrary digests | `redTeam.test.ts`: malformed digest | All provenance fields are required and input digest must be canonical `sha256:<64 lowercase hex>`. |
| RT-05 | NaN/out-of-range cohort metrics could bypass comparisons and incorrectly pass bias gates | `redTeam.test.ts`: NaN false-positive rate | Locale, integer sample size, and finite [0,1] rate validation fail closed. |
| RT-06 | Mental-health prohibitions were bypassable by labeling output `general`; harmful medication advice was not blocked | `redTeam.test.ts`: general-category suicidal inference and medication direction | Diagnostic/crisis claims are blocked in every category; harmful treatment-avoidance direction is blocked. |
| RT-07 | No reusable authorization contract constrained insider/admin privacy operations | `redTeam.test.ts`: admin without case, cross-subject user, admin token read | Step-up, subject-self binding, support-case requirement, service-role limits, and connector-only token reads. |

## Attack coverage and residual gate

- OAuth state/PKCE: one-use, expiry, tenant/subject/provider/redirect/state binding, scope subset, S256, and redirect allowlist are covered by connector tests. Production must store pending authorizations server-side and atomically consume state.
- Token vault: AES-256-GCM with tenant/subject/provider/scope/key AAD, connector-only reads, revocation denial, and cross-tenant denial are covered. Production KMS policy/rotation remains unverified.
- Tenant isolation/account takeover: domain context checks, step-up export, export ownership checks, passkey/social subject binding, and sensitive-operation policy are covered. Production session fixation, WebAuthn verification, rate limits, and recovery flows remain unverified.
- Archive parsers: traversal, Unicode traversal, NUL, symlink/device, malware, MIME/magic/digest, entry/size/ratio/depth limits, schema versioning, and idempotence are covered. Parser sandbox enforcement is a declared contract, not infrastructure evidence.
- Prompt injection: known instruction and secret patterns fail closed. Production should keep model tools disabled for analytics and use structured schemas; regex screening is defense-in-depth, not a complete injection defense.
- Deletion leakage: descendant/key/cache/queue deletion plans and non-personal tombstones exist. Production reconciliation, backup expiry, search/vector deletion, and failure alerting remain unverified.
- Model provenance/inference attacks: strict provenance format and evidence-first deterministic outputs exist. Provider attestation, signed model registry, membership-inference testing, and extraction resistance remain unverified.
- Multilingual/cultural bias: unsupported wellbeing locales abstain and cohort metrics fail closed. Representative human evaluation and dialect/code-switching cohorts remain unverified.
- Harmful mental-health outputs: diagnostic/crisis claims and unsafe treatment direction are blocked, with non-diagnostic disclosure/help guidance elsewhere. Professional safety approval remains unverified.
- Insider/admin abuse: privileged case binding and connector-only token reads are encoded. Production immutable audit, dual control, JIT access, and alerting remain unverified.

## Release requirements

Production decision may change to GO only when all are true:

1. zero open critical/high findings;
2. full regression suite and typechecks pass;
3. deployed model provenance is independently verified;
4. deletion reconciliation passes against every live store, cache, queue, export, and backup policy;
5. representative multilingual/dialect cohorts pass documented thresholds;
6. professional safety review is approved;
7. OAuth state is atomically consumed in a server-side store and KMS/IAM policies are tested in deployment;
8. infrastructure evidence confirms archive sandboxing and privileged-access audit controls.
