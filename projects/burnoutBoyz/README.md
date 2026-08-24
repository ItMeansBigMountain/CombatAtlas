# BurnoutBoyz

A data-backed maintenance owner's manual for every car owner.

Enter or decode your vehicle, current mileage, vehicle age, driving conditions, and maintenance history. BurnoutBoyz explains what maintenance should have occurred, what is confirmed, what is unknown or overdue, and what is coming next.

See [`PRODUCT_DIRECTION.md`](PRODUCT_DIRECTION.md) for the product contract, data strategy, and safety boundaries.
See [`DATA_STACK_RESEARCH.md`](DATA_STACK_RESEARCH.md) for the source-cited vehicle/maintenance data provider and licensing matrix. The evidence-backed [`HONDA_PRIOR_ART_MIGRATION.md`](HONDA_PRIOR_ART_MIGRATION.md) records which legacy planner/UI patterns may migrate, which claims must not, and the Git/deployment recovery anchors.

## Current stage

The provenance-first backend foundation is implemented in `burnoutboyz/`: a SQLite migration models accounts, garages, precise vehicle configuration, time/odometer history, versioned schedule rules, expected-versus-confirmed maintenance, evidence/costs/reminders/recalls, connected accounts, confidence, and deletion lineage. The previous Honda Tech Upgrade MVP remains prior art, not the final product.

The Expo Router SDK 57 universal client now lives in `apps/universal`. It renders one responsive garage/manual experience for web, iOS, and Android, with offline garage persistence, native Keychain/Keystore secret storage, receipt camera/document adapters, local notification permission flows, deep-link configuration, recalls/source caveats, and optional connected-car consent. Run `npm run build:web` there for the static web artifact or see `apps/universal/RELEASE.md` for verified commands and the remaining external store/account gates.

Run the dependency-free backend tooling with Python 3.11+:

```sh
python3 -m burnoutboyz.admin --database ./burnoutboyz.db migrate
python3 -m burnoutboyz.admin --database ./burnoutboyz.db schema-status
python3 -m unittest discover -s tests -v
```

[`IMPORT_CONTRACT.md`](IMPORT_CONTRACT.md) defines the transactional schedule-provider import boundary. Its bundled schedule is synthetic test data only, never OEM guidance.

## Vehicle onboarding

`burnoutboyz.onboarding` provides strict 17-character VIN/check-digit validation, NHTSA vPIC decoding with explicit `resolved`, `partial`, `not_found`, and `source_error` states, and a manual year/make/model fallback. A single decoded equipment candidate may be carried forward; multiple engine, transmission, or drivetrain candidates always require an explicit owner selection. vPIC data identifies manufacturer-reported possibilities and must not be presented as proof of installed equipment.

`OnboardingService` adds vehicles, initial mileage/in-service date, and normal/severe/unknown usage answers, plus garage list/rename/safe-delete operations. VINs are stored as randomized authenticated ciphertext, a keyed lookup fingerprint, and last four only. Construct `VinProtector` with an application secret of at least 32 random bytes supplied by the deployment secret manager; never store that secret in the database or repository. Decryption is deliberately unavailable without that secret.

## Maintenance timeline engine

`burnoutboyz.timeline.evaluate_rule` deterministically evaluates one exact provider/version/severity rule against an immutable vehicle snapshot and confirmed service evidence. It supports mileage-only, time-only, whichever-first, both-dimensions, one-time, repeating, initial-offset, and provider-tolerance semantics. Results keep elapsed expected and confirmed counts separate; elapsed intervals without evidence remain `unknown` or `overdue`, never completed. Each result carries provider/version/source, assumptions, confidence, generic-fallback labeling, occurrences, and next due mileage/date. Confirmations attributed to another schedule version are not silently reused after a schedule change.

Schedule imports may set `recurrence` (`repeating` or `one_time`), `mileage_tolerance`, and `time_tolerance_days`; omitted values default to repeating and zero tolerance. The engine is dependency-free and covered by synthetic tests only—fixture intervals are not vehicle advice.

## Owner-confirmed maintenance records

`burnoutboyz.maintenance.MaintenanceService` records only owner-confirmed work. A record includes its date, odometer, one or more service items, parts, fluids, shop, notes, itemized costs, and SHA-256-verified receipt evidence. Deterministic fingerprints make repeated single-entry and bulk-history imports report duplicates instead of silently creating them. Evidence edits retain an audit snapshot and replace obsolete receipt files.

Per-vehicle reminder preferences control channels and mileage/date lead windows. Notification generation labels expected work as upcoming or overdue but never creates a service confirmation or treats elapsed work as completed. Annual summaries group costs by currency and type. Versioned JSON export covers identity, mileage, usage, expected occurrences, reminders, recalls, connected observations, service details, costs, and receipt metadata; complete vehicle deletion removes those database rows and receipt files while retaining a minimal deletion-lineage audit.

## Mobile-first owner's-manual UX

`burnoutboyz.ux.OwnersManualUXService` turns the provenance backend into renderable mobile-first view models for the product experience. `garage_dashboard(user_id)` supports multi-vehicle garage cards with due-now, upcoming, unknown, history and recall counts. `vehicle_manual(vehicle_id)` returns bottom-tab-friendly sections for due-now, upcoming, service history, recalls and sources, plus source/confidence drill-downs, severe-use plain-language explanation, add-service flow fields, mileage-update fields, accessible reminder copy, connected-data status, and offline/error states.

The UX layer intentionally keeps expected-versus-confirmed counts separate: elapsed intervals never become completed work without owner evidence, model-level recalls are labeled with VIN caveats, connected data remains optional, and all copy is framed as helpful planning rather than fear-based upselling.

## Initial official data sources

- NHTSA vPIC: https://www.nhtsa.gov/cars/rules/manufacture
- NHTSA datasets and recalls APIs: https://www.nhtsa.gov/nhtsa-datasets-and-apis
- FuelEconomy.gov web services: https://www.fueleconomy.gov/feg/ws/

A complete OEM maintenance schedule will require licensed schedule data, manufacturer-authorized sources, or user-supplied manual data. BurnoutBoyz must label the source and confidence of every interval.

## Safety recalls and connected data

`RecallService` refreshes official NHTSA year/make/model campaign data, records the check time and NHTSA report-received date, and keeps completion status `unknown`. Model-level results do not establish that a particular VIN is affected or that the repair remains open; direct owners to NHTSA or the manufacturer for VIN-specific confirmation. A failed refresh is recorded without deleting the last successful result.

`ConnectedVehicleService` is the optional, provider-neutral owner-consent boundary for officially supported vehicle APIs. It permits only odometer, oil-life and DTC signals, requires explicit consent, stores provider compatibility labels, rate-limits refreshes, supports token-clearing revocation, and ignores ungranted data. DTCs are reported codes rather than diagnoses, and oil-life values do not prove service. Manual mileage entry remains available without any connected account.

Smartcar is the evaluated initial adapter target because its official Connect flow provides owner permission controls and its API documents vehicle connections, disconnection, odometer and other signals. Production enablement still requires a configured Smartcar application, encrypted token handling, and per-vehicle/region/scope compatibility checks; this repository deliberately does not claim universal support or ship credentials. See https://smartcar.com/docs/api-reference/intro and https://smartcar.com/product/signals.
