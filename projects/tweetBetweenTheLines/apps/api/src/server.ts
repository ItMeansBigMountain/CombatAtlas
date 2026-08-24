import { createServer } from 'node:http'
import { Buffer } from 'node:buffer'

import { ApiService, FixedKeyProvider, MemoryBackendStore, type ApiRequest, type OAuthCodeExchanger } from './index.js'

const keyText = process.env.LOCAL_DATA_KEY_BASE64
if (!keyText) throw new Error('LOCAL_DATA_KEY_BASE64 is required (32 bytes, base64)')
const key = Buffer.from(keyText, 'base64')
const exchange: OAuthCodeExchanger = async () => { throw new Error('No live OAuth exchanger configured; inject an official provider adapter') }
const api = new ApiService({ store: new MemoryBackendStore(), keyProvider: new FixedKeyProvider(key, 'local-env-v1'), exchange, allowedRedirectUris: (process.env.OAUTH_REDIRECT_URIS ?? '').split(',').filter(Boolean) })
const port = Number(process.env.PORT ?? '3001')

createServer(async (incoming, response) => {
  const chunks: Buffer[] = []
  for await (const chunk of incoming) chunks.push(Buffer.from(chunk))
  let body: unknown
  try { body = chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : undefined } catch { response.writeHead(400, { 'content-type': 'application/json' }).end(JSON.stringify({ error: 'invalid_json' })); return }
  const tenantId = incoming.headers['x-tenant-id']; const subjectId = incoming.headers['x-subject-id']; const actorId = incoming.headers['x-actor-id']
  const auth = typeof tenantId === 'string' && typeof subjectId === 'string' && typeof actorId === 'string' ? { tenantId, subjectId, actorId } : null
  const result = await api.handle({ method: incoming.method as ApiRequest['method'], path: new URL(incoming.url ?? '/', 'http://local').pathname, auth, body })
  response.writeHead(result.status, { 'content-type': 'application/json', 'cache-control': 'no-store' }).end(JSON.stringify(result.body))
}).listen(port, '127.0.0.1', () => console.log(JSON.stringify({ event: 'api-listening', host: '127.0.0.1', port })))
