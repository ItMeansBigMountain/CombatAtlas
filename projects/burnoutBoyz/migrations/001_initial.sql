PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id TEXT PRIMARY KEY, email TEXT UNIQUE, status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','disabled','deleted')),
  created_at TEXT NOT NULL, deleted_at TEXT
);
CREATE TABLE garages (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), name TEXT NOT NULL, created_at TEXT NOT NULL, deleted_at TEXT
);
CREATE TABLE engines (
  id TEXT PRIMARY KEY, external_key TEXT, manufacturer TEXT, family TEXT, displacement_liters REAL, cylinders INTEGER, fuel_type TEXT, attributes_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE transmissions (
  id TEXT PRIMARY KEY, external_key TEXT, manufacturer TEXT, name TEXT, transmission_type TEXT, speeds INTEGER, attributes_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE trims (
  id TEXT PRIMARY KEY, external_key TEXT, make TEXT NOT NULL, model TEXT NOT NULL, model_year INTEGER NOT NULL, name TEXT, body_style TEXT, drivetrain TEXT, attributes_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE provenance_sources (
  id TEXT PRIMARY KEY, source_type TEXT NOT NULL, provider_name TEXT NOT NULL, source_uri TEXT, external_id TEXT, retrieved_at TEXT NOT NULL,
  license_classification TEXT NOT NULL, content_hash TEXT, raw_reference TEXT
);
CREATE TABLE confidence_assessments (
  id TEXT PRIMARY KEY, level TEXT NOT NULL CHECK(level IN ('unknown','low','medium','high','verified')), score REAL CHECK(score IS NULL OR score BETWEEN 0 AND 1),
  rationale TEXT NOT NULL, source_id TEXT REFERENCES provenance_sources(id), created_at TEXT NOT NULL
);
CREATE TABLE vehicle_configurations (
  id TEXT PRIMARY KEY, model_year INTEGER, make TEXT, model TEXT, trim_id TEXT REFERENCES trims(id), engine_id TEXT REFERENCES engines(id),
  transmission_id TEXT REFERENCES transmissions(id), drivetrain TEXT, region TEXT, identity_state TEXT NOT NULL CHECK(identity_state IN ('unresolved','partial','confirmed')),
  source_id TEXT REFERENCES provenance_sources(id), confidence_id TEXT REFERENCES confidence_assessments(id), attributes_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE vehicles (
  id TEXT PRIMARY KEY, garage_id TEXT NOT NULL REFERENCES garages(id), configuration_id TEXT NOT NULL REFERENCES vehicle_configurations(id), nickname TEXT,
  vin_ciphertext BLOB, vin_fingerprint TEXT UNIQUE, vin_last4 TEXT, in_service_date TEXT, acquired_date TEXT, status TEXT NOT NULL DEFAULT 'active', created_at TEXT NOT NULL, deleted_at TEXT
);
CREATE TABLE odometer_observations (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), observed_at TEXT NOT NULL, distance_value INTEGER NOT NULL CHECK(distance_value >= 0),
  distance_unit TEXT NOT NULL CHECK(distance_unit IN ('mi','km')), source_id TEXT REFERENCES provenance_sources(id), confidence_id TEXT REFERENCES confidence_assessments(id), supersedes_id TEXT REFERENCES odometer_observations(id), created_at TEXT NOT NULL
);
CREATE INDEX idx_odometer_vehicle_time ON odometer_observations(vehicle_id, observed_at);
CREATE TABLE usage_profiles (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), severity TEXT NOT NULL CHECK(severity IN ('normal','severe','mixed','unknown')),
  effective_from TEXT NOT NULL, effective_to TEXT, answers_json TEXT NOT NULL, source_id TEXT REFERENCES provenance_sources(id), confidence_id TEXT REFERENCES confidence_assessments(id), created_at TEXT NOT NULL
);
CREATE TABLE schedule_providers (
  id TEXT PRIMARY KEY, external_id TEXT NOT NULL UNIQUE, name TEXT NOT NULL, source_type TEXT NOT NULL, license_classification TEXT NOT NULL, terms_uri TEXT, created_at TEXT NOT NULL
);
CREATE TABLE schedule_versions (
  id TEXT PRIMARY KEY, provider_id TEXT NOT NULL REFERENCES schedule_providers(id), external_version TEXT NOT NULL, source_url TEXT NOT NULL,
  effective_from TEXT NOT NULL, effective_to TEXT, retrieved_at TEXT NOT NULL, region TEXT NOT NULL, applicability_json TEXT NOT NULL,
  license_classification TEXT NOT NULL, confidence TEXT NOT NULL CHECK(confidence IN ('unknown','low','medium','high','verified')), content_hash TEXT NOT NULL,
  created_at TEXT NOT NULL, UNIQUE(provider_id, external_version)
);
CREATE TABLE service_items (
  id TEXT PRIMARY KEY, provider_id TEXT NOT NULL REFERENCES schedule_providers(id), external_id TEXT NOT NULL, name TEXT NOT NULL, category TEXT NOT NULL,
  description TEXT, canonical_key TEXT, UNIQUE(provider_id, external_id)
);
CREATE TABLE interval_rules (
  id TEXT PRIMARY KEY, schedule_version_id TEXT NOT NULL REFERENCES schedule_versions(id), service_item_id TEXT NOT NULL REFERENCES service_items(id), external_id TEXT NOT NULL,
  trigger_mode TEXT NOT NULL CHECK(trigger_mode IN ('mileage_only','time_only','whichever_first','both')),
  mileage_interval INTEGER CHECK(mileage_interval > 0), time_interval_months INTEGER CHECK(time_interval_months > 0), initial_mileage INTEGER CHECK(initial_mileage >= 0), initial_months INTEGER CHECK(initial_months >= 0),
  usage_severity TEXT NOT NULL CHECK(usage_severity IN ('normal','severe','all','unknown')), applicability_json TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK(confidence IN ('unknown','low','medium','high','verified')), source_note TEXT,
  UNIQUE(schedule_version_id, external_id),
  CHECK((trigger_mode='mileage_only' AND mileage_interval IS NOT NULL AND time_interval_months IS NULL) OR
        (trigger_mode='time_only' AND mileage_interval IS NULL AND time_interval_months IS NOT NULL) OR
        (trigger_mode IN ('whichever_first','both') AND mileage_interval IS NOT NULL AND time_interval_months IS NOT NULL))
);
CREATE TABLE expected_occurrences (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), interval_rule_id TEXT NOT NULL REFERENCES interval_rules(id), ordinal INTEGER NOT NULL CHECK(ordinal > 0),
  due_mileage INTEGER, due_date TEXT, state TEXT NOT NULL CHECK(state IN ('expected','unknown','overdue','not_applicable','superseded')),
  calculated_at TEXT NOT NULL, assumptions_json TEXT NOT NULL, UNIQUE(vehicle_id, interval_rule_id, ordinal)
);
CREATE TABLE service_records (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), service_item_id TEXT NOT NULL REFERENCES service_items(id), performed_at TEXT NOT NULL,
  odometer_value INTEGER CHECK(odometer_value IS NULL OR odometer_value >= 0), odometer_unit TEXT CHECK(odometer_unit IS NULL OR odometer_unit IN ('mi','km')),
  status TEXT NOT NULL CHECK(status IN ('confirmed','claimed','disputed','voided')), matched_expected_occurrence_id TEXT REFERENCES expected_occurrences(id),
  provider_name TEXT, notes TEXT, source_id TEXT REFERENCES provenance_sources(id), confidence_id TEXT REFERENCES confidence_assessments(id), created_at TEXT NOT NULL, deleted_at TEXT
);
CREATE TABLE receipts (
  id TEXT PRIMARY KEY, service_record_id TEXT NOT NULL REFERENCES service_records(id), storage_key TEXT NOT NULL, media_type TEXT, original_filename TEXT,
  sha256 TEXT NOT NULL, source_id TEXT REFERENCES provenance_sources(id), created_at TEXT NOT NULL, deleted_at TEXT
);
CREATE TABLE service_costs (
  id TEXT PRIMARY KEY, service_record_id TEXT NOT NULL REFERENCES service_records(id), amount_minor INTEGER NOT NULL CHECK(amount_minor >= 0), currency TEXT NOT NULL,
  cost_type TEXT NOT NULL CHECK(cost_type IN ('parts','labor','tax','fee','total','other')), created_at TEXT NOT NULL
);
CREATE TABLE reminders (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), expected_occurrence_id TEXT REFERENCES expected_occurrences(id), channel TEXT NOT NULL,
  remind_at TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('scheduled','sent','dismissed','cancelled','failed')), settings_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE recalls (
  id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL REFERENCES vehicles(id), campaign_number TEXT NOT NULL, component TEXT, summary TEXT, remedy TEXT,
  report_received_date TEXT, status TEXT NOT NULL CHECK(status IN ('open','remedied','unknown','not_applicable')), source_id TEXT NOT NULL REFERENCES provenance_sources(id),
  checked_at TEXT NOT NULL, UNIQUE(vehicle_id, campaign_number)
);
CREATE TABLE connected_accounts (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), provider TEXT NOT NULL, external_subject TEXT NOT NULL, token_ciphertext BLOB,
  scopes_json TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','revoked','expired','error')), connected_at TEXT NOT NULL, revoked_at TEXT, UNIQUE(provider, external_subject)
);
CREATE TABLE deletion_events (
  id TEXT PRIMARY KEY, requested_by_user_id TEXT REFERENCES users(id), reason TEXT NOT NULL, requested_at TEXT NOT NULL, completed_at TEXT, status TEXT NOT NULL CHECK(status IN ('pending','completed','failed'))
);
CREATE TABLE deletion_lineage (
  id TEXT PRIMARY KEY, deletion_event_id TEXT NOT NULL REFERENCES deletion_events(id), entity_type TEXT NOT NULL, entity_id TEXT NOT NULL,
  action TEXT NOT NULL CHECK(action IN ('tombstoned','anonymized','deleted','retained_legal')), processed_at TEXT NOT NULL, details_json TEXT NOT NULL,
  UNIQUE(deletion_event_id, entity_type, entity_id)
);
