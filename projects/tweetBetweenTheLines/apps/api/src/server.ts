import { createServer } from 'node:http'
import { Buffer } from 'node:buffer'

import { ApiService, FirstPartyAuthStore, FixedKeyProvider, MemoryBackendStore, type ApiRequest, type FirstPartyOAuthProvider, type OAuthCodeExchanger } from './index.js'

const keyText = process.env.LOCAL_DATA_KEY_BASE64
if (!keyText) throw new Error('LOCAL_DATA_KEY_BASE64 is required (32 bytes, base64)')
const key = Buffer.from(keyText, 'base64')
const exchange: OAuthCodeExchanger = async () => { throw new Error('No live OAuth exchanger configured; inject an official provider adapter') }
const revoker = { async revoke(): Promise<'revoked'> { throw new Error('No live provider revoker configured; unlink denied') } }
const configuredProviders = new Set((process.env.OAUTH_CONFIGURED_PROVIDERS ?? '').split(',').filter(Boolean))
const approvedProviders = new Set((process.env.OAUTH_APPROVED_PROVIDERS ?? '').split(',').filter(Boolean))
const allowedRedirectUris = (process.env.OAUTH_REDIRECT_URIS ?? '').split(',').filter(Boolean)
const loginProviders: Partial<Record<'google' | 'apple', FirstPartyOAuthProvider>> = {}
if (process.env.GOOGLE_OAUTH_CLIENT_ID && process.env.GOOGLE_OAUTH_CLIENT_SECRET) loginProviders.google = {
  authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth', clientId: process.env.GOOGLE_OAUTH_CLIENT_ID, scopes: ['openid', 'email'],
  async exchange(input) {
    const tokenResponse = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ code: input.code, client_id: process.env.GOOGLE_OAUTH_CLIENT_ID!, client_secret: process.env.GOOGLE_OAUTH_CLIENT_SECRET!, redirect_uri: input.redirectUri, grant_type: 'authorization_code', code_verifier: input.codeVerifier }) })
    if (!tokenResponse.ok) throw new Error('Google OAuth token exchange failed')
    const tokens = await tokenResponse.json() as { access_token?: string }
    if (!tokens.access_token) throw new Error('Google OAuth access token missing')
    const userResponse = await fetch('https://openidconnect.googleapis.com/v1/userinfo', { headers: { authorization: `Bearer ${tokens.access_token}` } })
    if (!userResponse.ok) throw new Error('Google OpenID identity lookup failed')
    const identity = await userResponse.json() as { sub?: string; email?: string }
    if (!identity.sub) throw new Error('Google OpenID subject missing')
    return { providerSubject: identity.sub, email: identity.email ?? null }
  },
}
const api = new ApiService({ store: new MemoryBackendStore(), keyProvider: new FixedKeyProvider(key, 'local-env-v1'), exchange, revoker, configuredProviders, approvedProviders, allowedRedirectUris, firstPartyAuth: new FirstPartyAuthStore(), loginProviders })
const port = Number(process.env.PORT ?? '3001')

createServer(async (incoming, response) => {
  const chunks: Buffer[] = []
  for await (const chunk of incoming) chunks.push(Buffer.from(chunk))
  let body: unknown
  try { body = chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : undefined } catch { response.writeHead(400, { 'content-type': 'application/json' }).end(JSON.stringify({ error: 'invalid_json' })); return }
  const requestUrl = new URL(incoming.url ?? '/', 'http://local')
  if (incoming.method === 'GET' && /^\/v1\/auth\/(google|apple)\/callback$/.test(requestUrl.pathname)) body = { state: requestUrl.searchParams.get('state'), code: requestUrl.searchParams.get('code'), redirectUri: requestUrl.searchParams.get('redirect_uri') }
  const tenantId = incoming.headers['x-tenant-id']; const subjectId = incoming.headers['x-subject-id']; const actorId = incoming.headers['x-actor-id']
  const auth = process.env.TRUST_DEV_AUTH_HEADERS === 'true' && typeof tenantId === 'string' && typeof subjectId === 'string' && typeof actorId === 'string' ? { tenantId, subjectId, actorId } : null
  const sessionToken = incoming.headers.cookie?.split(';').map((part) => part.trim()).find((part) => part.startsWith('tbl_session='))?.slice('tbl_session='.length)
  const result = await api.handle({ method: incoming.method as ApiRequest['method'], path: requestUrl.pathname, auth, body, sessionToken })
  response.writeHead(result.status, { 'content-type': 'application/json', 'cache-control': 'no-store', ...result.headers }).end(JSON.stringify(result.body))
}).listen(port, '0.0.0.0', () => console.log(JSON.stringify({ event: 'api-listening', host: '0.0.0.0', port })))
