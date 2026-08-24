import test from 'node:test'
import assert from 'node:assert/strict'

import { PostgresBackend } from '../src/postgres.js'

const url = process.env.TEST_DATABASE_URL
const adminUrl = process.env.TEST_DATABASE_ADMIN_URL

test('PostgreSQL adapter enforces RLS, atomic OAuth consumption, persistence, and worker recovery', { skip: !url }, async () => {
  const admin = await PostgresBackend.connect(adminUrl ?? url!)
  await admin.migrate()
  await admin.migrate()
  await admin.resetSyntheticFixtures()

  const repository = adminUrl ? await PostgresBackend.connect(url!) : admin
  const tenantA = repository.forTenant('tenant-a')
  const tenantB = repository.forTenant('tenant-b')
  await tenantA.putOAuthState({ subjectId: 'user-1', provider: 'x', stateHash: 'state-1', encryptedVerifier: { ciphertext: 'synthetic' }, redirectUri: 'https://app.test/callback', scopes: ['tweet.read'], expiresAt: new Date(Date.now() + 60_000).toISOString() })
  assert.equal((await tenantB.list('oauth_states')).length, 0)

  const consumers = await Promise.allSettled(Array.from({ length: 20 }, () => tenantA.consumeOAuthState('user-1', 'x', 'state-1')))
  assert.equal(consumers.filter((result) => result.status === 'fulfilled').length, 1)
  assert.equal(consumers.filter((result) => result.status === 'rejected').length, 19)

  for (const table of ['token_metadata', 'consent_receipts', 'corrections', 'privacy_exports', 'privacy_deletions', 'audit_events'] as const) {
    await tenantA.insertSynthetic(table, 'user-1')
    assert.equal((await tenantA.list(table)).length, 1)
    assert.equal((await tenantB.list(table)).length, 0)
  }

  const job = await tenantA.enqueueJob({ subjectId: 'user-1', kind: 'synthetic', idempotencyKey: 'job-1', maxAttempts: 2, payload: { fixture: true } })
  const [claim1, claim2] = await Promise.all([tenantA.claimJob('worker-1', 1), tenantA.claimJob('worker-2', 1)])
  assert.equal([claim1, claim2].filter(Boolean).length, 1)
  await new Promise((resolve) => setTimeout(resolve, 5))
  assert.equal(await tenantA.reconcileExpiredLeases(), 1)
  assert.equal((await tenantA.claimJob('worker-2', 10_000))?.id, job.id)
  await tenantA.cancelJob(job.id)
  assert.equal((await tenantA.getJob(job.id))?.status, 'cancelled')

  const completed = await tenantA.enqueueJob({ subjectId: 'user-1', kind: 'synthetic', idempotencyKey: 'job-2', maxAttempts: 2, payload: { fixture: true } })
  await tenantA.claimJob('worker-3', 10_000)
  await tenantA.renewLease(completed.id, 'worker-3', 10_000)
  await tenantA.succeedJob(completed.id, 'worker-3')
  assert.equal((await tenantA.getJob(completed.id))?.status, 'succeeded')
  await assert.rejects(tenantA.succeedJob(completed.id, 'worker-other'), /lease not owned/)
  await assert.rejects(tenantA.enqueueJob({ subjectId: 'user-1', kind: 'synthetic', idempotencyKey: 'invalid', maxAttempts: 0, payload: {} }), /maxAttempts/)
  await assert.rejects(tenantA.claimJob('worker-4', 0), /leaseMs/)
  const revoked = await tenantA.enqueueJob({ subjectId: 'user-revoked', kind: 'sync', idempotencyKey: 'job-revoked', maxAttempts: 1, payload: {} })
  assert.equal(await tenantA.revokeSubject('user-revoked'), 1)
  assert.equal((await tenantA.getJob(revoked.id))?.status, 'cancelled')

  await admin.resetSyntheticFixtures()
  if (repository !== admin) await repository.close()
  await admin.close()
})
