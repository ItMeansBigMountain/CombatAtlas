import test from 'node:test'
import assert from 'node:assert/strict'

import { ApiService, FixedKeyProvider, MemoryBackendStore, type ApiRequest, type OAuthCodeExchanger } from '../src/index.js'

const auth = { tenantId: 'tenant-a', subjectId: 'user-1', actorId: 'user-1' }
const fixedNow = () => '2026-08-24T05:00:00.000Z'
const exchange: OAuthCodeExchanger = async ({ code, codeVerifier }) => ({
  accessToken: `access-${code}-${codeVerifier.slice(0, 4)}`,
  refreshToken: `refresh-${code}`,
  grantedScopes: ['identity'],
  providerSubject: 'provider-user-1',
})

function request(method: ApiRequest['method'], path: string, body?: unknown, caller = auth): ApiRequest {
  return { method, path, auth: caller, body }
}

function createApi() {
  const store = new MemoryBackendStore()
  const api = new ApiService({ store, keyProvider: new FixedKeyProvider(Buffer.alloc(32, 7), 'test-key-v1'), exchange, now: fixedNow, allowedRedirectUris: ['app://oauth/callback'] })
  return { api, store }
}

test('OAuth initiation uses PKCE and callback atomically consumes state without returning tokens', async () => {
  const { api, store } = createApi()
  const initiated = await api.handle(request('POST', '/v1/oauth/reddit/authorize', { redirectUri: 'app://oauth/callback', scopes: ['identity'] }))
  assert.equal(initiated.status, 201)
  const contract = initiated.body as { authorizationUrl: string; state: string; expiresAt: string }
  const url = new URL(contract.authorizationUrl)
  assert.equal(url.searchParams.get('code_challenge_method'), 'S256')
  assert.equal(url.searchParams.has('code_challenge'), true)
  assert.equal(JSON.stringify(initiated).includes('codeVerifier'), false)

  const callback = await api.handle(request('POST', '/v1/oauth/reddit/callback', { redirectUri: 'app://oauth/callback', state: contract.state, code: 'consented-code' }))
  assert.equal(callback.status, 200)
  assert.deepEqual(callback.body, { connected: true, provider: 'reddit', scopes: ['identity'] })
  assert.equal(/access-|refresh-|consented-code/.test(JSON.stringify(callback)), false)
  assert.equal(store.tokenRecords.size, 1)

  const replay = await api.handle(request('POST', '/v1/oauth/reddit/callback', { redirectUri: 'app://oauth/callback', state: contract.state, code: 'replay' }))
  assert.equal(replay.status, 409)
})

test('OAuth state is tenant bound and unsupported/manual-only providers fail closed', async () => {
  const { api } = createApi()
  const initiated = await api.handle(request('POST', '/v1/oauth/reddit/authorize', { redirectUri: 'app://oauth/callback', scopes: ['identity'] }))
  const state = (initiated.body as { state: string }).state
  const crossTenant = await api.handle(request('POST', '/v1/oauth/reddit/callback', { redirectUri: 'app://oauth/callback', state, code: 'stolen' }, { ...auth, tenantId: 'tenant-b' }))
  assert.equal(crossTenant.status, 404)
  assert.equal((await api.handle(request('POST', '/v1/oauth/instagram/authorize', { redirectUri: 'app://oauth/callback', scopes: [] }))).status, 422)
})

test('archive admission authenticates, validates a synthetic manifest, and returns an async job contract', async () => {
  const { api } = createApi()
  const accepted = await api.handle(request('POST', '/v1/imports/archive', {
    sourceId: 'reddit', platform: 'reddit', consentReceiptId: 'consent:fixture',
    archive: { format: 'zip', compressedBytes: 100, malwareScan: 'clean', entries: [{ path: 'data.json', compressedBytes: 100, uncompressedBytes: 200, kind: 'file', mime: 'application/json', magic: 'json', sha256: 'a'.repeat(64) }] },
  }))
  assert.equal(accepted.status, 202)
  assert.match((accepted.body as { jobId: string }).jobId, /^import:/)
  assert.equal((accepted.body as { status: string }).status, 'queued')
  assert.equal((await api.handle(request('POST', '/v1/imports/archive', { sourceId: 'reddit', platform: 'reddit', consentReceiptId: 'consent:fixture', archive: { format: 'zip', compressedBytes: 1, malwareScan: 'clean', entries: [{ path: '../escape.json', compressedBytes: 1, uncompressedBytes: 1, kind: 'file', mime: 'application/json', magic: 'json', sha256: 'a'.repeat(64) }] } }))).status, 422)
})

test('correction, export, and delete endpoints enforce tenant isolation and deletion removes data', async () => {
  const { api, store } = createApi()
  store.seedEvent({ id: 'event-1', tenantId: 'tenant-a', subjectId: 'user-1', sourceId: 'reddit', content: 'consented fixture' })
  store.seedEvent({ id: 'event-2', tenantId: 'tenant-b', subjectId: 'user-2', sourceId: 'reddit', content: 'other tenant' })

  assert.equal((await api.handle(request('PUT', '/v1/corrections/event-2', { value: 'tamper' }))).status, 404)
  assert.equal((await api.handle(request('PUT', '/v1/corrections/event-1', { value: 'user correction' }))).status, 200)
  const exported = await api.handle(request('POST', '/v1/privacy/export', { stepUpAuthenticated: true }))
  assert.equal(exported.status, 200)
  assert.equal(JSON.stringify(exported.body).includes('other tenant'), false)

  const deleted = await api.handle(request('DELETE', '/v1/privacy/account', { stepUpAuthenticated: true, idempotencyKey: 'delete-fixture' }))
  assert.equal(deleted.status, 202)
  assert.equal(store.events.has('event-1'), false)
  assert.equal(store.events.has('event-2'), true)
  assert.equal((await api.handle(request('POST', '/v1/privacy/export', { stepUpAuthenticated: true }))).status, 404)
})

test('health/readiness and structured audits never expose content or secrets', async () => {
  const { api, store } = createApi()
  assert.deepEqual((await api.handle({ method: 'GET', path: '/healthz', auth: null })).body, { status: 'ok' })
  assert.deepEqual((await api.handle({ method: 'GET', path: '/readyz', auth: null })).body, { status: 'ready' })
  await api.handle(request('POST', '/v1/imports/archive', { sourceId: 'reddit', platform: 'reddit', consentReceiptId: 'consent:fixture', archive: { format: 'zip', compressedBytes: 1, malwareScan: 'infected', entries: [] }, accessToken: 'must-not-log', content: 'must-not-log' }))
  const auditJson = JSON.stringify(store.auditEvents)
  assert.equal(/must-not-log|accessToken|content|ciphertext|codeVerifier/i.test(auditJson), false)
  assert.equal(store.auditEvents.length > 0, true)
})
