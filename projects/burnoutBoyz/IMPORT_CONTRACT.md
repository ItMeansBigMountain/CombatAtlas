# Schedule import contract v1

BurnoutBoyz imports provider data only through a versioned JSON bundle. `fixtures/synthetic_schedule.json` is the executable example and is explicitly not real maintenance guidance.

Required top-level objects: `provider`, `schedule`, `items`, `rules`.

Every provider requires a stable external ID, display name, source type, and license classification. Every immutable schedule version requires an external version, source URL, retrieval timestamp, effective date, region/applicability object, and confidence. Each rule references an item by external ID and declares trigger mode (`mileage_only`, `time_only`, `whichever_first`, `both`), usage severity (`normal`, `severe`, `all`), explicit applicability JSON, confidence, and the corresponding mileage/time values.

Imports are transactional and idempotent by provider/version/item/rule external IDs. Missing provenance, unsupported enum values, dangling item references, or trigger/value mismatches fail the complete bundle. Provider schedule versions are immutable after publication; corrections use a new `external_version`.

Run:

    python3 -m burnoutboyz.admin --database ./burnoutboyz.db migrate
    python3 -m burnoutboyz.admin --database ./burnoutboyz.db import-schedule fixtures/synthetic_schedule.json
    python3 -m burnoutboyz.admin --database ./burnoutboyz.db schema-status

The synthetic fixture must never be relabeled or displayed as OEM guidance.
