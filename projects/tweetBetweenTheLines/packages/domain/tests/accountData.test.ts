import test from 'node:test'
import assert from 'node:assert/strict'
import { randomBytes } from 'node:crypto'

import {
  assertConsent, bindPasskey, bindSocialIdentity, buildCryptographicDeletion, buildUserExport,
  createAccountIdentity, createAnalyticsPromptPayload, createAuditEvent, createLeastPrivilegeScopeGrant,
  createPrivacyJob, decryptProviderToken, encryptProviderToken, issueConsentReceipt,
  normalizeProvenanceEvent, revokeConsent, type TenantContext,
} from '../src/index.js'

const context: TenantContext = { tenantId: 'tenant-a', subjectId: 'user-1', actorId: 'user-1', purpose: 'profile-reflection' }

test('accounts support optional passkeys and stable social bindings with tenant isolation', () => {
  let account = createAccountIdentity({ tenantId: 'tenant-a', subjectId: 'user-1', email: ' USER@Example.com ', createdAt: '2026-08-24T00:00:00Z' })
  account = bindPasskey(account, context, 'credential-1')
  account = bindSocialIdentity(account, context, 'google', 'google-subject-1')
  assert.equal(account.email, 'user@example.com')
  assert.deepEqual(account.passkeyCredentialIds, ['credential-1'])
  assert.throws(() => bindPasskey(account, { ...context, tenantId: 'tenant-b' }, 'evil'), /Tenant context mismatch/)
})

test('scope and consent ledgers fail closed and revocation blocks processing', () => {
  const grant = createLeastPrivilegeScopeGrant('youtube', ['youtube.readonly'], ['youtube.readonly'], ['youtube.readonly'])
  assert.deepEqual(grant.granted, ['youtube.readonly'])
  assert.throws(() => createLeastPrivilegeScopeGrant('youtube', ['youtube.readonly'], ['youtube.force-ssl'], ['youtube.readonly']), /Unexpected/)
  const receipt = issueConsentReceipt({ tenantId: 'tenant-a', subjectId: 'user-1', sourceId: 'youtube', purposes: ['profile-reflection'], dataCategories: ['watch-history'], oauthScopes: grant.granted, policyVersion: '3', uiCopyVersion: '2', locale: 'en', acquisitionPath: 'oauth', retention: '30-days', grantedAt: '2026-08-24T00:00:00Z', supersedesReceiptId: null })
  assert.doesNotThrow(() => assertConsent(receipt, context, 'youtube', 'watch-history', 'profile-reflection', '2026-08-25T00:00:00Z'))
  assert.throws(() => assertConsent(receipt, context, 'youtube', 'messages', 'profile-reflection', '2026-08-25T00:00:00Z'), /consent/i)
  assert.throws(() => assertConsent(revokeConsent(receipt, '2026-08-25T01:00:00Z', 'user-request'), context, 'youtube', 'watch-history', 'profile-reflection', '2026-08-25T02:00:00Z'), /consent/i)
})

test('AES-GCM token vault permits connector-only tenant-bound access', () => {
  const key = randomBytes(32)
  const record = encryptProviderToken({ context, provider: 'youtube', scopes: ['youtube.readonly'], token: 'secret-token', dataKey: key, keyId: 'kms:key-1', createdAt: '2026-08-24T00:00:00Z' })
  assert.equal(record.ciphertext.includes('secret-token'), false)
  assert.equal(decryptProviderToken(record, context, key, 'connector'), 'secret-token')
  assert.throws(() => decryptProviderToken(record, context, key, 'analytics'), /denied/)
  assert.throws(() => decryptProviderToken(record, { ...context, tenantId: 'tenant-b' }, key, 'connector'), /mismatch/)
})

test('normalized events retain consent and deletion provenance', () => {
  const event = normalizeProvenanceEvent({ tenantId: 'tenant-a', subjectId: 'user-1', sourceId: 'x', sourceRecordId: 'post-1', consentReceiptId: 'consent:1', category: 'posts', kind: 'post', occurredAt: '2026-08-23T00:00:00Z', ingestedAt: '2026-08-24T00:00:00Z', locale: 'en', content: ' hello ', lineage: { sourceKey: 'x:user-1', rawObjectRef: 'raw:1', analyzerVersion: null } }, context)
  assert.equal(event.content, 'hello')
  assert.match(event.id, /^event:tenant-a:user-1:/)
  assert.equal(event.consentReceiptId, 'consent:1')
})

test('exports require step-up auth, isolate subjects, and exclude vault material', () => {
  assert.throws(() => buildUserExport({ context, stepUpAuthenticated: false, receipts: [], events: [], features: [], insights: [], generatedAt: '2026-08-24T00:00:00Z' }), /Step-up/)
  const result = buildUserExport({ context, stepUpAuthenticated: true, receipts: [], events: [], features: [{ tenantId: 'tenant-a', subjectId: 'user-1', count: 2 }], insights: [], generatedAt: '2026-08-24T00:00:00Z' })
  assert.match(result.manifest.sha256, /^[a-f0-9]{64}$/)
  assert.equal(JSON.stringify(result).includes('vault://'), false)
})

test('deletion, audit, and jobs retain only non-personal evidence', () => {
  const deletion = buildCryptographicDeletion({ tenantId: 'tenant-a', subjectId: 'user-1', sourceId: 'youtube', descendantRefs: ['insight:1', 'event:1'], keyIds: ['dek:1'] })
  assert.equal(deletion.steps.some((step) => step.action === 'destroy-data-encryption-keys'), true)
  assert.equal(deletion.auditTombstone.containsPersonalData, false)
  const audit = createAuditEvent({ tenantId: 'tenant-a', actorClass: 'user', action: 'source-revoked', targetRef: deletion.auditTombstone.lineageDigest, decision: 'allow', outcome: 'succeeded', occurredAt: '2026-08-24T00:00:00Z' })
  assert.match(audit.id, /^audit:/)
  assert.throws(() => createAuditEvent({ tenantId: 'tenant-a', actorClass: 'worker', action: 'token-read', targetRef: 'x', decision: 'deny', outcome: 'failed', occurredAt: '2026-08-24T00:00:00Z' }), /secret/)
  const job = createPrivacyJob({ tenantId: 'tenant-a', subjectId: 'user-1', sourceId: 'youtube', kind: 'source-revocation', idempotencyKey: 'revoke-youtube-v1', notAfter: '2026-08-25T00:00:00Z' })
  assert.equal(job.status, 'queued')
})

test('analytics prompt payload rejects tokens and token-vault fields', () => {
  assert.deepEqual(createAnalyticsPromptPayload({ tenantId: 'tenant-a', subjectId: 'user-1', aggregateEvidence: { music: 3 } }).aggregateEvidence, { music: 3 })
  assert.throws(() => createAnalyticsPromptPayload({ tenantId: 'tenant-a', subjectId: 'user-1', aggregateEvidence: { access_token: 'secret' } }), /prohibited/)
  assert.throws(() => createAnalyticsPromptPayload({ tenantId: 'tenant-a', subjectId: 'user-1', aggregateEvidence: { reference: 'vault://tenant/user/provider' } }), /prohibited/)
})