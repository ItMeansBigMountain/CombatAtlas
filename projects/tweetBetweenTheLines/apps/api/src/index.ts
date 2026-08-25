import { createHash, randomUUID } from 'node:crypto'

import {
  CONNECTOR_REGISTRY, beginOAuthAuthorization, createAuditEvent, encryptProviderToken, inspectArchive,
  type ArchiveEnvelope, type AuditEvent, type ConnectorPlatform, type EncryptedTokenRecord, type PendingOAuthAuthorization,
  type TenantContext,
} from '@tweet-between-the-lines/domain'
import { FirstPartyAuthStore, linkedProviderStatus, loginProviderStatus, pkceChallenge, type FirstPartyOAuthProvider, type LoginProvider, type ProviderTokenRevoker, type ProviderAvailability } from './auth.js'

export * from './durable.js'
export * from './postgres.js'
export * from './auth.js'

export type AuthContext = { tenantId: string; subjectId: string; actorId: string }
export type ApiRequest = { method: 'GET' | 'POST' | 'PUT' | 'DELETE'; path: string; auth: AuthContext | null; body?: unknown; sessionToken?: string }
export type ApiResponse = { status: number; body: unknown; headers?: Record<string, string> }
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
export type LinkedAccountMetadata = { tenantId: string; subjectId: string; provider: ConnectorPlatform; providerSubject: string; scopes: string[]; vaultRef: string; consentReceiptId: string; linkedAt: string }
export type SourceConsentReceipt = { id: string; tenantId: string; subjectId: string; provider: ConnectorPlatform; providerSubject: string; purpose: 'source-connection'; scopes: string[]; grantedAt: string; revokedAt: string | null }

export class MemoryBackendStore {
  readonly oauthStates = new Map<string, PendingState>()
  readonly consumedOAuthStates = new Set<string>()
  readonly tokenRecords = new Map<string, EncryptedTokenRecord>()
  readonly linkedAccounts = new Map<string, LinkedAccountMetadata>()
  readonly consentReceipts = new Map<string, SourceConsentReceipt>()
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
  findOAuth(auth: AuthContext, provider: ConnectorPlatform, state: string): PendingState | undefined {
    const pending = this.oauthStates.get(this.stateKey(auth, provider, state))
    return pending ? structuredClone(pending) : undefined
  }
  wasOAuthConsumed(auth: AuthContext, provider: ConnectorPlatform, state: string): boolean { return this.consumedOAuthStates.has(this.stateKey(auth, provider, state)) }
  subjectKey(auth: Pick<AuthContext, 'tenantId' | 'subjectId'>): string { return `${auth.tenantId}\u0000${auth.subjectId}` }
  linkedAccountKey(auth: Pick<AuthContext, 'tenantId' | 'subjectId'>, provider: ConnectorPlatform): string { return `${this.subjectKey(auth)}\u0000${provider}` }
  private stateKey(auth: Pick<AuthContext, 'tenantId' | 'subjectId'>, provider: string, state: string): string { return `${this.subjectKey(auth)}\u0000${provider}\u0000${state}` }
}

type ApiOptions = { store: MemoryBackendStore; keyProvider: KeyProvider; exchange: OAuthCodeExchanger; revoker: ProviderTokenRevoker; now?: () => string; allowedRedirectUris: string[]; configuredProviders: ReadonlySet<string>; approvedProviders: ReadonlySet<string>; firstPartyAuth?: FirstPartyAuthStore; loginProviders?: Partial<Record<LoginProvider, FirstPartyOAuthProvider>> }

export class ApiService {
  private readonly now: () => string
  constructor(private readonly options: ApiOptions) { this.now = options.now ?? (() => new Date().toISOString()) }

  async handle(request: ApiRequest): Promise<ApiResponse> {
    if (request.method === 'GET' && request.path === '/healthz') return { status: 200, body: { status: 'ok' } }
    if (request.method === 'GET' && request.path === '/readyz') return { status: 200, body: { status: 'ready' } }

    try {
      if (request.method === 'GET' && request.path === '/v1/auth/providers') return { status: 200, body: loginProviderStatus(new Set(Object.keys(this.options.loginProviders ?? {}))) }
      const loginOAuth = request.path.match(/^\/v1\/auth\/(google|apple)\/(authorize|callback)$/)
      if (loginOAuth) return loginOAuth[2] === 'authorize' ? this.loginAuthorize(loginOAuth[1] as LoginProvider, request.body) : await this.loginCallback(loginOAuth[1] as LoginProvider, request.body)
      const session = this.options.firstPartyAuth?.verifySession(request.sessionToken)
      const auth = request.auth ?? (session ? { tenantId: session.subjectId, subjectId: session.subjectId, actorId: session.subjectId } : null)
      if (request.method === 'GET' && request.path === '/v1/auth/session') return auth ? { status: 200, body: { subjectId: auth.subjectId } } : { status: 401, body: { error: 'authentication_required' } }
      if (!auth) return { status: 401, body: { error: 'authentication_required' } }
      request = { ...request, auth }
      if (this.options.store.deletedSubjects.has(this.options.store.subjectKey(auth))) return { status: 404, body: { error: 'not_found' } }
      const oauth = request.path.match(/^\/v1\/oauth\/([a-z0-9_]+)\/(authorize|callback)$/)
      if (oauth) return oauth[2] === 'authorize'
        ? this.authorize(auth, oauth[1] as ConnectorPlatform, request.body)
        : await this.callback(auth, oauth[1] as ConnectorPlatform, request.body)
      if (request.method === 'GET' && request.path === '/v1/oauth/providers') return this.providerStatuses()
      if (request.method === 'GET' && request.path === '/v1/linked-accounts') return this.listLinkedAccounts(auth)
      const linkedAccount = request.path.match(/^\/v1\/linked-accounts\/([a-z0-9_]+)$/)
      if (request.method === 'DELETE' && linkedAccount) return await this.unlink(auth, linkedAccount[1] as ConnectorPlatform)
      if (request.method === 'POST' && request.path === '/v1/imports/archive') return this.admitArchive(auth, request.body)
      const correction = request.path.match(/^\/v1\/corrections\/([^/]+)$/)
      if (request.method === 'PUT' && correction) return this.correct(auth, decodeURIComponent(correction[1]!), request.body)
      if (request.method === 'POST' && request.path === '/v1/privacy/export') return this.export(auth, request.body)
      if (request.method === 'DELETE' && request.path === '/v1/privacy/account') return this.deleteAccount(auth, request.body)
      return { status: 404, body: { error: 'not_found' } }
    } catch (error) {
      if (request.auth) this.audit(request.auth, 'request-denied', 'request', 'deny', 'failed')
      return { status: 422, body: { error: 'request_rejected', message: error instanceof Error ? error.message : 'Rejected' } }
    }
  }

  private loginAuthorize(providerName: LoginProvider, body: unknown): ApiResponse {
    const auth = this.options.firstPartyAuth; const provider = this.options.loginProviders?.[providerName]
    if (!auth || !provider) return { status: 503, body: { error: 'provider_unconfigured', provider: providerName } }
    const redirectUri = text(object(body).redirectUri, 'redirectUri')
    if (!this.options.allowedRedirectUris.includes(redirectUri)) throw new Error('Redirect URI is not allowlisted')
    const pending = auth.begin({ purpose: 'login', provider: providerName, redirectUri, requestedScopes: provider.scopes, subjectId: null })
    const url = new URL(provider.authorizationEndpoint)
    url.searchParams.set('client_id', provider.clientId); url.searchParams.set('redirect_uri', redirectUri); url.searchParams.set('response_type', 'code'); url.searchParams.set('scope', provider.scopes.join(' ')); url.searchParams.set('state', pending.state); url.searchParams.set('code_challenge', pkceChallenge(pending.verifier)); url.searchParams.set('code_challenge_method', 'S256')
    return { status: 201, body: { authorizationUrl: url.toString(), state: pending.state, expiresAt: pending.expiresAt } }
  }

  private async loginCallback(providerName: LoginProvider, body: unknown): Promise<ApiResponse> {
    const auth = this.options.firstPartyAuth; const provider = this.options.loginProviders?.[providerName]
    if (!auth || !provider) return { status: 503, body: { error: 'provider_unconfigured', provider: providerName } }
    const input = object(body); const state = text(input.state, 'state'); const redirectUri = text(input.redirectUri, 'redirectUri'); const code = text(input.code, 'code')
    let pending
    try { pending = auth.consume(state, 'login', providerName, redirectUri, null) } catch (error) {
      if (error instanceof Error && error.message.includes('already consumed')) return { status: 409, body: { error: 'oauth_state_consumed' } }
      throw error
    }
    const identity = await provider.exchange({ code, codeVerifier: pending.verifier, redirectUri })
    const login = auth.login({ provider: providerName, providerSubject: identity.providerSubject, email: identity.email })
    return { status: 200, body: { authenticated: true, subjectId: login.subjectId, created: login.created }, headers: { 'set-cookie': `tbl_session=${login.session}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000` } }
  }

  private authorize(auth: AuthContext, provider: ConnectorPlatform, body: unknown): ApiResponse {
    const input = object(body); const redirectUri = text(input.redirectUri, 'redirectUri'); const scopes = strings(input.scopes, 'scopes')
    if (!(provider in CONNECTOR_REGISTRY)) throw new Error('Unknown provider')
    if (this.statusFor(provider) !== 'available') throw new Error(`${provider} OAuth is not available`)
    const pending = beginOAuthAuthorization({ context: tenant(auth, 'source-connection'), provider, redirectUri, allowedRedirectUris: this.options.allowedRedirectUris, requestedScopes: scopes, now: this.now() })
    this.options.store.saveOAuth(pending)
    this.audit(auth, 'oauth-started', provider, 'allow', 'succeeded')
    return { status: 201, body: { authorizationUrl: pending.authorizationUrl, state: pending.state, expiresAt: pending.expiresAt } }
  }

  private async callback(auth: AuthContext, provider: ConnectorPlatform, body: unknown): Promise<ApiResponse> {
    const input = object(body); const state = text(input.state, 'state')
    const pending = this.options.store.findOAuth(auth, provider, state)
    if (!pending) return this.options.store.wasOAuthConsumed(auth, provider, state)
      ? { status: 409, body: { error: 'oauth_state_consumed' } }
      : { status: 404, body: { error: 'oauth_state_not_found' } }
    const redirectUri = text(input.redirectUri, 'redirectUri'); const code = text(input.code, 'code')
    if (redirectUri !== pending.redirectUri || new Date(this.now()).valueOf() > new Date(pending.expiresAt).valueOf()) throw new Error('OAuth callback binding or expiry check failed')
    if (this.statusFor(provider) !== 'available') throw new Error(`${provider} OAuth is not available`)
    const accountKey = this.options.store.linkedAccountKey(auth, provider)
    if (this.options.store.linkedAccounts.has(accountKey)) throw new Error('Provider account is already linked')
    this.options.store.consumeOAuth(auth, provider, state)
    const exchanged = await this.options.exchange({ provider, code, codeVerifier: pending.codeVerifier, redirectUri })
    if (exchanged.grantedScopes.some((scope) => !pending.requestedScopes.includes(scope))) throw new Error('Provider granted an unexpected scope')
    const { key, keyId } = await this.options.keyProvider.dataKey(auth)
    const record = encryptProviderToken({ context: tenant(auth, 'connector-storage'), provider, scopes: exchanged.grantedScopes, token: JSON.stringify({ accessToken: exchanged.accessToken, refreshToken: exchanged.refreshToken ?? null, providerSubject: exchanged.providerSubject }), dataKey: key, keyId, createdAt: this.now() })
    this.options.store.tokenRecords.set(record.vaultRef, record)
    const linkedAt = this.now()
    const receipt: SourceConsentReceipt = { id: `consent:${randomUUID()}`, tenantId: auth.tenantId, subjectId: auth.subjectId, provider, providerSubject: exchanged.providerSubject, purpose: 'source-connection', scopes: [...exchanged.grantedScopes].sort(), grantedAt: linkedAt, revokedAt: null }
    this.options.store.consentReceipts.set(receipt.id, receipt)
    this.options.store.linkedAccounts.set(accountKey, { tenantId: auth.tenantId, subjectId: auth.subjectId, provider, providerSubject: exchanged.providerSubject, scopes: [...receipt.scopes], vaultRef: record.vaultRef, consentReceiptId: receipt.id, linkedAt })
    this.audit(auth, 'oauth-completed', provider, 'allow', 'succeeded')
    return { status: 200, body: { connected: true, provider, scopes: [...exchanged.grantedScopes].sort() } }
  }

  private providerStatuses(): ApiResponse {
    const statuses = linkedProviderStatus(this.options.configuredProviders, this.options.approvedProviders)
    const providers = Object.fromEntries(Object.entries(statuses).map(([provider, status]) => [provider, {
      status,
      scopes: status === 'available' ? [...CONNECTOR_REGISTRY[provider as ConnectorPlatform].allowedScopes] : [],
    }]))
    return { status: 200, body: { providers } }
  }

  private listLinkedAccounts(auth: AuthContext): ApiResponse {
    const accounts = [...this.options.store.linkedAccounts.values()]
      .filter((account) => account.tenantId === auth.tenantId && account.subjectId === auth.subjectId)
      .map(({ provider, providerSubject, scopes, linkedAt }) => ({ provider, providerSubject, scopes: [...scopes], linkedAt }))
      .sort((a, b) => a.provider.localeCompare(b.provider))
    return { status: 200, body: { accounts } }
  }

  private async unlink(auth: AuthContext, provider: ConnectorPlatform): Promise<ApiResponse> {
    if (!(provider in CONNECTOR_REGISTRY)) return { status: 404, body: { error: 'not_found' } }
    const key = this.options.store.linkedAccountKey(auth, provider)
    const account = this.options.store.linkedAccounts.get(key)
    if (!account) return { status: 404, body: { error: 'not_found' } }
    await this.options.revoker.revoke(provider, account.vaultRef)
    this.options.store.linkedAccounts.delete(key)
    this.options.store.tokenRecords.delete(account.vaultRef)
    const receipt = this.options.store.consentReceipts.get(account.consentReceiptId)
    if (receipt && !receipt.revokedAt) receipt.revokedAt = this.now()
    this.audit(auth, 'oauth-unlinked', provider, 'allow', 'succeeded')
    return { status: 200, body: { unlinked: true, provider } }
  }

  private statusFor(provider: ConnectorPlatform): ProviderAvailability {
    return linkedProviderStatus(this.options.configuredProviders, this.options.approvedProviders)[provider]
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
    for (const [id, item] of this.options.store.linkedAccounts) if (item.tenantId === auth.tenantId && item.subjectId === auth.subjectId) this.options.store.linkedAccounts.delete(id)
    for (const item of this.options.store.consentReceipts.values()) if (item.tenantId === auth.tenantId && item.subjectId === auth.subjectId && !item.revokedAt) item.revokedAt = this.now()
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
