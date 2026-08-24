BEGIN;

CREATE TABLE IF NOT EXISTS oauth_states (
  tenant_id text NOT NULL, subject_id text NOT NULL, provider text NOT NULL, state_hash text NOT NULL,
  encrypted_verifier jsonb NOT NULL, redirect_uri text NOT NULL, scopes jsonb NOT NULL, expires_at timestamptz NOT NULL,
  consumed_at timestamptz, PRIMARY KEY (tenant_id, subject_id, provider, state_hash)
);
CREATE UNIQUE INDEX IF NOT EXISTS oauth_state_once ON oauth_states (tenant_id, provider, state_hash);

CREATE TABLE IF NOT EXISTS token_metadata (
  tenant_id text NOT NULL, subject_id text NOT NULL, vault_ref text NOT NULL, provider text NOT NULL,
  key_id text NOT NULL, scopes jsonb NOT NULL, created_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, vault_ref)
);
CREATE TABLE IF NOT EXISTS consent_receipts (tenant_id text NOT NULL, subject_id text NOT NULL, id text NOT NULL, payload jsonb NOT NULL, created_at timestamptz NOT NULL, revoked_at timestamptz, PRIMARY KEY (tenant_id, id));
CREATE TABLE IF NOT EXISTS durable_jobs (
  tenant_id text NOT NULL, subject_id text NOT NULL, id uuid NOT NULL, kind text NOT NULL, idempotency_key text NOT NULL,
  status text NOT NULL CHECK (status IN ('queued','running','succeeded','failed','cancelled')), attempts integer NOT NULL DEFAULT 0,
  max_attempts integer NOT NULL, lease_owner text, lease_expires_at timestamptz, last_error text, payload jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, id), UNIQUE (tenant_id, idempotency_key)
);
CREATE INDEX IF NOT EXISTS durable_jobs_claim ON durable_jobs (status, created_at) WHERE status = 'queued';
CREATE TABLE IF NOT EXISTS corrections (tenant_id text NOT NULL, subject_id text NOT NULL, id text NOT NULL, payload jsonb NOT NULL, created_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, id));
CREATE TABLE IF NOT EXISTS privacy_exports (tenant_id text NOT NULL, subject_id text NOT NULL, id uuid NOT NULL, status text NOT NULL, digest text, created_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, id));
CREATE TABLE IF NOT EXISTS privacy_deletions (tenant_id text NOT NULL, subject_id text NOT NULL, id uuid NOT NULL, idempotency_key text NOT NULL, status text NOT NULL, created_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, id), UNIQUE (tenant_id, idempotency_key));
CREATE TABLE IF NOT EXISTS audit_events (tenant_id text NOT NULL, id uuid NOT NULL, actor_class text NOT NULL, action text NOT NULL, target_ref text NOT NULL, decision text NOT NULL, outcome text NOT NULL, occurred_at timestamptz NOT NULL, PRIMARY KEY (tenant_id, id));

ALTER TABLE oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE token_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE consent_receipts ENABLE ROW LEVEL SECURITY;
ALTER TABLE durable_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE corrections ENABLE ROW LEVEL SECURITY;
ALTER TABLE privacy_exports ENABLE ROW LEVEL SECURITY;
ALTER TABLE privacy_deletions ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;

ALTER TABLE oauth_states FORCE ROW LEVEL SECURITY;
ALTER TABLE token_metadata FORCE ROW LEVEL SECURITY;
ALTER TABLE consent_receipts FORCE ROW LEVEL SECURITY;
ALTER TABLE durable_jobs FORCE ROW LEVEL SECURITY;
ALTER TABLE corrections FORCE ROW LEVEL SECURITY;
ALTER TABLE privacy_exports FORCE ROW LEVEL SECURITY;
ALTER TABLE privacy_deletions FORCE ROW LEVEL SECURITY;
ALTER TABLE audit_events FORCE ROW LEVEL SECURITY;

DO $policies$
DECLARE table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY['oauth_states','token_metadata','consent_receipts','durable_jobs','corrections','privacy_exports','privacy_deletions','audit_events']
  LOOP
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE schemaname = current_schema() AND tablename = table_name AND policyname = 'tenant_isolation') THEN
      EXECUTE format('CREATE POLICY tenant_isolation ON %I USING (tenant_id = current_setting(''app.tenant_id'', true)) WITH CHECK (tenant_id = current_setting(''app.tenant_id'', true))', table_name);
    END IF;
  END LOOP;
END
$policies$;

COMMIT;
