ALTER TABLE service_records ADD COLUMN shop_name TEXT;
ALTER TABLE service_records ADD COLUMN duplicate_fingerprint TEXT;
CREATE UNIQUE INDEX idx_service_record_fingerprint ON service_records(vehicle_id, duplicate_fingerprint) WHERE deleted_at IS NULL;

CREATE TABLE service_record_items (
  service_record_id TEXT NOT NULL REFERENCES service_records(id) ON DELETE CASCADE,
  service_item_id TEXT NOT NULL REFERENCES service_items(id),
  PRIMARY KEY(service_record_id, service_item_id)
);
CREATE TABLE service_record_details (
  service_record_id TEXT PRIMARY KEY REFERENCES service_records(id) ON DELETE CASCADE,
  parts_json TEXT NOT NULL DEFAULT '[]', fluids_json TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE service_record_revisions (
  id TEXT PRIMARY KEY, service_record_id TEXT NOT NULL REFERENCES service_records(id) ON DELETE CASCADE,
  snapshot_json TEXT NOT NULL, reason TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE reminder_preferences (
  vehicle_id TEXT PRIMARY KEY REFERENCES vehicles(id) ON DELETE CASCADE,
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1)), channels_json TEXT NOT NULL,
  lead_days INTEGER NOT NULL CHECK(lead_days >= 0), lead_miles INTEGER NOT NULL CHECK(lead_miles >= 0), updated_at TEXT NOT NULL
);
