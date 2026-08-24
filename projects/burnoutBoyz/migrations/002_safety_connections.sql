ALTER TABLE connected_accounts ADD COLUMN consented_at TEXT;
ALTER TABLE connected_accounts ADD COLUMN consent_version TEXT;
ALTER TABLE connected_accounts ADD COLUMN last_refreshed_at TEXT;

CREATE TABLE connected_vehicle_links (
  connection_id TEXT NOT NULL REFERENCES connected_accounts(id),
  vehicle_id TEXT NOT NULL REFERENCES vehicles(id),
  compatibility_status TEXT NOT NULL CHECK(compatibility_status IN ('compatible','incompatible','unknown')),
  compatibility_label TEXT NOT NULL,
  linked_at TEXT NOT NULL,
  PRIMARY KEY(connection_id, vehicle_id)
);

CREATE TABLE connected_signal_observations (
  id TEXT PRIMARY KEY,
  connection_id TEXT NOT NULL REFERENCES connected_accounts(id),
  vehicle_id TEXT NOT NULL REFERENCES vehicles(id),
  signal_type TEXT NOT NULL CHECK(signal_type IN ('oil_life','dtc')),
  value_json TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  caveat TEXT NOT NULL
);

CREATE TABLE recall_refreshes (
  id TEXT PRIMARY KEY,
  vehicle_id TEXT NOT NULL REFERENCES vehicles(id),
  lookup_basis TEXT NOT NULL CHECK(lookup_basis IN ('year_make_model')),
  state TEXT NOT NULL CHECK(state IN ('resolved','not_found','source_error')),
  source_uri TEXT NOT NULL,
  checked_at TEXT NOT NULL,
  caveat TEXT NOT NULL,
  error TEXT
);
