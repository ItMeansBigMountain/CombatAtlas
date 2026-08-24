# Honda Tech Upgrade prior-art audit and BurnoutBoyz migration map

Audited: 2026-08-24

## Decision

Honda Tech Upgrade is useful interaction and deterministic-planner prior art, but it is not a trustworthy maintenance data source. BurnoutBoyz may reuse the form/timeline interaction patterns, local-trial privacy behavior, pure-function calculation shape, status presentation, and tests after generalization. It must not copy the hard-coded intervals or present their output as manufacturer guidance.

BurnoutBoyz remains an all-makes product. Honda is only a legacy fixture and a possible future provider-specific test case.

## Canonical sources and recoverability

| Source | Role | Recoverable reference |
|---|---|---|
| `projects/honda-tech-upgrade` | Canonical static/Express local scaffold and original planning docs | Imported in Git commit `bde1f1151`; plans added in `f2c024bac`; tested scaffold captured in `577682570` |
| `projects/_vercel_mvp/honda-tech-upgrade` | React/Vite Vercel implementation | Initial shell in `481646208`; planner/UI implementation captured in `577682570` |
| `https://honda-tech-upgrade.vercel.app` | **Production legacy URL**; currently serves the React/Vite planner | Anonymous HTTP 200 on 2026-08-24; HTML references `index-1y6Fr59b.js` and `index-BpntD7P-.css` |
| `https://honda-tech-upgrade-f62krixi3-itmeansbigmountains-projects.vercel.app` | **Historical production deployment URL**; older shell | Anonymous HTTP 200 on 2026-08-24; 167-byte HTML has no title and is not the current planner |

The legacy directories remain in place and are tracked by the monorepo, so no destructive move or history rewrite is required. The commit references above are the recovery anchors. Do not delete either legacy directory until a separately reviewed archival task records an immutable bundle and confirms the Vercel retirement policy.

Key audited file checksums (SHA-256):

- Canonical `app.js`: `50c63c9c8b68f3eef80151c41614186382a29f29d0b90263664959fdd2021d2e`
- Canonical `app.test.js`: `ed59f49cd08bacac9cac4cdcc4310f36eb7a4f19c114543d16e4ee7a2ce89aa1`
- Vercel `src/planner.js`: `baaf660c016a8fe7a86e228dae73baaea7ce65e48f91b5e946edfb544cfa1b2b`
- Vercel `src/planner.test.mjs`: `02cf16539dfb809fb8546c50b37c6bcf6552ae8b7b6fdbf43914a956f6c1a40d`
- Vercel `src/main.jsx`: `3379f469f353775763c60e934fd6ea283b4b47494dbfbc0e2f3e71e024078b2f`

## Verification evidence

Executed against both source trees on 2026-08-24:

- Canonical: `npm test && npm run build` — 3/3 tests passed; its `build` script only reruns tests and emits no deploy artifact.
- Vercel MVP: `npm test && npm run build` — 3/3 tests passed; Vite produced a 0.57 kB HTML file, 2.31 kB CSS asset, and 196.00 kB JavaScript asset.
- Friendly production alias: HTTP 200, `text/html; charset=utf-8`, title `Honda Tech Upgrade`; fetched JavaScript contains the current planner heading and owner-workflow copy.
- Historical deployment URL: HTTP 200, `text/html; charset=utf-8`, no document title; it remains an older review shell.

The six tests are near-duplicates across two implementations. They validate normalization, one mileage calculation, and sample reset behavior. They do not validate schedule provenance, year/trim/powertrain variation, time intervals, severe use, multiple records, expected-versus-confirmed semantics, recalls, or provider versioning.

## Reusable prior art

| Legacy piece | Evidence | BurnoutBoyz destination/contract | Treatment |
|---|---|---|---|
| Pure normalization and plan functions | `app.js:27-117`; `src/planner.js:28-108` | Domain service consuming validated vehicle + versioned schedule rules | Reimplement with typed/domain inputs; no embedded vehicle table |
| Deterministic timeline ordering and status badges | `app.js:61-97,152-188`; `main.jsx:24-26,86-103` | Timeline view model and accessible UI components | Reuse interaction concept; replace status vocabulary and calculation rules |
| Local browser trial and clear/reset controls | `app.js:135-149,198-223`; `main.jsx:15-22,38-48` | Privacy-preserving local trial adapter | Reuse pattern with explicit schema version, export, and deletion confirmation |
| Labeled form controls, live results, keyboard-friendly controls | `index.html:18-50`; `main.jsx:51-104` | Vehicle intake and timeline screens | Reuse semantic structure and visible focus styling; generalize all copy/options |
| Sample fixture and deterministic tests | both planner test files | Provider-neutral fixtures and contract tests | Preserve testing style; replace Honda interval assertions with synthetic, explicitly non-OEM rules |
| Formatting and distance-to-due presentation | `app.js:57-59`; `src/planner.js:56-58` | Shared display formatter | Reuse only as presentation; store canonical numeric units separately |

## Unsupported or unsafe claims and logic

1. `SERVICE_INTERVALS` assigns one mileage-only table to entire Civic, Accord, and CR-V model names with no year, engine, transmission, trim, region, schedule version, source, license, confidence, or normal/severe-use distinction. These values are unsupported generic claims and must not migrate.
2. The planner treats elapsed mileage as evidence for a next service target. BurnoutBoyz must separately model expected occurrences and confirmed service records; absence of a record is `unknown`, not proof that service happened or did not happen.
3. Only one recent service event is accepted. This cannot represent recurring history, receipts, multiple odometer readings, corrections, or conflicting evidence.
4. Time-based intervals are absent. Production due state must evaluate mileage and elapsed time according to the sourced rule rather than mileage alone.
5. `overdue`, `due soon`, and `planned` are calculated with a fixed 1,500-mile threshold, not provider semantics or user-configured reminders. The threshold must not migrate as maintenance truth.
6. Defaulting unknown vehicles/events to Civic/Oil Change silently manufactures applicability. Production validation must fail closed or show a clearly labeled generic-guidance state.
7. The React planner's selected-event calculation uses `knownServiceMileage + interval`, while the canonical scaffold applies an additional cycle-based maximum. The two implementations can disagree; neither algorithm should become the production contract without schedule-rule tests.
8. Copy such as “All tracked services need attention soon; prioritize a maintenance visit” is generated without mechanical context or sourced safety guidance. Replace it with factual due-state language and an explicit non-diagnostic disclaimer.
9. Browser `localStorage` is suitable for a disposable trial, not durable sensitive VIN/service/receipt storage without threat modeling, schema migration, and deletion/export controls.
10. The canonical package's `build` script is test-only. It must not be used as evidence that a deployable production artifact was built.

## Migration sequence

### 1. Domain and provenance first

Implement the backend child task's vehicle identity, schedule provider/version, interval rule, expected occurrence, confirmed record, evidence, confidence, and deletion-lineage models before importing planner behavior. Every computed recommendation must carry rule/provider/version/source identifiers.

### 2. Provider-neutral planner contract

Define a pure planner that accepts:

- a precisely identified vehicle configuration or an explicit unresolved identity state;
- dated odometer observations and an in-service date;
- usage severity with evidence/assumptions;
- versioned interval rules containing mileage and/or time triggers;
- confirmed service records and applicability decisions;
- a calculation timestamp.

Return expected occurrences, confirmed matches, unknown/overdue state, next mileage/date, assumptions, and provenance. Never return an OEM-looking recommendation from a make/model name alone.

### 3. Synthetic test migration

Port the deterministic test shape, not the Honda numbers. Add synthetic rules for mileage-only, time-only, whichever-first, severe-use, repeated occurrences, conflicting odometer data, unknown vehicle identity, non-applicable rules, schedule-version changes, and no confirmed history. Keep provider adapter tests separate from planner tests.

### 4. UI migration

Generalize the React form/timeline pattern into:

1. VIN or year/make/model/trim intake;
2. decoded-configuration confirmation;
3. mileage/date/severity capture;
4. service-history entry;
5. expected vs confirmed vs unknown/overdue timeline;
6. source/version/confidence disclosure on every rule;
7. local-trial reset/export/delete controls.

Do not migrate Honda branding, fixed vehicle dropdowns, fixed service dropdowns, generic intervals, or the claim that the browser-only demo is a complete ownership plan.

### 5. Legacy boundary

Keep legacy code read-only as prior art. New BurnoutBoyz code must not import modules from either legacy directory at runtime. If a visual component is reused, copy it into BurnoutBoyz with renamed all-makes semantics, attribution to the recovery commit in its migration commit, and new provider-neutral tests.

## Acceptance gates for downstream implementation

- No hard-coded real-world interval may enter production without provider, source URL/document identity, license classification, version/effective dates, applicability fields, and confidence.
- Unknown configuration must remain unknown; no silent Civic or other model fallback.
- Expected and confirmed service are separate persisted concepts.
- Both mileage and time rules are tested.
- The UI displays source/version/assumptions beside recommendations.
- Local trial data can be exported and permanently cleared; account data follows server deletion lineage.
- Honda appears only as sourced data or an explicitly labeled fixture, never as product scope.

## Artifact scope

This migration map is a documentation artifact and has no new runnable BurnoutBoyz URL. The only runnable URLs audited here are the two legacy production URLs labeled above.
