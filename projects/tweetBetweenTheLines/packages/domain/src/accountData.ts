import { createCipheriv, createDecipheriv, createHash, randomBytes, randomUUID } from 'node:crypto'

export type TenantContext = { tenantId: string; subjectId: string; actorId: string; purpose: string }

function required(value: string, field: string): string {
  const normalized = value.trim()
  if (!normalized) throw new Error(`${field} is required`)
  return normalized
}

function iso(value: string): string {
  const parsed = new Date(value)
  if (Number.isNaN(parsed.valueOf())) throw new Error('Invalid timestamp')
  return parsed.toISOString()
}

function unique(values: string[]): string[] {
  return [...new Set(values.map((value) => value.trim()).filter(Boolean))].sort()
}

export function requireTenantContext(context: TenantContext, expectedTenantId?: string): TenantContext {
  const verified = {
    tenantId: required(context.tenantId, 'tenantId'),
    subjectId: required(context.subjectId, 'subjectId'),
    actorId: required(context.actorId, 'actorId'),
    purpose: required(context.purpose, 'purpose'),
  }
  if (expectedTenantId && verified.tenantId !== expectedTenantId) throw new Error('Tenant context mismatch')
  return verified
}

export type AccountIdentity = {
  id: string
  tenantId: string
  subjectId: string
  email: string | null
  passkeyCredentialIds: string[]
  socialBindings: Array<{ provider: string; providerSubject: string }>
  createdAt: string
}

export function createAccountIdentity(input: Omit<AccountIdentity, 'id' | 'passkeyCredentialIds' | 'socialBindings'>): AccountIdentity {
  const tenantId = required(input.tenantId, 'tenantId')
  const subjectId = required(input.subjectId, 'subjectId')
  return {
    id: `account:${encodeURIComponent(tenantId)}:${encodeURIComponent(subjectId)}`,
    tenantId,
    subjectId,
    email: input.email?.trim().toLowerCase() || null,
    passkeyCredentialIds: [],
    socialBindings: [],
    createdAt: iso(input.createdAt),
  }
}

export function bindPasskey(account: AccountIdentity, context: TenantContext, credentialId: string): AccountIdentity {
  requireTenantContext(context, account.tenantId)
  if (context.subjectId !== account.subjectId) throw new Error('Subject context mismatch')
  return { ...account, passkeyCredentialIds: unique([...account.passkeyCredentialIds, required(credentialId, 'credentialId')]) }
}

export function bindSocialIdentity(account: AccountIdentity, context: TenantContext, provider: string, providerSubject: string): AccountIdentity {
  requireTenantContext(context, account.tenantId)
  if (context.subjectId !== account.subjectId) throw new Error('Subject context mismatch')
  const binding = { provider: required(provider, 'provider'), providerSubject: required(providerSubject, 'providerSubject') }
  if (account.socialBindings.some((item) => item.provider === binding.provider && item.providerSubject !== binding.providerSubject)) {
    throw new Error('Provider is already bound to another identity')
  }
  return { ...account, socialBindings: [...account.socialBindings.filter((item) => item.provider !== binding.provider), binding] }
}

export type ScopeGrant = {
  provider: string
  requested: string[]
  granted: string[]
  rejected: string[]
}

export function createLeastPrivilegeScopeGrant(provider: string, requested: string[], granted: string[], allowed: string[]): ScopeGrant {
  const allowedSet = new Set(unique(allowed))
  const normalizedRequested = unique(requested)
  const normalizedGranted = unique(granted)
  const rejected = normalizedGranted.filter((scope) => !allowedSet.has(scope) || !normalizedRequested.includes(scope))
  if (rejected.length) throw new Error(`Unexpected provider scopes: ${rejected.join(', ')}`)
  return { provider: required(provider, 'provider'), requested: normalizedRequested, granted: normalizedGranted, rejected: [] }
}

export type DetailedConsentReceipt = {
  id: string
  tenantId: string
  subjectId: string
  sourceId: string
  purposes: string[]
  dataCategories: string[]
  oauthScopes: string[]
  policyVersion: string
  uiCopyVersion: string
  locale: string
  acquisitionPath: 'oauth' | 'archive'
  retention: string
  grantedAt: string
  status: 'active' | 'revoked'
  supersedesReceiptId: string | null
  revokedAt: string | null
  revocationReason: string | null
}

export function issueConsentReceipt(input: Omit<DetailedConsentReceipt, 'id' | 'status' | 'revokedAt' | 'revocationReason'>): DetailedConsentReceipt {
  const receipt = {
    ...input,
    tenantId: required(input.tenantId, 'tenantId'), subjectId: required(input.subjectId, 'subjectId'), sourceId: required(input.sourceId, 'sourceId'),
    purposes: unique(input.purposes), dataCategories: unique(input.dataCategories), oauthScopes: unique(input.oauthScopes),
    policyVersion: required(input.policyVersion, 'policyVersion'), uiCopyVersion: required(input.uiCopyVersion, 'uiCopyVersion'),
    locale: required(input.locale, 'locale'), retention: required(input.retention, 'retention'), grantedAt: iso(input.grantedAt),
  }
  if (!receipt.purposes.length || !receipt.dataCategories.length) throw new Error('Consent requires purpose and data category')
  const digest = createHash('sha256').update(JSON.stringify(receipt)).digest('hex')
  return { ...receipt, id: `consent:${digest}`, status: 'active', revokedAt: null, revocationReason: null }
}

export function revokeConsent(receipt: DetailedConsentReceipt, revokedAt: string, reason: string): DetailedConsentReceipt {
  if (receipt.status === 'revoked') return receipt
  return { ...receipt, status: 'revoked', revokedAt: iso(revokedAt), revocationReason: required(reason, 'reason') }
}

export function assertConsent(receipt: DetailedConsentReceipt | undefined, context: TenantContext, sourceId: string, category: string, purpose: string, at: string): void {
  requireTenantContext(context, receipt?.tenantId)
  if (!receipt || receipt.status !== 'active' || receipt.subjectId !== context.subjectId || receipt.sourceId !== sourceId ||
      !receipt.dataCategories.includes(category) || !receipt.purposes.includes(purpose) || iso(at) < receipt.grantedAt) {
    throw new Error('Active, specific consent is required')
  }
}

export type EncryptedTokenRecord = {
  vaultRef: string
  tenantId: string
  subjectId: string
  provider: string
  scopes: string[]
  keyId: string
  iv: string
  authTag: string
  ciphertext: string
  createdAt: string
  revokedAt: string | null
}

function vaultAad(record: Pick<EncryptedTokenRecord, 'tenantId' | 'subjectId' | 'provider' | 'scopes' | 'keyId'>): Buffer {
  const { tenantId, subjectId, provider, scopes, keyId } = record
  return Buffer.from(JSON.stringify({ tenantId, subjectId, provider, scopes, keyId }))
}

export function encryptProviderToken(input: { context: TenantContext; provider: string; scopes: string[]; token: string; dataKey: Buffer; keyId: string; createdAt: string }): EncryptedTokenRecord {
  const context = requireTenantContext(input.context)
  if (input.dataKey.length !== 32) throw new Error('A 256-bit data key is required')
  const base = { tenantId: context.tenantId, subjectId: context.subjectId, provider: required(input.provider, 'provider'), scopes: unique(input.scopes), keyId: required(input.keyId, 'keyId') }
  const iv = randomBytes(12)
  const cipher = createCipheriv('aes-256-gcm', input.dataKey, iv)
  cipher.setAAD(vaultAad(base))
  const ciphertext = Buffer.concat([cipher.update(required(input.token, 'token'), 'utf8'), cipher.final()])
  return { ...base, vaultRef: `vault://${base.tenantId}/${base.subjectId}/${base.provider}`, iv: iv.toString('base64'), authTag: cipher.getAuthTag().toString('base64'), ciphertext: ciphertext.toString('base64'), createdAt: iso(input.createdAt), revokedAt: null }
}

export function decryptProviderToken(record: EncryptedTokenRecord, context: TenantContext, dataKey: Buffer, role: 'connector' | 'analytics'): string {
  requireTenantContext(context, record.tenantId)
  if (context.subjectId !== record.subjectId || role !== 'connector' || record.revokedAt) throw new Error('Token access denied')
  const decipher = createDecipheriv('aes-256-gcm', dataKey, Buffer.from(record.iv, 'base64'))
  decipher.setAAD(vaultAad(record)); decipher.setAuthTag(Buffer.from(record.authTag, 'base64'))
  return Buffer.concat([decipher.update(Buffer.from(record.ciphertext, 'base64')), decipher.final()]).toString('utf8')
}

export type ProvenanceRichEvent = {
  id: string; tenantId: string; subjectId: string; sourceId: string; sourceRecordId: string; consentReceiptId: string
  category: string; kind: string; occurredAt: string; ingestedAt: string; locale: string | null; content: string
  lineage: { sourceKey: string; rawObjectRef: string | null; analyzerVersion: string | null }
}

export function normalizeProvenanceEvent(input: Omit<ProvenanceRichEvent, 'id'>, context: TenantContext): ProvenanceRichEvent {
  requireTenantContext(context, input.tenantId)
  if (context.subjectId !== input.subjectId) throw new Error('Subject context mismatch')
  const sourceId = required(input.sourceId, 'sourceId'); const sourceRecordId = required(input.sourceRecordId, 'sourceRecordId')
  return { ...input, id: `event:${input.tenantId}:${input.subjectId}:${sourceId}:${sourceRecordId}`, sourceId, sourceRecordId, occurredAt: iso(input.occurredAt), ingestedAt: iso(input.ingestedAt), content: input.content.trim() }
}

export type AuditEvent = { id: string; tenantId: string; actorClass: 'user' | 'connector' | 'worker' | 'support'; action: string; targetRef: string; decision: 'allow' | 'deny'; outcome: 'succeeded' | 'failed'; occurredAt: string }
export function createAuditEvent(input: Omit<AuditEvent, 'id'>): AuditEvent {
  const serialized = JSON.stringify(input)
  if (/token|ciphertext|content|prompt/i.test(serialized)) throw new Error('Audit records may not contain secret or content fields')
  return { ...input, id: `audit:${randomUUID()}`, tenantId: required(input.tenantId, 'tenantId'), occurredAt: iso(input.occurredAt) }
}

export function buildUserExport(input: { context: TenantContext; stepUpAuthenticated: boolean; receipts: DetailedConsentReceipt[]; events: ProvenanceRichEvent[]; features: unknown[]; insights: unknown[]; generatedAt: string }) {
  const context = requireTenantContext(input.context)
  if (!input.stepUpAuthenticated) throw new Error('Step-up authentication is required')
  const receipts = input.receipts.filter((item) => item.tenantId === context.tenantId && item.subjectId === context.subjectId)
  const events = input.events.filter((item) => item.tenantId === context.tenantId && item.subjectId === context.subjectId)
  const assertOwned = (items: unknown[], collection: string) => {
    for (const item of items) {
      if (!item || typeof item !== 'object') throw new Error(`${collection} export entries require tenant and subject ownership`)
      const owned = item as { tenantId?: unknown; subjectId?: unknown }
      if (owned.tenantId !== context.tenantId || owned.subjectId !== context.subjectId) throw new Error(`${collection} export ownership mismatch`)
    }
  }
  assertOwned(input.features, 'Feature')
  assertOwned(input.insights, 'Insight')
  const payload = { receipts, events, features: structuredClone(input.features), insights: structuredClone(input.insights) }
  if (/ciphertext|authTag|vault:\/\//i.test(JSON.stringify(payload))) throw new Error('Export contains secret material')
  return { generatedAt: iso(input.generatedAt), subjectId: context.subjectId, payload, manifest: { schemaVersion: '1', sha256: createHash('sha256').update(JSON.stringify(payload)).digest('hex') } }
}

export type PrivacyJob = { id: string; tenantId: string; subjectId: string; sourceId: string; kind: 'source-revocation' | 'account-deletion' | 'deletion-reconciliation'; status: 'queued' | 'running' | 'completed' | 'failed'; idempotencyKey: string; notAfter: string }
export function createPrivacyJob(input: Omit<PrivacyJob, 'id' | 'status'>): PrivacyJob {
  required(input.idempotencyKey, 'idempotencyKey')
  return { ...input, id: `job:${createHash('sha256').update(`${input.tenantId}:${input.idempotencyKey}`).digest('hex')}`, status: 'queued', notAfter: iso(input.notAfter) }
}

export function buildCryptographicDeletion(input: { tenantId: string; subjectId: string; sourceId: string; descendantRefs: string[]; keyIds: string[] }) {
  const lineage = `${required(input.tenantId, 'tenantId')}:${required(input.subjectId, 'subjectId')}:${required(input.sourceId, 'sourceId')}`
  return {
    lineage,
    steps: [
      { action: 'stop-ingestion-and-revoke-token', refs: [`vault://${input.tenantId}/${input.subjectId}/${input.sourceId}`] },
      { action: 'hide-and-delete-descendants', refs: unique(input.descendantRefs) },
      { action: 'destroy-data-encryption-keys', refs: unique(input.keyIds) },
      { action: 'purge-caches-exports-queues', refs: [lineage] },
      { action: 'reconcile-and-tombstone', refs: [createHash('sha256').update(lineage).digest('hex')] },
    ],
    auditTombstone: { lineageDigest: createHash('sha256').update(lineage).digest('hex'), containsPersonalData: false as const },
  }
}

export function createAnalyticsPromptPayload(input: { tenantId: string; subjectId: string; aggregateEvidence: Record<string, unknown> }) {
  const payload = structuredClone({
    tenantId: required(input.tenantId, 'tenantId'),
    subjectId: required(input.subjectId, 'subjectId'),
    aggregateEvidence: input.aggregateEvidence,
  })
  const serialized = JSON.stringify(payload)
  if (/vault:\/\/|ciphertext|authTag|access[_-]?token|refresh[_-]?token/i.test(serialized)) throw new Error('Secret-like data is prohibited in analytics prompts')
  if (/(?:ignore|disregard|override)\s+(?:all\s+)?(?:(?:previous|prior)\s+)?(?:system\s+|developer\s+)?instructions|<\/?(?:system|assistant|developer|tool)>|(?:tool|function)[_-]?call|call\s+(?:a\s+)?tool/i.test(serialized)) {
    throw new Error('Instruction-like content is prohibited in aggregate analytics evidence')
  }
  return { ...payload, trustBoundary: 'untrusted-aggregate-data' as const }
}
