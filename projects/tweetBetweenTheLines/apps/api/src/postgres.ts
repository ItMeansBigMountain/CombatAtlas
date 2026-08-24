import { randomUUID } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

import pg from 'pg'

const { Pool } = pg
const TABLES = ['oauth_states', 'token_metadata', 'consent_receipts', 'durable_jobs', 'corrections', 'privacy_exports', 'privacy_deletions', 'audit_events'] as const
export type PostgresTable = typeof TABLES[number]
type JobStatus = 'queued' | 'running' | 'succeeded' | 'failed' | 'cancelled'
export type PostgresJob = { id: string; status: JobStatus; attempts: number; maxAttempts: number; leaseOwner: string | null; leaseExpiresAt: string | null }

export class PostgresBackend {
  private constructor(private readonly pool: pg.Pool) {}
  static async connect(connectionString: string): Promise<PostgresBackend> { return new PostgresBackend(new Pool({ connectionString, max: 20 })) }
  forTenant(tenantId: string): PostgresTenantRepository {
    if (!tenantId.trim()) throw new Error('Tenant ID is required')
    return new PostgresTenantRepository(this.pool, tenantId)
  }
  async migrate(): Promise<void> {
    const source = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'migrations', '001_durable_backend.sql')
    const fallback = join(process.cwd(), 'apps', 'api', 'migrations', '001_durable_backend.sql')
    let sql: string
    try { sql = await readFile(source, 'utf8') } catch { sql = await readFile(fallback, 'utf8') }
    await this.pool.query(sql)
  }
  async resetSyntheticFixtures(): Promise<void> {
    for (const table of [...TABLES].reverse()) await this.pool.query(`DELETE FROM ${table}`)
  }
  async close(): Promise<void> { await this.pool.end() }
}

export class PostgresTenantRepository {
  constructor(private readonly pool: pg.Pool, private readonly tenantId: string) {}
  private async transaction<T>(operation: (client: pg.PoolClient) => Promise<T>): Promise<T> {
    const client = await this.pool.connect()
    try {
      await client.query('BEGIN')
      await client.query("SELECT set_config('app.tenant_id', $1, true)", [this.tenantId])
      const result = await operation(client)
      await client.query('COMMIT')
      return result
    } catch (error) { await client.query('ROLLBACK'); throw error } finally { client.release() }
  }
  async list(table: PostgresTable): Promise<Record<string, unknown>[]> {
    if (!TABLES.includes(table)) throw new Error('Unsupported table')
    return this.transaction(async (client) => (await client.query(`SELECT * FROM ${table} ORDER BY tenant_id`)).rows)
  }
  async putOAuthState(input: { subjectId: string; provider: string; stateHash: string; encryptedVerifier: object; redirectUri: string; scopes: string[]; expiresAt: string }): Promise<void> {
    await this.transaction(async (client) => { await client.query('INSERT INTO oauth_states (tenant_id,subject_id,provider,state_hash,encrypted_verifier,redirect_uri,scopes,expires_at) VALUES ($1,$2,$3,$4,$5,$6,$7::jsonb,$8)', [this.tenantId, input.subjectId, input.provider, input.stateHash, input.encryptedVerifier, input.redirectUri, JSON.stringify(input.scopes), input.expiresAt]) })
  }
  async consumeOAuthState(subjectId: string, provider: string, stateHash: string): Promise<Record<string, unknown>> {
    return this.transaction(async (client) => {
      const result = await client.query('UPDATE oauth_states SET consumed_at = now() WHERE tenant_id=$1 AND subject_id=$2 AND provider=$3 AND state_hash=$4 AND consumed_at IS NULL AND expires_at > now() RETURNING *', [this.tenantId, subjectId, provider, stateHash])
      if (result.rowCount !== 1) throw new Error('OAuth state unavailable or already consumed')
      return result.rows[0] as Record<string, unknown>
    })
  }
  async insertSynthetic(table: Exclude<PostgresTable, 'oauth_states' | 'durable_jobs'>, subjectId: string): Promise<void> {
    const id = randomUUID(); const now = new Date().toISOString()
    const statements: Record<string, [string, unknown[]]> = {
      token_metadata: ['INSERT INTO token_metadata VALUES ($1,$2,$3,$4,$5,$6::jsonb,$7)', [this.tenantId, subjectId, `vault-${id}`, 'x', 'synthetic-key', '[]', now]],
      consent_receipts: ['INSERT INTO consent_receipts VALUES ($1,$2,$3,$4,$5,NULL)', [this.tenantId, subjectId, id, { synthetic: true }, now]],
      corrections: ['INSERT INTO corrections VALUES ($1,$2,$3,$4,$5)', [this.tenantId, subjectId, id, { synthetic: true }, now]],
      privacy_exports: ['INSERT INTO privacy_exports VALUES ($1,$2,$3,$4,$5,$6)', [this.tenantId, subjectId, id, 'ready', 'synthetic-digest', now]],
      privacy_deletions: ['INSERT INTO privacy_deletions VALUES ($1,$2,$3,$4,$5,$6)', [this.tenantId, subjectId, id, `delete-${id}`, 'queued', now]],
      audit_events: ['INSERT INTO audit_events VALUES ($1,$2,$3,$4,$5,$6,$7,$8)', [this.tenantId, id, 'system', 'synthetic-test', 'fixture', 'allow', 'succeeded', now]],
    }
    const [sql, values] = statements[table]!
    await this.transaction(async (client) => { await client.query(sql, values) })
  }
  async enqueueJob(input: { subjectId: string; kind: string; idempotencyKey: string; maxAttempts: number; payload: object }): Promise<{ id: string }> {
    if (!Number.isInteger(input.maxAttempts) || input.maxAttempts < 1) throw new Error('maxAttempts must be a positive integer')
    return this.transaction(async (client) => {
      const id = randomUUID(); const result = await client.query("INSERT INTO durable_jobs (tenant_id,subject_id,id,kind,idempotency_key,status,max_attempts,payload,created_at,updated_at) VALUES ($1,$2,$3,$4,$5,'queued',$6,$7,now(),now()) ON CONFLICT (tenant_id,idempotency_key) DO UPDATE SET updated_at=durable_jobs.updated_at RETURNING id", [this.tenantId, input.subjectId, id, input.kind, input.idempotencyKey, input.maxAttempts, input.payload])
      return { id: String(result.rows[0].id) }
    })
  }
  async claimJob(workerId: string, leaseMs: number): Promise<(PostgresJob & { id: string }) | undefined> {
    if (!Number.isFinite(leaseMs) || leaseMs < 1) throw new Error('leaseMs must be positive')
    return this.transaction(async (client) => {
      const result = await client.query("WITH candidate AS (SELECT id FROM durable_jobs WHERE tenant_id=$1 AND (status='queued' OR (status='running' AND lease_expires_at < now())) AND attempts < max_attempts ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT 1) UPDATE durable_jobs j SET status='running', attempts=j.attempts+1, lease_owner=$2, lease_expires_at=now()+($3 * interval '1 millisecond'), updated_at=now() FROM candidate WHERE j.tenant_id=$1 AND j.id=candidate.id RETURNING j.id,j.status,j.attempts,j.max_attempts AS \"maxAttempts\",j.lease_owner AS \"leaseOwner\",j.lease_expires_at AS \"leaseExpiresAt\"", [this.tenantId, workerId, leaseMs])
      return result.rows[0] as PostgresJob | undefined
    })
  }
  async renewLease(id: string, workerId: string, leaseMs: number): Promise<void> {
    if (!Number.isFinite(leaseMs) || leaseMs < 1) throw new Error('leaseMs must be positive')
    await this.ownedLeaseTransition(id, workerId, "lease_expires_at=now()+($4 * interval '1 millisecond'),updated_at=now()", leaseMs)
  }
  async succeedJob(id: string, workerId: string): Promise<void> { await this.ownedLeaseTransition(id, workerId, "status='succeeded',lease_owner=NULL,lease_expires_at=NULL,updated_at=now()") }
  async failJob(id: string, workerId: string, message: string): Promise<void> {
    await this.transaction(async (client) => {
      const result = await client.query("UPDATE durable_jobs SET status=CASE WHEN attempts < max_attempts THEN 'queued' ELSE 'failed' END,lease_owner=NULL,lease_expires_at=NULL,last_error=$3,updated_at=now() WHERE tenant_id=$1 AND id=$2 AND status='running' AND lease_owner=$4", [this.tenantId, id, message.slice(0, 256), workerId])
      if (result.rowCount !== 1) throw new Error('Job lease not owned')
    })
  }
  private async ownedLeaseTransition(id: string, workerId: string, assignment: string, leaseMs = 0): Promise<void> {
    await this.transaction(async (client) => {
      const values = leaseMs > 0 ? [this.tenantId, id, workerId, leaseMs] : [this.tenantId, id, workerId]
      const result = await client.query(`UPDATE durable_jobs SET ${assignment} WHERE tenant_id=$1 AND id=$2 AND status='running' AND lease_owner=$3`, values)
      if (result.rowCount !== 1) throw new Error('Job lease not owned')
    })
  }
  async reconcileExpiredLeases(): Promise<number> {
    return this.transaction(async (client) => (await client.query("UPDATE durable_jobs SET status=CASE WHEN attempts < max_attempts THEN 'queued' ELSE 'failed' END, lease_owner=NULL, lease_expires_at=NULL, last_error='worker lease expired', updated_at=now() WHERE tenant_id=$1 AND status='running' AND lease_expires_at < now()", [this.tenantId])).rowCount ?? 0)
  }
  async cancelJob(id: string): Promise<void> { await this.transaction(async (client) => { await client.query("UPDATE durable_jobs SET status='cancelled',lease_owner=NULL,lease_expires_at=NULL,updated_at=now() WHERE tenant_id=$1 AND id=$2 AND status IN ('queued','running')", [this.tenantId, id]) }) }
  async revokeSubject(subjectId: string): Promise<number> { return this.transaction(async (client) => (await client.query("UPDATE durable_jobs SET status='cancelled',lease_owner=NULL,lease_expires_at=NULL,updated_at=now() WHERE tenant_id=$1 AND subject_id=$2 AND status IN ('queued','running')", [this.tenantId, subjectId])).rowCount ?? 0) }
  async getJob(id: string): Promise<PostgresJob | undefined> { return this.transaction(async (client) => (await client.query('SELECT id,status,attempts,max_attempts AS "maxAttempts",lease_owner AS "leaseOwner",lease_expires_at AS "leaseExpiresAt" FROM durable_jobs WHERE tenant_id=$1 AND id=$2', [this.tenantId, id])).rows[0] as PostgresJob | undefined) }
}
