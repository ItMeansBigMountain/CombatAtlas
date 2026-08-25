import { createHash, randomBytes, randomUUID } from 'node:crypto'

import { CONNECTOR_REGISTRY, type ConnectorPlatform } from '@tweet-between-the-lines/domain'

export type LoginProvider = 'google' | 'apple'
export type ProviderAvailability = 'available' | 'unconfigured' | 'pending_review' | 'archive_only' | 'unavailable'
export type OAuthPurpose = 'login' | 'link'
export type OAuthTransaction = {
  purpose: OAuthPurpose
  provider: string
  state: string
  verifier: string
  redirectUri: string
  requestedScopes: string[]
  subjectId: string | null
  expiresAt: string
}
export type Identity = { provider: LoginProvider; providerSubject: string; email: string | null }
export type FirstPartyOAuthProvider = {
  authorizationEndpoint: string
  clientId: string
  scopes: string[]
  exchange(input: { code: string; codeVerifier: string; redirectUri: string }): Promise<{ providerSubject: string; email: string | null }>
}
export type LinkedAccount = { provider: ConnectorPlatform; providerSubject: string; scopes: string[]; vaultRef: string; linkedAt: string }
export type ConsentReceipt = { id: string; subjectId: string; provider: string; purpose: OAuthPurpose; scopes: string[]; grantedAt: string; revokedAt: string | null }

export interface ProviderTokenRevoker { revoke(provider: ConnectorPlatform, vaultRef: string): Promise<'revoked' | 'already_revoked'> }

export class FirstPartyAuthStore {
  readonly transactions = new Map<string, OAuthTransaction>()
  readonly consumedStates = new Set<string>()
  readonly identities = new Map<string, { subjectId: string; identity: Identity }>()
  readonly linkedAccounts = new Map<string, LinkedAccount>()
  readonly consents = new Map<string, ConsentReceipt>()
  readonly sessions = new Map<string, { subjectId: string; createdAt: string; expiresAt: string }>()
  constructor(private readonly now: () => string = () => new Date().toISOString()) {}

  begin(input: Omit<OAuthTransaction, 'state' | 'verifier' | 'expiresAt'>): OAuthTransaction {
    const verifier = randomBytes(48).toString('base64url')
    const state = randomBytes(32).toString('base64url')
    const transaction = { ...input, verifier, state, expiresAt: new Date(new Date(this.now()).valueOf() + 10 * 60_000).toISOString() }
    this.transactions.set(state, transaction)
    return structuredClone(transaction)
  }
  consume(state: string, purpose: OAuthPurpose, provider: string, redirectUri: string, subjectId: string | null): OAuthTransaction {
    if (this.consumedStates.has(state)) throw new Error('OAuth state already consumed')
    const transaction = this.transactions.get(state)
    if (!transaction) throw new Error('OAuth state not found')
    if (transaction.purpose !== purpose || transaction.provider !== provider || transaction.redirectUri !== redirectUri || transaction.subjectId !== subjectId) throw new Error('OAuth callback binding mismatch')
    if (new Date(this.now()).valueOf() > new Date(transaction.expiresAt).valueOf()) throw new Error('OAuth state expired')
    this.transactions.delete(state); this.consumedStates.add(state)
    return transaction
  }
  login(identity: Identity): { subjectId: string; session: string; created: boolean } {
    const key = `${identity.provider}\u0000${identity.providerSubject}`
    const existing = this.identities.get(key)
    const subjectId = existing?.subjectId ?? `user:${randomUUID()}`
    if (!existing) this.identities.set(key, { subjectId, identity: structuredClone(identity) })
    for (const [digest, stored] of this.sessions) if (stored.subjectId === subjectId) this.sessions.delete(digest)
    const session = randomBytes(32).toString('base64url')
    this.sessions.set(createHash('sha256').update(session).digest('hex'), { subjectId, createdAt: this.now(), expiresAt: new Date(new Date(this.now()).valueOf() + 30 * 24 * 60 * 60_000).toISOString() })
    return { subjectId, session, created: !existing }
  }
  verifySession(session: string | undefined): { subjectId: string } | null {
    if (!session) return null
    const digest = createHash('sha256').update(session).digest('hex')
    const stored = this.sessions.get(digest)
    if (!stored) return null
    if (new Date(this.now()).valueOf() > new Date(stored.expiresAt).valueOf()) { this.sessions.delete(digest); return null }
    return { subjectId: stored.subjectId }
  }
  link(subjectId: string, account: LinkedAccount): ConsentReceipt {
    this.linkedAccounts.set(`${subjectId}\u0000${account.provider}`, structuredClone(account))
    const receipt: ConsentReceipt = { id: `consent:${randomUUID()}`, subjectId, provider: account.provider, purpose: 'link', scopes: [...account.scopes], grantedAt: this.now(), revokedAt: null }
    this.consents.set(receipt.id, receipt)
    return structuredClone(receipt)
  }
  list(subjectId: string): LinkedAccount[] { return [...this.linkedAccounts.entries()].filter(([key]) => key.startsWith(`${subjectId}\u0000`)).map(([, value]) => structuredClone(value)) }
  async unlink(subjectId: string, provider: ConnectorPlatform, revoker: ProviderTokenRevoker): Promise<boolean> {
    const key = `${subjectId}\u0000${provider}`; const account = this.linkedAccounts.get(key)
    if (!account) return false
    await revoker.revoke(provider, account.vaultRef)
    this.linkedAccounts.delete(key)
    for (const receipt of this.consents.values()) if (receipt.subjectId === subjectId && receipt.provider === provider && !receipt.revokedAt) receipt.revokedAt = this.now()
    return true
  }
}

export function loginProviderStatus(configured: ReadonlySet<string>): Record<LoginProvider, ProviderAvailability> {
  return { google: configured.has('google') ? 'available' : 'unconfigured', apple: configured.has('apple') ? 'available' : 'unconfigured' }
}

export function linkedProviderStatus(configured: ReadonlySet<string>, approved: ReadonlySet<string>): Record<ConnectorPlatform, ProviderAvailability> {
  return Object.fromEntries(Object.entries(CONNECTOR_REGISTRY).map(([provider, connector]) => {
    let status: ProviderAvailability
    if (!connector.apiSupported || !connector.authorizationEndpoint) status = connector.archiveSupported ? 'archive_only' : 'unavailable'
    else if (!configured.has(provider)) status = 'unconfigured'
    else if (connector.requiresReview && !approved.has(provider)) status = 'pending_review'
    else status = 'available'
    return [provider, status]
  })) as Record<ConnectorPlatform, ProviderAvailability>
}

export function pkceChallenge(verifier: string): string { return createHash('sha256').update(verifier).digest('base64url') }
