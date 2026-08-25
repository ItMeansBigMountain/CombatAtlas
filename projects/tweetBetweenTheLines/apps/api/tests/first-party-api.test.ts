import assert from 'node:assert/strict'
import test from 'node:test'

import { ApiService, FirstPartyAuthStore, FixedKeyProvider, MemoryBackendStore, type FirstPartyOAuthProvider } from '../src/index.js'

const redirectUri = 'https://app.example.test/auth/callback'
const provider: FirstPartyOAuthProvider = {
  authorizationEndpoint: 'https://accounts.example.test/authorize', clientId: 'test-client', scopes: ['openid', 'email'],
  async exchange(input) { return { providerSubject: `google:${input.code}`, email: 'person@example.test' } },
}

function service() {
  const firstPartyAuth = new FirstPartyAuthStore(() => '2026-08-25T03:00:00.000Z')
  return { api: new ApiService({ store: new MemoryBackendStore(), keyProvider: new FixedKeyProvider(Buffer.alloc(32, 7), 'test'), exchange: async () => { throw new Error('not used') }, revoker: { async revoke() { return 'revoked' } }, allowedRedirectUris: [redirectUri], configuredProviders: new Set(), approvedProviders: new Set(), firstPartyAuth, loginProviders: { google: provider }, now: () => '2026-08-25T03:00:00.000Z' }) }
}

test('first-party HTTP routes advertise providers and issue an opaque verified secure session', async () => {
  const { api } = service()
  assert.deepEqual((await api.handle({ method: 'GET', path: '/v1/auth/providers', auth: null })).body, { google: 'available', apple: 'unconfigured' })
  const started = await api.handle({ method: 'POST', path: '/v1/auth/google/authorize', auth: null, body: { redirectUri } })
  assert.equal(started.status, 201)
  const url = new URL((started.body as { authorizationUrl: string }).authorizationUrl)
  assert.equal(url.searchParams.get('code_challenge_method'), 'S256')
  const state = (started.body as { state: string }).state
  assert.equal((await api.handle({ method: 'POST', path: '/v1/auth/google/callback', auth: null, body: { state, code: 'ok', redirectUri: 'https://evil.example/callback' } })).status, 422)
  const callback = await api.handle({ method: 'POST', path: '/v1/auth/google/callback', auth: null, body: { state, code: 'ok', redirectUri } })
  assert.equal(callback.status, 200)
  const cookie = callback.headers?.['set-cookie'] ?? ''
  assert.match(cookie, /^tbl_session=[A-Za-z0-9_-]+; Path=\/; HttpOnly; Secure; SameSite=Lax;/)
  const token = cookie.match(/^tbl_session=([^;]+)/)?.[1]
  assert.equal((await api.handle({ method: 'GET', path: '/v1/auth/session', auth: null, sessionToken: token })).status, 200)
  assert.equal((await api.handle({ method: 'POST', path: '/v1/auth/google/callback', auth: null, body: { state, code: 'ok', redirectUri } })).status, 409)
})

test('re-login rotates the prior session and unconfigured providers fail honestly', async () => {
  const { api } = service()
  const login = async () => {
    const started = await api.handle({ method: 'POST', path: '/v1/auth/google/authorize', auth: null, body: { redirectUri } })
    return api.handle({ method: 'POST', path: '/v1/auth/google/callback', auth: null, body: { state: (started.body as { state: string }).state, code: 'same', redirectUri } })
  }
  const first = await login(); const second = await login()
  const firstToken = first.headers?.['set-cookie']?.match(/^tbl_session=([^;]+)/)?.[1]
  const secondToken = second.headers?.['set-cookie']?.match(/^tbl_session=([^;]+)/)?.[1]
  assert.notEqual(firstToken, secondToken)
  assert.equal((await api.handle({ method: 'GET', path: '/v1/auth/session', auth: null, sessionToken: firstToken })).status, 401)
  assert.equal((await api.handle({ method: 'GET', path: '/v1/auth/session', auth: null, sessionToken: secondToken })).status, 200)
  assert.equal((await api.handle({ method: 'POST', path: '/v1/auth/apple/authorize', auth: null, body: { redirectUri } })).status, 503)
})