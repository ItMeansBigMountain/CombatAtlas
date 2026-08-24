# Durable backend bindings and recovery

## Local deterministic adapter

`DurableBackend` is a container-free, crash-safe local/test adapter. It serializes transactions, writes mode-0600 snapshots through atomic rename, records the schema revision, namespaces every record by tenant, and persists consumed OAuth-state tombstones. It is not the production database and does not claim multi-process locking.

Run the focused integration/concurrency suite:

```text
npm run test -w @tweet-between-the-lines/api
```

## Production PostgreSQL binding

- PostgreSQL: `apps/api/src/postgres.ts` binds the repository contract to `apps/api/migrations/001_durable_backend.sql`. Every operation sets transaction-local `app.tenant_id`; the migration forces RLS and idempotently installs tenant policies. Job claims use `FOR UPDATE SKIP LOCKED`. OAuth consumption is one conditional `UPDATE ... RETURNING` transaction.
- Queue: use the `DurableJobQueue` state machine with a PostgreSQL outbox or a managed queue whose message carries only job ID and tenant routing metadata. Database state remains authoritative. Retry with bounded exponential backoff; reconcile expired leases; cancellation and source revocation must be checked immediately before each side effect.
- KMS: implement `KeyProvider` with a managed KMS/HSM envelope key. Store only key ID and encrypted token metadata in PostgreSQL; never persist plaintext tokens, local keys, or credentials.
- Archive scanning/sandbox: implement `MalwareScanner` and `ArchiveSandbox` independently. The `GuardedArchiveAdapter` refuses extraction if either capability is absent/unavailable. The sandbox must be unprivileged, read-only, network-denied, CPU/memory/time bounded, and preserve the existing path, zip-bomb, entry-size, digest, MIME/magic, and schema gates.

The dedicated `apps/api/tests/postgres.integration.test.ts` suite requires a non-superuser application URL in `TEST_DATABASE_URL`; `TEST_DATABASE_ADMIN_URL` is used only for migrations and fixture cleanup. It runs the migration twice and verifies cross-tenant RLS, a 20-connection one-winner OAuth race, durable table persistence, concurrent claims, lease recovery, and cancellation with synthetic fixtures.

Local evidence used the `embedded-postgres` development dependency because Docker was installed but its daemon was unavailable. This is a real PostgreSQL server, but is not managed-database, KMS, provider, backup/restore, or deployment evidence.

## Exact migration commands

Apply in a disposable/staging database first:

```text
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f apps/api/migrations/001_durable_backend.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT to_regclass('public.durable_jobs'), to_regclass('public.oauth_states');"
```

Run the dedicated test after creating a non-superuser, non-`BYPASSRLS` application role and granting it DML access:

```text
npm run build -w @tweet-between-the-lines/api
TEST_DATABASE_ADMIN_URL='postgresql://<admin>@127.0.0.1:<port>/<db>' TEST_DATABASE_URL='postgresql://<app>@127.0.0.1:<port>/<db>' node --test apps/api/dist/tests/postgres.integration.test.js
```

## Worker and reconciliation contract

1. Enqueue transactionally with `(tenant_id, idempotency_key)` uniqueness.
2. Claim one queued job using `FOR UPDATE SKIP LOCKED`, increment attempts, and set a bounded lease.
3. Re-check cancellation/revocation after claim and before external or destructive effects.
4. On transient failure, clear the lease and requeue only while `attempts < max_attempts`; otherwise mark failed.
5. A periodic reconciler requeues or fails expired leases. Completion writes durable status before acknowledging the managed-queue message.

## Recovery commands

Stop API/worker writers before file-adapter recovery. Preserve the damaged file for forensics, validate JSON, then reopen it through tests:

```text
cp "$DURABLE_BACKEND_FILE" "$DURABLE_BACKEND_FILE.recovery-copy"
node -e "JSON.parse(require('node:fs').readFileSync(process.env.DURABLE_BACKEND_FILE,'utf8')); console.log('json-ok')"
npm run test -w @tweet-between-the-lines/api
```

For PostgreSQL, use provider-native point-in-time recovery into a new instance; never restore over the only copy. Then run:

```text
psql "$RECOVERY_DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT status, count(*) FROM durable_jobs GROUP BY status ORDER BY status;"
psql "$RECOVERY_DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT count(*) FROM oauth_states WHERE consumed_at IS NULL AND expires_at > now();"
```

Reconcile expired leases before enabling workers. Production restore, backup integrity, KMS decryptability, malware-service availability, and sandbox behavior remain blocked until independently exercised with real infrastructure.
