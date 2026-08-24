import { randomUUID } from 'node:crypto'
import { mkdir, readFile, rename, writeFile } from 'node:fs/promises'
import { dirname } from 'node:path'

import { inspectArchive, type ArchiveEnvelope } from '@tweet-between-the-lines/domain'

export const DURABLE_TABLES = ['oauthStates', 'tokenMetadata', 'consents', 'jobs', 'corrections', 'exports', 'deletions', 'audits'] as const
export type DurableTable = typeof DURABLE_TABLES[number]
export type DurableRecord = { tenantId: string; subjectId?: string; [key: string]: unknown }
type Database = { schemaVersion: 1; revision: number; tables: Record<DurableTable, Record<string, DurableRecord>>; consumedOAuthStates: Record<string, string> }

function emptyDatabase(): Database {
  return { schemaVersion: 1, revision: 0, tables: Object.fromEntries(DURABLE_TABLES.map((table) => [table, {}])) as Database['tables'], consumedOAuthStates: {} }
}

/** Container-free deterministic persistence adapter. Production binds this contract to PostgreSQL. */
export class DurableBackend {
  private gate: Promise<void> = Promise.resolve()
  private constructor(private readonly file: string, private database: Database) {}

  static async open(file: string): Promise<DurableBackend> {
    await mkdir(dirname(file), { recursive: true })
    let database: Database
    try { database = JSON.parse(await readFile(file, 'utf8')) as Database } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error
      database = emptyDatabase()
      await DurableBackend.persist(file, database)
    }
    if (database.schemaVersion !== 1) throw new Error(`Unsupported durable schema version: ${String(database.schemaVersion)}`)
    return new DurableBackend(file, database)
  }

  private static async persist(file: string, database: Database): Promise<void> {
    const temporary = `${file}.${process.pid}.${randomUUID()}.tmp`
    await writeFile(temporary, `${JSON.stringify(database)}\n`, { encoding: 'utf8', mode: 0o600 })
    await rename(temporary, file)
  }

  private transaction<T>(operation: (draft: Database) => T | Promise<T>): Promise<T> {
    const run = this.gate.then(async () => {
      const draft = structuredClone(this.database)
      const result = await operation(draft)
      draft.revision += 1
      await DurableBackend.persist(this.file, draft)
      this.database = draft
      return structuredClone(result)
    })
    this.gate = run.then(() => undefined, () => undefined)
    return run
  }

  private key(tenantId: string, id: string): string { return `${tenantId}\u0000${id}` }
  async put(table: DurableTable, id: string, record: DurableRecord): Promise<DurableRecord> {
    if (!record.tenantId || !id) throw new Error('Tenant and record ID are required')
    return this.transaction((draft) => { draft.tables[table][this.key(record.tenantId, id)] = structuredClone(record); return record })
  }
  async get(table: DurableTable, tenantId: string, id: string): Promise<DurableRecord | undefined> {
    await this.gate
    const record = this.database.tables[table][this.key(tenantId, id)]
    return record ? structuredClone(record) : undefined
  }
  async list(table: DurableTable, tenantId: string): Promise<DurableRecord[]> {
    await this.gate
    return Object.values(this.database.tables[table]).filter((record) => record.tenantId === tenantId).map((record) => structuredClone(record))
  }
  async consumeOAuthState(tenantId: string, subjectId: string, state: string): Promise<DurableRecord> {
    return this.transaction((draft) => {
      const key = this.key(tenantId, state); const record = draft.tables.oauthStates[key]
      if (!record || record.subjectId !== subjectId) {
        if (draft.consumedOAuthStates[key]) throw new Error('OAuth state already consumed')
        throw new Error('OAuth state not found')
      }
      delete draft.tables.oauthStates[key]
      draft.consumedOAuthStates[key] = new Date().toISOString()
      return record
    })
  }
  async snapshot(): Promise<Database> { await this.gate; return structuredClone(this.database) }
}

export type DurableJob = DurableRecord & { id: string; kind: string; idempotencyKey: string; status: 'queued' | 'running' | 'succeeded' | 'failed' | 'cancelled'; attempts: number; maxAttempts: number; leaseOwner: string | null; leaseExpiresAt: string | null; lastError: string | null; createdAt: string }
export class DurableJobQueue {
  constructor(private readonly store: DurableBackend, private readonly now = () => new Date().toISOString()) {}
  async enqueue(input: { tenantId: string; subjectId: string; kind: string; idempotencyKey: string; maxAttempts: number }): Promise<DurableJob> {
    const existing = (await this.store.list('jobs', input.tenantId)).find((record) => record.idempotencyKey === input.idempotencyKey) as DurableJob | undefined
    if (existing) return existing
    const job: DurableJob = { ...input, id: `job:${randomUUID()}`, status: 'queued', attempts: 0, leaseOwner: null, leaseExpiresAt: null, lastError: null, createdAt: this.now() }
    return await this.store.put('jobs', job.id, job) as DurableJob
  }
  async lease(workerId: string, leaseMs: number): Promise<DurableJob | undefined> {
    const snapshot = await this.store.snapshot()
    const job = Object.values(snapshot.tables.jobs).find((record) => record.status === 'queued') as DurableJob | undefined
    if (!job) return undefined
    const leased = { ...job, status: 'running' as const, attempts: job.attempts + 1, leaseOwner: workerId, leaseExpiresAt: new Date(new Date(this.now()).valueOf() + leaseMs).toISOString() }
    return await this.store.put('jobs', leased.id, leased) as DurableJob
  }
  async fail(id: string, workerId: string, message: string): Promise<DurableJob> {
    const snapshot = await this.store.snapshot(); const job = Object.values(snapshot.tables.jobs).find((record) => record.id === id) as DurableJob | undefined
    if (!job || job.status !== 'running' || job.leaseOwner !== workerId) throw new Error('Job lease not owned')
    const failed = { ...job, status: job.attempts < job.maxAttempts ? 'queued' as const : 'failed' as const, leaseOwner: null, leaseExpiresAt: null, lastError: message.slice(0, 256) }
    return await this.store.put('jobs', id, failed) as DurableJob
  }
  async succeed(id: string, workerId: string): Promise<DurableJob> {
    const snapshot = await this.store.snapshot(); const job = Object.values(snapshot.tables.jobs).find((record) => record.id === id) as DurableJob | undefined
    if (!job || job.status !== 'running' || job.leaseOwner !== workerId) throw new Error('Job lease not owned')
    return await this.store.put('jobs', id, { ...job, status: 'succeeded', leaseOwner: null, leaseExpiresAt: null }) as DurableJob
  }
  async cancel(id: string, tenantId: string): Promise<DurableJob> {
    const job = await this.store.get('jobs', tenantId, id) as DurableJob | undefined
    if (!job) throw new Error('Job not found')
    const cancelled = { ...job, status: 'cancelled' as const, leaseOwner: null, leaseExpiresAt: null }
    return await this.store.put('jobs', id, cancelled) as DurableJob
  }
  async revokeSubject(tenantId: string, subjectId: string): Promise<DurableJob[]> {
    const cancellable = (await this.store.list('jobs', tenantId) as DurableJob[]).filter((job) => job.subjectId === subjectId && (job.status === 'queued' || job.status === 'running'))
    const cancelled: DurableJob[] = []
    for (const job of cancellable) cancelled.push(await this.cancel(job.id, tenantId))
    return cancelled
  }
  async reconcileExpiredLeases(): Promise<DurableJob[]> {
    const snapshot = await this.store.snapshot(); const now = this.now(); const changed: DurableJob[] = []
    for (const record of Object.values(snapshot.tables.jobs) as DurableJob[]) if (record.status === 'running' && record.leaseExpiresAt && record.leaseExpiresAt <= now) {
      changed.push(await this.store.put('jobs', record.id, { ...record, status: record.attempts < record.maxAttempts ? 'queued' : 'failed', leaseOwner: null, leaseExpiresAt: null, lastError: 'worker lease expired' }) as DurableJob)
    }
    return changed
  }
}

export interface MalwareScanner { scan(archive: ArchiveEnvelope): Promise<'clean' | 'infected' | 'unavailable'> }
export interface ArchiveSandbox<T = unknown> { extract(archive: ArchiveEnvelope, inspection: ReturnType<typeof inspectArchive>): Promise<T> }
export class GuardedArchiveAdapter<T = unknown> {
  constructor(private readonly capabilities: { scanner?: MalwareScanner; sandbox?: ArchiveSandbox<T> } = {}) {}
  async inspectAndExtract(archive: ArchiveEnvelope): Promise<T> {
    if (!this.capabilities.scanner) throw new Error('Archive scanner capability unavailable; fail closed')
    if (!this.capabilities.sandbox) throw new Error('Archive sandbox capability unavailable; fail closed')
    const scan = await this.capabilities.scanner.scan(archive)
    if (scan !== 'clean') throw new Error(scan === 'infected' ? 'Archive failed malware scan' : 'Archive malware scan unavailable; fail closed')
    const inspection = inspectArchive({ ...archive, malwareScan: 'clean' })
    return this.capabilities.sandbox.extract(archive, inspection)
  }
}
