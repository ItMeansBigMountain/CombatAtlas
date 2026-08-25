import { createHash, randomUUID } from 'node:crypto'

import {
  CONNECTOR_REGISTRY, beginOAuthAuthorization, createAuditEvent, encryptProviderToken, inspectArchive,
  type ArchiveEnvelope, type AuditEvent, type ConnectorPlatform, type EncryptedTokenRecord, type PendingOAuthAuthorization,
  type TenantContext,
} from '@tweet-between-the-lines/domain'

export * from './durable.js'
export * from './postgres.js'
export * from './auth.js'

export type AuthContext = { tenantId: string; subjectId: string; actorId: string }
export type ApiRequest = { method: 'GET' | 'POST' | 'PUT' | 'DELETE'; path: string; auth: AuthContext | null; body?: unknown }
export type ApiResponse = { status: number; body: unknown }
export type OAuthExchangeInput = { provider: ConnectorPlatform; code: string; codeVerifier: string; redirectUri: string }
export type OAuthExchangeResult = { accessToken: string; refreshToken?: string; grantedScopes: string[]; providerSubject: string }
export type OAuthCodeExchanger = (input: OAuthExchangeInput) => Promise<OAuthExchangeResult>
export interface KeyProvider { dataKey(context: AuthContext): Promise<{ key: Buffer; keyId: string }> }

export class FixedKeyProvider implements KeyProvider {
  constructor(private readonly key: Buffer, private readonly keyId: string) {
    if (key.length !== 32) throw new Error('A 256-bit key is required')
  }
  async dataKey(): Promise<{ key: Buffer; keyId: string }> { return { key: Buffer.from(this.key), keyId: this.keyId } }
}

type StoredEvent = { id: string; tenantId: string; subjectId: string; sourceId: string; content: string }
type Correction = { eventId: string; tenantId: string; subjectId: string; value: string; correctedAt: string }
type ImportJob = { id: string; tenantId: string; subjectId: string; sourceId: string; platform: string; status: 'queued'; archiveDigest: string; createdAt: string }
type PendingState = PendingOAuthAuthorization

export class MemoryBackendStore {
  readonly oauthStates = new Map<string, PendingState>()
  readonly consumedOAuthStates = new Set<string>()
  readonly tokenRecords = new Map<string, EncryptedTokenRecord>()
  readonly importJobs = new Map<string, ImportJob>()
  readonly events = new Map<string, StoredEvent>()
  readonly corrections = new Map<string, Correction>()
  readonly auditEvents: AuditEvent[] = []
  readonly deletedSubjects = new Set<string>()

  seedEvent(event: StoredEvent): void { this.events.set(event.id, structuredClone(event)) }
  saveOAuth(pending: PendingState): void { this.oauthStates.set(this.stateKey(pending.context, pending.provider, pending.state), structuredClone(pending)) }
  consumeOAuth(auth: AuthContext, provider: ConnectorPlatform, state: string): PendingState | undefined {
    const key = this.stateKey(auth, provider, state)
    const pending = this.oauthStates.get(key)
    if (!pending) return undefined
    this.oauthStates.delete(key)
    this.consumedOAuthStates.add(key)
    return pending
  }
  wasOAuthConsumed(auth: AuthContext, provider: ConnectorPlatform, state: string): boolean { return this.consumedOAuthStates.has(this.stateKey(auth, provider, state)) }
  subjectKey(auth: Pick<AuthContext, 'tenantId' | 'subjectId'>): string { return `${auth.tenantId}\u0000${auth.subjectId}` }
  private stateKey(auth: Pick<AuthContext, 'tenantId' | 'subjectId'>, provider: string, state: string): string { return `${this.subjectKey(auth)}\u0000${provider}\u0000${state}` }
}

type ApiOptions = { store: MemoryBackendStore; keyProvider: KeyProvider; exchange: OAuthCodeExchanger; now?: () => string; allowedRedirectUris: string[] }

export class ApiService {
  private readonly now: () => string
  constructor(private readonly options: ApiOptions) { this.now = options.now ?? (() => new Date().toISOString()) }

  async handle(request: ApiRequest): Promise<ApiResponse> {
    if (request.method === 'GET' && request.path === '/healthz') return { status: 200, body: { status: 'ok' } }
    if (request.method === 'GET' && request.path === '/readyz') return { status: 200, body: { status: 'ready' } }
    if (!request.auth) return { status: 401, body: { error: 'authentication_required' } }
    if (this.options.store.deletedSubjects.has(this.options.store.subjectKey(request.auth))) return { status: 404, body: { error: 'not_found' } }

    try {
      const oauth = request.path.match(/^\/v1\/oauth\/([a-z0-9_]+)\/(authorize|callback)$/)
      if (oauth) return oauth[2] === 'authorize'
        ? this.authorize(request.auth, oauth[1] as ConnectorPlatform, request.body)
        : await this.callback(request.auth, oauth[1] as ConnectorPlatform, request.body)
      if (request.method === 'POST' && request.path === '/v1/imports/archive') return this.admitArchive(request.auth, request.body)
      const correction = request.path.match(/^\/v1\/corrections\/([^/]+)$/)
      if (request.method === 'PUT' && correction) return this.correct(request.auth, decodeURIComponent(correction[1]!), request.body)
      if (request.method === 'POST' && request.path === '/v1/privacy/export') return this.export(request.auth, request.body)
      if (request.method === 'DELETE' && request.path === '/v1/privacy/account') return this.deleteAccount(request.auth, request.body)
      return { status: 404, body: { error: 'not_found' } }
    } catch (error) {
      this.audit(request.auth, 'request-denied', 'request', 'deny', 'failed')
      return { status: 422, body: { error: 'request_rejected', message: error instanceof Error ? error.message : 'Rejected' } }
    }
  }

  private authorize(auth: AuthContext, provider: ConnectorPlatform, body: unknown): ApiResponse {
    const input = object(body); const redirectUri = text(input.redirectUri, 'redirectUri'); const scopes = strings(input.scopes, 'scopes')
    if (!(provider in CONNECTOR_REGISTRY)) throw new Error('Unknown provider')
    const pending = beginOAuthAuthorization({ context: tenant(auth, 'source-connection'), provider, redirectUri, allowedRedirectUris: this.options.allowedRedirectUris, requestedScopes: scopes, now: this.now() })
    this.options.store.saveOAuth(pending)
    this.audit(auth, 'oauth-started', provider, 'allow', 'succeeded')
    return { status: 201, body: { authorizationUrl: pending.authorizationUrl, state: pending.state, expiresAt: pending.expiresAt } }
  }

  private async callback(auth: AuthContext, provider: ConnectorPlatform, body: unknown): Promise<ApiResponse> {
    const input = object(body); const state = text(input.state, 'state')
    const pending = this.options.store.consumeOAuth(auth, provider, state)
    if (!pending) return this.options.store.wasOAuthConsumed(auth, provider, state)
      ? { status: 409, body: { error: 'oauth_state_consumed' } }
      : { status: 404, body: { error: 'oauth_state_not_found' } }
    const redirectUri = text(input.redirectUri, 'redirectUri'); const code = text(input.code, 'code')
    if (redirectUri !== pending.redirectUri || new Date(this.now()).valueOf() > new Date(pending.expiresAt).valueOf()) throw new Error('OAuth callback binding or expiry check failed')
    const exchanged = await this.options.exchange({ provider, code, codeVerifier: pending.codeVerifier, redirectUri })
    if (exchanged.grantedScopes.some((scope) => !pending.requestedScopes.includes(scope))) throw new Error('Provider granted an unexpected scope')
    const { key, keyId } = await this.options.keyProvider.dataKey(auth)
    const record = encryptProviderToken({ context: tenant(auth, 'connector-storage'), provider, scopes: exchanged.grantedScopes, token: JSON.stringify({ accessToken: exchanged.accessToken, refreshToken: exchanged.refreshToken ?? null, providerSubject: exchanged.providerSubject }), dataKey: key, keyId, createdAt: this.now() })
    this.options.store.tokenRecords.set(record.vaultRef, record)
    this.audit(auth, 'oauth-completed', provider, 'allow', 'succeeded')
    return { status: 200, body: { connected: true, provider, scopes: [...exchanged.grantedScopes].sort() } }
  }

  private admitArchive(auth: AuthContext, body: unknown): ApiResponse {
    const input = object(body); const sourceId = text(input.sourceId, 'sourceId'); const platform = text(input.platform, 'platform'); text(input.consentReceiptId, 'consentReceiptId')
    const archive = input.archive as ArchiveEnvelope
    const inspection = inspectArchive(archive)
    const digest = createHash('sha256').update(JSON.stringify(archive)).digest('hex')
    const id = `import:${createHash('sha256').update(`${auth.tenantId}:${auth.subjectId}:${digest}`).digest('hex')}`
    const job: ImportJob = { id, tenantId: auth.tenantId, subjectId: auth.subjectId, sourceId, platform, status: 'queued', archiveDigest: digest, createdAt: this.now() }
    this.options.store.importJobs.set(id, job)
    this.audit(auth, 'archive-admitted', id, 'allow', 'succeeded')
    return { status: 202, body: { jobId: id, status: job.status, acceptedEntries: inspection.entryCount } }
  }

  private correct(auth: AuthContext, eventId: string, body: unknown): ApiResponse {
    const event = this.options.store.events.get(eventId)
    if (!event || event.tenantId !== auth.tenantId || event.subjectId !== auth.subjectId) return { status: 404, body: { error: 'not_found' } }
    const value = text(object(body).value, 'value')
    this.options.store.corrections.set(`${auth.tenantId}:${auth.subjectId}:${eventId}`, { eventId, tenantId: auth.tenantId, subjectId: auth.subjectId, value, correctedAt: this.now() })
    this.audit(auth, 'correction-recorded', eventId, 'allow', 'succeeded')
    return { status: 200, body: { eventId, corrected: true } }
  }

  private export(auth: AuthContext, body: unknown): ApiResponse {
    if (object(body).stepUpAuthenticated !== true) return { status: 403, body: { error: 'step_up_required' } }
    const events = [...this.options.store.events.values()].filter((item) => item.tenantId === auth.tenantId && item.subjectId === auth.subjectId)
    const corrections = [...this.options.store.corrections.values()].filter((item) => item.tenantId === auth.tenantId && item.subjectId === auth.subjectId)
    const payload = { schemaVersion: '1', generatedAt: this.now(), events: structuredClone(events), corrections: structuredClone(corrections) }
    this.audit(auth, 'export-created', 'account', 'allow', 'succeeded')
    return { status: 200, body: { ...payload, sha256: createHash('sha256').update(JSON.stringify(payload)).digest('hex') } }
  }

  private deleteAccount(auth: AuthContext, body: unknown): ApiResponse {
    const input = object(body); if (input.stepUpAuthenticated !== true) return { status: 403, body: { error: 'step_up_required' } }
    const key = text(input.idempotencyKey, 'idempotencyKey')
    for (const [id, item] of this.options.store.events) if (item.tenantId === auth.tenantId && item.subjectId === auth.subjectId) this.options.store.events.delete(id)
    for (const [id, item] of this.options.store.corrections) if (item.tenantId === auth.tenantId && item.subjectId === auth.subjectId) this.options.store.corrections.delete(id)
    for (const [id, item] of this.options.store.tokenRecords) if (item.tenantId === auth.tenantId && item.subjectId === auth.subjectId) this.options.store.tokenRecords.delete(id)
    this.options.store.deletedSubjects.add(this.options.store.subjectKey(auth))
    const jobId = `deletion:${createHash('sha256').update(`${auth.tenantId}:${key}`).digest('hex')}`
    this.audit(auth, 'account-deleted', jobId, 'allow', 'succeeded')
    return { status: 202, body: { jobId, status: 'queued', dataAccessRevoked: true } }
  }

  private audit(auth: AuthContext, action: string, targetRef: string, decision: 'allow' | 'deny', outcome: 'succeeded' | 'failed'): void {
    this.options.store.auditEvents.push(createAuditEvent({ tenantId: auth.tenantId, actorClass: 'user', action, targetRef, decision, outcome, occurredAt: this.now() }))
  }
}

function tenant(auth: AuthContext, purpose: string): TenantContext { return { ...auth, purpose } }
function object(value: unknown): Record<string, unknown> { if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('JSON object body required'); return value as Record<string, unknown> }
function text(value: unknown, field: string): string { if (typeof value !== 'string' || !value.trim()) throw new Error(`${field} is required`); return value.trim() }
function strings(value: unknown, field: string): string[] { if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) throw new Error(`${field} must be a string array`); return value.map((item) => item.trim()).filter(Boolean) }
