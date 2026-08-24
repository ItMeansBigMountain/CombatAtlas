import test from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

import { DurableBackend, DurableJobQueue, GuardedArchiveAdapter } from '../src/durable.js'

async function fixture() {
  const directory = await mkdtemp(join(tmpdir(), 'tbtl-durable-'))
  return { directory, file: join(directory, 'backend.json'), cleanup: () => rm(directory, { recursive: true, force: true }) }
}

test('durable backend migrates and atomically rejects OAuth replay under concurrency', async () => {
  const f = await fixture()
  try {
    const store = await DurableBackend.open(f.file)
    await store.put('oauthStates', 'state-1', { tenantId: 'tenant-a', subjectId: 'user-1', verifier: 'secret' })
    const results = await Promise.allSettled(Array.from({ length: 20 }, () => store.consumeOAuthState('tenant-a', 'user-1', 'state-1')))
    assert.equal(results.filter((result) => result.status === 'fulfilled').length, 1)
    assert.equal(results.filter((result) => result.status === 'rejected').length, 19)
    const reopened = await DurableBackend.open(f.file)
    await assert.rejects(reopened.consumeOAuthState('tenant-a', 'user-1', 'state-1'), /consumed/)
    assert.equal((await reopened.snapshot()).schemaVersion, 1)
  } finally { await f.cleanup() }
})

test('durable records are tenant isolated across all production tables', async () => {
  const f = await fixture()
  try {
    const store = await DurableBackend.open(f.file)
    const tables = ['tokenMetadata', 'consents', 'jobs', 'corrections', 'exports', 'deletions', 'audits'] as const
    for (const table of tables) {
      await store.put(table, 'same-id', { tenantId: 'tenant-a', subjectId: 'user-1', value: `a-${table}` })
      await store.put(table, 'same-id', { tenantId: 'tenant-b', subjectId: 'user-2', value: `b-${table}` })
      assert.equal((await store.get(table, 'tenant-a', 'same-id'))?.value, `a-${table}`)
      assert.equal((await store.list(table, 'tenant-a')).some((row) => row.tenantId === 'tenant-b'), false)
    }
  } finally { await f.cleanup() }
})

test('durable queue supports idempotency, leases, retry, cancellation, and reconciliation', async () => {
  const f = await fixture()
  try {
    const store = await DurableBackend.open(f.file)
    const queue = new DurableJobQueue(store, () => '2026-08-24T06:00:00.000Z')
    const first = await queue.enqueue({ tenantId: 'tenant-a', subjectId: 'user-1', kind: 'archive-import', idempotencyKey: 'fixture-1', maxAttempts: 2 })
    assert.equal((await queue.enqueue({ tenantId: 'tenant-a', subjectId: 'user-1', kind: 'archive-import', idempotencyKey: 'fixture-1', maxAttempts: 2 })).id, first.id)
    const leased = await queue.lease('worker-1', 30_000)
    assert.equal(leased?.status, 'running')
    assert.equal((await queue.fail(first.id, 'worker-1', 'synthetic failure')).status, 'queued')
    await queue.lease('worker-1', 30_000)
    assert.equal((await queue.fail(first.id, 'worker-1', 'synthetic failure')).status, 'failed')
    const cancelled = await queue.enqueue({ tenantId: 'tenant-a', subjectId: 'user-1', kind: 'deletion', idempotencyKey: 'fixture-2', maxAttempts: 1 })
    assert.equal((await queue.cancel(cancelled.id, 'tenant-a')).status, 'cancelled')
    const completed = await queue.enqueue({ tenantId: 'tenant-a', subjectId: 'user-1', kind: 'export', idempotencyKey: 'fixture-3', maxAttempts: 1 })
    await queue.lease('worker-2', 30_000)
    assert.equal((await queue.succeed(completed.id, 'worker-2')).status, 'succeeded')
    const revoked = await queue.enqueue({ tenantId: 'tenant-a', subjectId: 'user-1', kind: 'sync', idempotencyKey: 'fixture-4', maxAttempts: 1 })
    assert.deepEqual((await queue.revokeSubject('tenant-a', 'user-1')).map((job) => job.id), [revoked.id])
    assert.equal((await queue.reconcileExpiredLeases()).length, 0)
  } finally { await f.cleanup() }
})

test('archive adapter fails closed without scanner or sandbox and delegates only after both approve', async () => {
  const archive = { format: 'zip' as const, compressedBytes: 100, malwareScan: 'clean' as const, entries: [{ path: 'data.json', compressedBytes: 100, uncompressedBytes: 200, kind: 'file' as const, mime: 'application/json', magic: 'json', sha256: 'a'.repeat(64) }] }
  await assert.rejects(new GuardedArchiveAdapter().inspectAndExtract(archive), /scanner capability unavailable/)
  await assert.rejects(new GuardedArchiveAdapter({ scanner: { scan: async () => 'clean' } }).inspectAndExtract(archive), /sandbox capability unavailable/)
  const adapter = new GuardedArchiveAdapter({ scanner: { scan: async () => 'clean' }, sandbox: { extract: async (_archive, inspection) => ({ files: inspection.entryCount }) } })
  assert.deepEqual(await adapter.inspectAndExtract(archive), { files: 1 })
  const infected = new GuardedArchiveAdapter({ scanner: { scan: async () => 'infected' }, sandbox: { extract: async () => ({ files: 0 }) } })
  await assert.rejects(infected.inspectAndExtract(archive), /malware scan/)
})
