import assert from 'node:assert/strict'
import test from 'node:test'

import { FirstPartyAuthStore, linkedProviderStatus, loginProviderStatus, pkceChallenge, type ProviderTokenRevoker } from '../src/auth.js'

const fixedNow = () => '2026-08-25T03:00:00.000Z'

test('login OAuth transactions use PKCE and are purpose, redirect, and subject bound', () => {
  const store = new FirstPartyAuthStore(fixedNow)
  const pending = store.begin({ purpose: 'login', provider: 'google', redirectUri: 'app://auth', requestedScopes: ['openid', 'email'], subjectId: null })
  assert.match(pending.state, /^[A-Za-z0-9_-]+$/)
  assert.notEqual(pkceChallenge(pending.verifier), pending.verifier)
  assert.throws(() => store.consume(pending.state, 'link', 'google', 'app://auth', null), /binding mismatch/)
  assert.throws(() => store.consume(pending.state, 'login', 'google', 'app://auth', null), /already consumed/)
})

test('first login creates an account and subsequent provider login returns the same subject', () => {
  const store = new FirstPartyAuthStore(fixedNow)
  const first = store.login({ provider: 'apple', providerSubject: 'apple-user-1', email: 'private-relay@example.test' })
  const again = store.login({ provider: 'apple', providerSubject: 'apple-user-1', email: null })
  assert.equal(first.created, true)
  assert.equal(again.created, false)
  assert.equal(again.subjectId, first.subjectId)
  assert.notEqual(again.session, first.session)
  assert.equal(store.sessions.size, 2)
})

test('linked social accounts require separate consent and unlink revokes before deleting metadata', async () => {
  const store = new FirstPartyAuthStore(fixedNow)
  const receipt = store.link('user-1', { provider: 'reddit', providerSubject: 'reddit-1', scopes: ['identity'], vaultRef: 'vault-1', linkedAt: fixedNow() })
  const revoked: string[] = []
  const revoker: ProviderTokenRevoker = { async revoke(provider, vaultRef) { revoked.push(`${provider}:${vaultRef}`); return 'revoked' } }
  assert.equal(store.list('user-1').length, 1)
  assert.equal(await store.unlink('user-1', 'reddit', revoker), true)
  assert.deepEqual(revoked, ['reddit:vault-1'])
  assert.equal(store.list('user-1').length, 0)
  assert.equal(store.consents.get(receipt.id)?.revokedAt, fixedNow())
})

test('revocation failure preserves linked account and active consent', async () => {
  const store = new FirstPartyAuthStore(fixedNow)
  const receipt = store.link('user-1', { provider: 'reddit', providerSubject: 'reddit-1', scopes: ['identity'], vaultRef: 'vault-1', linkedAt: fixedNow() })
  await assert.rejects(() => store.unlink('user-1', 'reddit', { async revoke() { throw new Error('provider unavailable') } }), /unavailable/)
  assert.equal(store.list('user-1').length, 1)
  assert.equal(store.consents.get(receipt.id)?.revokedAt, null)
})

test('provider status never implies unconfigured or unapproved access', () => {
  assert.deepEqual(loginProviderStatus(new Set(['google'])), { google: 'available', apple: 'unconfigured' })
  const statuses = linkedProviderStatus(new Set(['reddit', 'google_youtube']), new Set(['reddit']))
  assert.equal(statuses.reddit, 'available')
  assert.equal(statuses.google_youtube, 'pending_review')
  assert.equal(statuses.instagram, 'archive_only')
  assert.equal(statuses.threads, 'unavailable')
})
