import assert from 'node:assert/strict'
import test from 'node:test'
import {
  ArchiveImportStore,
  CONNECTOR_REGISTRY,
  assertConnectorAvailable,
  beginOAuthAuthorization,
  completeOAuthAuthorization,
  createArchiveImportPlan,
  createConnectorRuntime,
  createRateLimitBudget,
  deleteSourceData,
  inspectArchive,
  registerArchiveSchema,
  revokeConnector,
} from '../src/connectors.js'

const context = { tenantId: 'tenant-a', subjectId: 'person-a', actorId: 'person-a', purpose: 'personal-analysis' }

test('official connector registry exposes honest supported and restricted states', () => {
  assert.equal(CONNECTOR_REGISTRY.google_youtube.decision, 'supported_api')
  assert.equal(CONNECTOR_REGISTRY.x_twitter.decision, 'supported_archive_import')
  assert.equal(CONNECTOR_REGISTRY.threads.decision, 'blocked_or_restricted')
  assert.throws(() => assertConnectorAvailable('threads', 'history', { reviewApproved: false, paidTier: false }), /not available/)
  assert.throws(() => assertConnectorAvailable('x_twitter', 'api', { reviewApproved: true, paidTier: false }), /paid tier/)
})

test('OAuth authorization binds one-use PKCE state to tenant subject provider and redirect', () => {
  const pending = beginOAuthAuthorization({
    context,
    provider: 'google_youtube',
    redirectUri: 'https://app.example.test/oauth/google/callback',
    allowedRedirectUris: ['https://app.example.test/oauth/google/callback'],
    requestedScopes: ['openid', 'https://www.googleapis.com/auth/youtube.readonly'],
    now: '2026-08-24T02:00:00Z',
  })
  assert.match(pending.authorizationUrl, /^https:\/\/accounts\.google\.com\/o\/oauth2\/v2\/auth\?/)
  assert.equal(pending.codeChallengeMethod, 'S256')
  const callback = completeOAuthAuthorization(pending, {
    context,
    provider: 'google_youtube',
    redirectUri: 'https://app.example.test/oauth/google/callback',
    state: pending.state,
    grantedScopes: ['openid'],
    now: '2026-08-24T02:02:00Z',
  })
  assert.deepEqual(callback.grantedScopes, ['openid'])
  assert.throws(() => completeOAuthAuthorization(pending, { context, provider: 'google_youtube', redirectUri: pending.redirectUri, state: pending.state, grantedScopes: [], now: '2026-08-24T02:03:00Z' }), /already used/)
})

test('rate limit budget blocks exhaustion and honors reset', () => {
  const budget = createRateLimitBudget({ provider: 'spotify', capacity: 2, resetAt: '2026-08-24T03:00:00Z' })
  assert.equal(budget.consume(2, '2026-08-24T02:30:00Z').remaining, 0)
  assert.throws(() => budget.consume(1, '2026-08-24T02:31:00Z'), /rate limit/)
  assert.equal(budget.consume(1, '2026-08-24T03:00:00Z').remaining, 1)
})

test('archive inspection rejects traversal symlinks malware and expansion bombs', () => {
  const base = { format: 'zip' as const, compressedBytes: 100, malwareScan: 'clean' as const, entries: [{ path: 'data/posts.json', compressedBytes: 50, uncompressedBytes: 500, kind: 'file' as const, mime: 'application/json', magic: 'json', sha256: 'a'.repeat(64) }] }
  assert.equal(inspectArchive(base).accepted, true)
  assert.throws(() => inspectArchive({ ...base, entries: [{ ...base.entries[0], path: '../escape.json' }] }), /path traversal/)
  assert.throws(() => inspectArchive({ ...base, entries: [{ ...base.entries[0], kind: 'symlink' }] }), /not allowed/)
  assert.throws(() => inspectArchive({ ...base, malwareScan: 'infected' }), /malware/)
  assert.throws(() => inspectArchive({ ...base, malwareScan: undefined }), /malware scan/)
  assert.throws(() => inspectArchive({ ...base, compressedBytes: 1, entries: [{ ...base.entries[0], uncompressedBytes: 1_000_000 }] }), /expansion ratio/)
})

test('schema registry and import store provide versioned idempotent incremental ingestion', () => {
  const schemas = registerArchiveSchema([], { platform: 'spotify', schemaVersion: 'spotify-streaming-history@1', paths: ['Streaming_History_Audio_*.json'], recordIdFields: ['ts', 'master_metadata_track_name'] })
  assert.throws(() => registerArchiveSchema(schemas, schemas[0]), /already registered/)
  const plan = createArchiveImportPlan({ context, sourceId: 'spotify:acct-1', platform: 'spotify', schemaVersion: 'spotify-streaming-history@1', archiveDigest: 'b'.repeat(64), consentReceiptId: 'consent:1', records: [{ sourceRecordId: 'r1', occurredAt: '2026-01-01T00:00:00Z', category: 'listen', content: 'Track One' }] }, schemas)
  const store = new ArchiveImportStore()
  assert.deepEqual(store.ingest(plan), { inserted: 1, skipped: 0 })
  assert.deepEqual(store.ingest(plan), { inserted: 0, skipped: 1 })
  assert.equal(store.eventsForSource(context, 'spotify:acct-1').length, 1)
  assert.equal(store.deleteSource(context, 'spotify:acct-1'), 1)
  assert.equal(store.eventsForSource(context, 'spotify:acct-1').length, 0)
})

test('revocation stops connector and per-source deletion removes imported descendants', () => {
  const runtime = createConnectorRuntime(context, 'spotify:acct-1', 'spotify')
  const revoked = revokeConnector(runtime, context, '2026-08-24T04:00:00Z', 'user disconnect')
  assert.equal(revoked.status, 'revoked')
  assert.equal(revoked.ingestionEnabled, false)
  const deletion = deleteSourceData({ context, sourceId: 'spotify:acct-1', descendantRefs: ['event:1', 'feature:1'], keyIds: ['dek:1'] })
  assert.equal(deletion.steps[0].action, 'stop-ingestion-and-revoke-token')
  assert.equal(deletion.auditTombstone.containsPersonalData, false)
})
