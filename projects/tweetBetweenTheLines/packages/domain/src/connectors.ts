import { createHash, randomBytes } from 'node:crypto'
import { buildCryptographicDeletion, normalizeProvenanceEvent, requireTenantContext, type ProvenanceRichEvent, type TenantContext } from './accountData.js'

export type ConnectorDecision = 'supported_api' | 'supported_archive_import' | 'manual_import_first' | 'blocked_or_restricted' | 'unsupported'
export type ConnectorDefinition = {
  platform: string
  decision: ConnectorDecision
  apiSupported: boolean
  archiveSupported: boolean
  pkce: boolean
  authorizationEndpoint: string | null
  allowedScopes: string[]
  requiresReview: boolean
  requiresPaidTier: boolean
  limitations: string[]
}

export const CONNECTOR_REGISTRY = {
  google_youtube: { platform: 'google_youtube', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth', allowedScopes: ['openid', 'email', 'profile', 'https://www.googleapis.com/auth/youtube.readonly'], requiresReview: true, requiresPaidTier: false, limitations: ['API does not provide complete YouTube history; use official Takeout for archive history.'] },
  reddit: { platform: 'reddit', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: 'https://www.reddit.com/api/v1/authorize', allowedScopes: ['identity', 'history', 'read', 'save', 'vote', 'mysubreddits'], requiresReview: false, requiresPaidTier: false, limitations: ['Endpoint and rate limits may omit account history.'] },
  discord: { platform: 'discord', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: 'https://discord.com/oauth2/authorize', allowedScopes: ['identify', 'email', 'guilds', 'connections'], requiresReview: false, requiresPaidTier: false, limitations: ['OAuth is not private-message history access.'] },
  bluesky_atproto: { platform: 'bluesky_atproto', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: null, allowedScopes: ['atproto'], requiresReview: false, requiresPaidTier: false, limitations: ['Authorization endpoint and limits are discovered per PDS.'] },
  spotify: { platform: 'spotify', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: 'https://accounts.spotify.com/authorize', allowedScopes: ['user-read-recently-played', 'user-top-read', 'user-library-read', 'playlist-read-private'], requiresReview: true, requiresPaidTier: false, limitations: ['Extended listening history requires an official data export.'] },
  mastodon_fediverse: { platform: 'mastodon_fediverse', decision: 'supported_api', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: null, allowedScopes: ['read', 'read:accounts', 'read:statuses', 'read:favourites'], requiresReview: false, requiresPaidTier: false, limitations: ['Endpoint, capabilities, and limits vary per instance.'] },
  x_twitter: { platform: 'x_twitter', decision: 'supported_archive_import', apiSupported: true, archiveSupported: true, pkce: true, authorizationEndpoint: 'https://twitter.com/i/oauth2/authorize', allowedScopes: ['tweet.read', 'users.read', 'offline.access'], requiresReview: true, requiresPaidTier: true, limitations: ['API history is tier-limited and not complete.'] },
  facebook: { platform: 'facebook', decision: 'manual_import_first', apiSupported: false, archiveSupported: true, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['Full consumer history is not available through an approved broad API.'] },
  instagram: { platform: 'instagram', decision: 'manual_import_first', apiSupported: false, archiveSupported: true, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['Official archive is required for personal history.'] },
  tiktok: { platform: 'tiktok', decision: 'manual_import_first', apiSupported: false, archiveSupported: true, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['Login Kit is not activity history access.'] },
  linkedin: { platform: 'linkedin', decision: 'manual_import_first', apiSupported: false, archiveSupported: true, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['Profile products are gated and not a full-history feed.'] },
  snapchat: { platform: 'snapchat', decision: 'manual_import_first', apiSupported: false, archiveSupported: true, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['Login Kit exposes identity, not snaps or chats.'] },
  threads: { platform: 'threads', decision: 'blocked_or_restricted', apiSupported: false, archiveSupported: false, pkce: false, authorizationEndpoint: null, allowedScopes: [], requiresReview: true, requiresPaidTier: false, limitations: ['No approved complete personal-history connector.'] },
} as const satisfies Record<string, ConnectorDefinition>

export type ConnectorPlatform = keyof typeof CONNECTOR_REGISTRY

export function assertConnectorAvailable(platform: ConnectorPlatform, lane: 'api' | 'history', gates: { reviewApproved: boolean; paidTier: boolean }): ConnectorDefinition {
  const connector: ConnectorDefinition = CONNECTOR_REGISTRY[platform]
  if (connector.decision === 'blocked_or_restricted' || connector.decision === 'unsupported') throw new Error(`${platform} ${lane} is not available`)
  if (lane === 'api' && !connector.apiSupported) throw new Error(`${platform} API is not available; use an official archive`)
  if (lane === 'history' && !connector.archiveSupported) throw new Error(`${platform} history is not available`)
  if (lane === 'api' && connector.requiresReview && !gates.reviewApproved) throw new Error(`${platform} requires approved app review`)
  if (lane === 'api' && connector.requiresPaidTier && !gates.paidTier) throw new Error(`${platform} requires a paid tier for this API lane`)
  return connector
}

export type PendingOAuthAuthorization = {
  context: TenantContext; provider: ConnectorPlatform; redirectUri: string; requestedScopes: string[]; state: string
  codeVerifier: string; codeChallenge: string; codeChallengeMethod: 'S256'; authorizationUrl: string; expiresAt: string; used: boolean
}

const base64url = (bytes: Buffer) => bytes.toString('base64url')
export function beginOAuthAuthorization(input: { context: TenantContext; provider: ConnectorPlatform; redirectUri: string; allowedRedirectUris: string[]; requestedScopes: string[]; now: string }): PendingOAuthAuthorization {
  const context = requireTenantContext(input.context)
  const connector = CONNECTOR_REGISTRY[input.provider]
  if (!connector.apiSupported || !connector.pkce || !connector.authorizationEndpoint) throw new Error(`${input.provider} OAuth is not available in this runtime`)
  if (!input.allowedRedirectUris.includes(input.redirectUri)) throw new Error('OAuth redirect URI is not allowlisted')
  const requestedScopes = [...new Set(input.requestedScopes)].sort()
  const unexpected = requestedScopes.filter((scope) => !(connector.allowedScopes as readonly string[]).includes(scope))
  if (unexpected.length) throw new Error(`Unexpected OAuth scopes: ${unexpected.join(', ')}`)
  const now = new Date(input.now)
  if (Number.isNaN(now.valueOf())) throw new Error('Invalid timestamp')
  const codeVerifier = base64url(randomBytes(48)); const codeChallenge = createHash('sha256').update(codeVerifier).digest('base64url')
  const statePayload = `${context.tenantId}:${context.subjectId}:${input.provider}:${input.redirectUri}:${base64url(randomBytes(32))}`
  const state = createHash('sha256').update(statePayload).digest('base64url')
  const url = new URL(connector.authorizationEndpoint)
  url.searchParams.set('response_type', 'code'); url.searchParams.set('redirect_uri', input.redirectUri); url.searchParams.set('scope', requestedScopes.join(' ')); url.searchParams.set('state', state); url.searchParams.set('code_challenge', codeChallenge); url.searchParams.set('code_challenge_method', 'S256')
  return { context, provider: input.provider, redirectUri: input.redirectUri, requestedScopes, state, codeVerifier, codeChallenge, codeChallengeMethod: 'S256', authorizationUrl: url.toString(), expiresAt: new Date(now.valueOf() + 10 * 60_000).toISOString(), used: false }
}

export function completeOAuthAuthorization(pending: PendingOAuthAuthorization, callback: { context: TenantContext; provider: ConnectorPlatform; redirectUri: string; state: string; grantedScopes: string[]; now: string }) {
  if (pending.used) throw new Error('OAuth state was already used')
  const context = requireTenantContext(callback.context, pending.context.tenantId)
  if (context.subjectId !== pending.context.subjectId || callback.provider !== pending.provider || callback.redirectUri !== pending.redirectUri || callback.state !== pending.state) throw new Error('OAuth callback binding mismatch')
  if (new Date(callback.now).toISOString() > pending.expiresAt) throw new Error('OAuth state expired')
  const grantedScopes = [...new Set(callback.grantedScopes)].sort()
  if (grantedScopes.some((scope) => !pending.requestedScopes.includes(scope))) throw new Error('Provider granted an unexpected scope')
  pending.used = true
  return { provider: pending.provider, grantedScopes, codeVerifier: pending.codeVerifier, stateConsumed: true as const }
}

export function createRateLimitBudget(input: { provider: string; capacity: number; resetAt: string }) {
  if (!Number.isSafeInteger(input.capacity) || input.capacity <= 0) throw new Error('Positive integer capacity is required')
  let remaining = input.capacity; let resetAt = new Date(input.resetAt).toISOString()
  return { consume(cost: number, nowValue: string) { const now = new Date(nowValue).toISOString(); if (now >= resetAt) { remaining = input.capacity; resetAt = new Date(new Date(now).valueOf() + 60_000).toISOString() } if (!Number.isSafeInteger(cost) || cost <= 0 || cost > remaining) throw new Error(`${input.provider} rate limit exhausted; retry after ${resetAt}`); remaining -= cost; return { remaining, resetAt } } }
}

export type ArchiveEntry = { path: string; compressedBytes: number; uncompressedBytes: number; kind: 'file' | 'directory' | 'symlink' | 'device'; mime: string; magic: string; sha256: string }
export type ArchiveEnvelope = { format: 'zip'; compressedBytes: number; entries: ArchiveEntry[]; malwareScan?: 'clean' | 'infected' | 'unavailable'; nestedDepth?: number }
export function inspectArchive(archive: ArchiveEnvelope) {
  if (archive.malwareScan === 'infected') throw new Error('Archive failed malware scan')
  if (archive.malwareScan !== 'clean') throw new Error('Archive malware scan unavailable; fail closed')
  if (archive.compressedBytes <= 0 || archive.compressedBytes > 250_000_000) throw new Error('Archive compressed size is outside limits')
  if (archive.entries.length > 10_000) throw new Error('Archive entry limit exceeded')
  if ((archive.nestedDepth ?? 0) > 1) throw new Error('Nested archive depth exceeded')
  let total = 0
  for (const entry of archive.entries) {
    const normalized = entry.path.normalize('NFKC').replaceAll('\\', '/')
    if (normalized.startsWith('/') || /^[A-Za-z]:\//.test(normalized) || normalized.split('/').includes('..') || normalized.includes('\0')) throw new Error('Archive path traversal detected')
    if (entry.kind === 'symlink' || entry.kind === 'device') throw new Error(`Archive entry kind ${entry.kind} is not allowed`)
    if (entry.uncompressedBytes > 50_000_000) throw new Error('Archive entry size limit exceeded')
    if ((entry.mime === 'application/json' && entry.magic !== 'json') || !/^[a-f0-9]{64}$/.test(entry.sha256)) throw new Error('Archive MIME, magic, or digest validation failed')
    total += entry.uncompressedBytes
  }
  if (total > 1_000_000_000 || total / archive.compressedBytes > 100) throw new Error('Archive expansion ratio limit exceeded')
  return { accepted: true as const, entryCount: archive.entries.length, uncompressedBytes: total, sandbox: { network: 'denied', runtime: 'read-only', privilege: 'unprivileged', executeContent: false } }
}

export type ArchiveSchema = { platform: string; schemaVersion: string; paths: string[]; recordIdFields: string[] }
export function registerArchiveSchema(registry: ArchiveSchema[], schema: ArchiveSchema): ArchiveSchema[] {
  if (registry.some((item) => item.platform === schema.platform && item.schemaVersion === schema.schemaVersion)) throw new Error('Archive schema version already registered')
  if (!/^[-a-z0-9_]+@\d+$/.test(schema.schemaVersion) || !schema.paths.length || !schema.recordIdFields.length) throw new Error('Invalid archive schema registration')
  return [...registry, structuredClone(schema)]
}

type ImportRecord = { sourceRecordId: string; occurredAt: string; category: string; content: string; locale?: string }
export type ArchiveImportPlan = { context: TenantContext; sourceId: string; platform: string; schemaVersion: string; archiveDigest: string; consentReceiptId: string; records: ImportRecord[] }
export function createArchiveImportPlan(input: ArchiveImportPlan, registry: ArchiveSchema[]): ArchiveImportPlan {
  const context = requireTenantContext(input.context)
  if (!registry.some((schema) => schema.platform === input.platform && schema.schemaVersion === input.schemaVersion)) throw new Error('Unsupported archive schema version')
  if (!/^[a-f0-9]{64}$/.test(input.archiveDigest)) throw new Error('Invalid archive digest')
  const ids = new Set<string>()
  for (const record of input.records) { if (!record.sourceRecordId.trim() || ids.has(record.sourceRecordId)) throw new Error('Archive records require unique source IDs'); ids.add(record.sourceRecordId) }
  return { ...structuredClone(input), context }
}

export class ArchiveImportStore {
  #events = new Map<string, ProvenanceRichEvent>()
  ingest(plan: ArchiveImportPlan) { let inserted = 0; let skipped = 0; for (const record of plan.records) { const event = normalizeProvenanceEvent({ tenantId: plan.context.tenantId, subjectId: plan.context.subjectId, sourceId: plan.sourceId, sourceRecordId: record.sourceRecordId, consentReceiptId: plan.consentReceiptId, category: record.category, kind: 'archive-import', occurredAt: record.occurredAt, ingestedAt: record.occurredAt, locale: record.locale ?? null, content: record.content, lineage: { sourceKey: `${plan.platform}:${plan.archiveDigest}`, rawObjectRef: null, analyzerVersion: plan.schemaVersion } }, plan.context); if (this.#events.has(event.id)) skipped += 1; else { this.#events.set(event.id, event); inserted += 1 } } return { inserted, skipped } }
  eventsForSource(context: TenantContext, sourceId: string) { const verified = requireTenantContext(context); return [...this.#events.values()].filter((event) => event.tenantId === verified.tenantId && event.subjectId === verified.subjectId && event.sourceId === sourceId).map((event) => structuredClone(event)) }
  deleteSource(context: TenantContext, sourceId: string) { const matches = this.eventsForSource(context, sourceId); for (const event of matches) this.#events.delete(event.id); return matches.length }
}

export type ConnectorRuntime = { tenantId: string; subjectId: string; sourceId: string; platform: ConnectorPlatform; status: 'active' | 'revoked'; ingestionEnabled: boolean; revokedAt: string | null; revocationReason: string | null }
export function createConnectorRuntime(context: TenantContext, sourceId: string, platform: ConnectorPlatform): ConnectorRuntime { const verified = requireTenantContext(context); return { tenantId: verified.tenantId, subjectId: verified.subjectId, sourceId: sourceId.trim(), platform, status: 'active', ingestionEnabled: true, revokedAt: null, revocationReason: null } }
export function revokeConnector(runtime: ConnectorRuntime, context: TenantContext, revokedAt: string, reason: string): ConnectorRuntime { const verified = requireTenantContext(context, runtime.tenantId); if (verified.subjectId !== runtime.subjectId) throw new Error('Subject context mismatch'); return { ...runtime, status: 'revoked', ingestionEnabled: false, revokedAt: new Date(revokedAt).toISOString(), revocationReason: reason.trim() } }
export function deleteSourceData(input: { context: TenantContext; sourceId: string; descendantRefs: string[]; keyIds: string[] }) { const context = requireTenantContext(input.context); return buildCryptographicDeletion({ tenantId: context.tenantId, subjectId: context.subjectId, sourceId: input.sourceId, descendantRefs: input.descendantRefs, keyIds: input.keyIds }) }
