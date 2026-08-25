import { Buffer } from 'node:buffer'
import { createHash } from 'node:crypto'
import yauzl, { type Entry, type ZipFile } from 'yauzl'

export type PlanId = 'free' | 'premium' | 'premium_ai'
export const ENTITLEMENTS = {
  free: { importSuccessesPerRolling30Days: 2, maxCompressedImportBytes: 262_144_000, maxActiveAccounts: 1 },
  premium: { importSuccessesPerRolling30Days: 20, maxCompressedImportBytes: 2_147_483_648, maxActiveAccounts: 10 },
  premium_ai: { importSuccessesPerRolling30Days: 20, maxCompressedImportBytes: 2_147_483_648, maxActiveAccounts: 10 },
} as const

export type ArchiveUploadOptions = {
  tenantId: string
  subjectId: string
  sourceId: string
  consentReceiptId: string
  malwareScan: 'clean' | 'infected' | 'unavailable'
  plan: PlanId
  successfulImportsInRolling30Days: number
  activeAccounts: number
  importedAt: string
}

type Category = 'posts' | 'likes' | 'follows' | 'watch_history'
type ExtractedFile = { path: string; data: Buffer }
export type NormalizedArchiveRecord = {
  id: string
  sourceRecordId: string
  category: Category
  kind: 'archive-import'
  occurredAt: string
  locale: string | null
  content: string
  metadata: Record<string, string | number | boolean | null>
  provenance: { archiveSha256: string; rawObjectRef: string; parserVersion: string; consentReceiptId: string }
}

export function assertImportEntitlement(input: Pick<ArchiveUploadOptions, 'plan' | 'successfulImportsInRolling30Days' | 'activeAccounts'> & { compressedBytes: number }): void {
  const limits = ENTITLEMENTS[input.plan]
  if (!Number.isSafeInteger(input.compressedBytes) || input.compressedBytes <= 0 || input.compressedBytes > limits.maxCompressedImportBytes) throw new Error('Compressed import exceeds plan limit')
  if (input.successfulImportsInRolling30Days >= limits.importSuccessesPerRolling30Days) throw new Error('Rolling 30-day import limit reached')
  if (input.activeAccounts > limits.maxActiveAccounts) throw new Error('Active account limit exceeded')
}

function openZip(buffer: Buffer): Promise<ZipFile> {
  return new Promise((resolve, reject) => yauzl.fromBuffer(buffer, { lazyEntries: true, decodeStrings: true, validateEntrySizes: true }, (error, zip) => error || !zip ? reject(new Error(`Invalid ZIP archive: ${error?.message ?? 'unable to open'}`)) : resolve(zip)))
}

function readEntry(zip: ZipFile, entry: Entry): Promise<Buffer> {
  return new Promise((resolve, reject) => zip.openReadStream(entry, (error, stream) => {
    if (error || !stream) return reject(error ?? new Error('Unable to read ZIP entry'))
    const chunks: Buffer[] = []; let size = 0
    stream.on('data', (chunk: Buffer) => { size += chunk.length; if (size > 50_000_000) stream.destroy(new Error('Archive entry size limit exceeded')); else chunks.push(Buffer.from(chunk)) })
    stream.once('error', reject); stream.once('end', () => resolve(Buffer.concat(chunks)))
  }))
}

async function extractZip(buffer: Buffer): Promise<ExtractedFile[]> {
  const zip = await openZip(buffer)
  return await new Promise((resolve, reject) => {
    const files: ExtractedFile[] = []; let entries = 0; let total = 0; let settled = false
    const fail = (error: unknown) => { if (!settled) { settled = true; zip.close(); reject(error) } }
    zip.once('error', fail)
    zip.once('end', () => { if (!settled) { settled = true; resolve(files) } })
    zip.on('entry', async (entry: Entry) => {
      try {
        entries += 1
        if (entries > 10_000) throw new Error('Archive entry limit exceeded')
        const path = entry.fileName.normalize('NFKC').replaceAll('\\', '/')
        if (!path || path.includes('\0') || path.startsWith('/') || /^[A-Za-z]:\//.test(path) || path.split('/').includes('..')) throw new Error('Archive path traversal detected')
        if ((entry.externalFileAttributes >>> 16 & 0o170000) === 0o120000) throw new Error('Archive symlink is not allowed')
        if ((entry.generalPurposeBitFlag & 1) !== 0) throw new Error('Encrypted ZIP entries are not supported')
        if (entry.uncompressedSize > 50_000_000) throw new Error('Archive entry size limit exceeded')
        total += entry.uncompressedSize
        if (total > 1_000_000_000 || total / buffer.length > 100) throw new Error('Archive expansion ratio limit exceeded')
        if (path.toLowerCase().endsWith('.zip')) throw new Error('Nested archive depth exceeded')
        if (path.endsWith('/')) { zip.readEntry(); return }
        const data = await readEntry(zip, entry)
        files.push({ path, data }); zip.readEntry()
      } catch (error) { fail(error) }
    })
    zip.readEntry()
  })
}

const sha256 = (value: Buffer | string) => createHash('sha256').update(value).digest('hex')
const iso = (value: unknown, fallback: string): string => {
  if (typeof value !== 'string' || !value.trim()) return new Date(fallback).toISOString()
  const spotify = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(value) ? `${value.replace(' ', 'T')}:00Z` : value
  const parsed = new Date(spotify); if (Number.isNaN(parsed.valueOf())) throw new Error(`Invalid archive timestamp: ${value}`)
  return parsed.toISOString()
}
const parseJson = (file: ExtractedFile): unknown => {
  let text = file.data.toString('utf8').replace(/^\uFEFF/, '').trim()
  const assignment = text.indexOf('=')
  if (/^(window\.)?YTD\./.test(text) && assignment >= 0) text = text.slice(assignment + 1).trim().replace(/;$/, '')
  try { return JSON.parse(text) } catch { throw new Error(`Invalid JSON in ${file.path}`) }
}
const cleanHtml = (value: unknown): string => String(value ?? '').replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/\s+/g, ' ').trim()

function parseCsv(text: string): string[][] {
  const rows: string[][] = []; let row: string[] = []; let field = ''; let quoted = false
  for (let i = 0; i < text.length; i += 1) { const char = text[i]; if (char === '"') { if (quoted && text[i + 1] === '"') { field += '"'; i += 1 } else quoted = !quoted } else if (char === ',' && !quoted) { row.push(field); field = '' } else if ((char === '\n' || char === '\r') && !quoted) { if (char === '\r' && text[i + 1] === '\n') i += 1; row.push(field); if (row.some(Boolean)) rows.push(row); row = []; field = '' } else field += char }
  if (quoted) throw new Error('Malformed CSV: unclosed quoted field'); if (field || row.length) { row.push(field); rows.push(row) } return rows
}

type Parsed = Omit<NormalizedArchiveRecord, 'id' | 'kind' | 'provenance'> & { rawObjectRef: string }
type Detection = { platform: string; parserVersion: string; certainty: number }
function detect(files: ExtractedFile[]): Detection | null {
  const paths = new Set(files.map((file) => file.path))
  if ([...paths].some((path) => /(^|\/)StreamingHistory[^/]*\.json$/i.test(path) || /(^|\/)endsong[^/]*\.json$/i.test(path) || /(^|\/)YourLibrary\.json$/i.test(path))) return { platform: 'spotify', parserVersion: 'spotify_archive@1', certainty: 1 }
  if (paths.has('data/tweets.js') || paths.has('data/like.js') || paths.has('data/following.js')) return { platform: 'x_twitter', parserVersion: 'x_twitter_archive@1', certainty: 0.8 }
  if (paths.has('outbox.json') || paths.has('following_accounts.csv')) return { platform: 'mastodon_fediverse', parserVersion: 'mastodon_instance_export@1', certainty: 0.9 }
  if ([...paths].some((path) => path.startsWith('decoded/app.bsky.'))) return { platform: 'bluesky_atproto', parserVersion: 'bluesky_atproto_repo@1', certainty: 0.8 }
  return null
}

function parseFiles(files: ExtractedFile[], detection: Detection, importedAt: string): { records: Parsed[]; accepted: Set<string> } {
  const records: Parsed[] = []; const accepted = new Set<string>()
  for (const file of files) {
    const pointer = (index: number) => `${file.path}#/${index}`
    if (detection.platform === 'spotify' && /StreamingHistory[^/]*\.json$|endsong[^/]*\.json$/i.test(file.path)) {
      const rows = parseJson(file); if (!Array.isArray(rows)) throw new Error(`Expected JSON array in ${file.path}`)
      rows.forEach((raw, index) => { const row = raw as Record<string, unknown>; const artist = String(row.artistName ?? row.master_metadata_album_artist_name ?? '').trim(); const track = String(row.trackName ?? row.master_metadata_track_name ?? '').trim(); const occurredAt = iso(row.endTime ?? row.ts, importedAt); const durationMs = Number(row.msPlayed ?? row.ms_played ?? 0); const sourceRecordId = `spotify:history:sha256:${sha256(`${occurredAt}\0${artist}\0${track}\0${durationMs}`)}`; records.push({ sourceRecordId, category: 'watch_history', occurredAt, locale: null, content: `${artist} — ${track}`, metadata: { durationMs }, rawObjectRef: pointer(index) }) }); accepted.add(file.path)
    } else if (detection.platform === 'spotify' && /YourLibrary\.json$/i.test(file.path)) {
      const root = parseJson(file) as { tracks?: Array<Record<string, unknown>> }; (root.tracks ?? []).forEach((row, index) => { const artist = String(row.artist ?? ''); const track = String(row.track ?? ''); records.push({ sourceRecordId: String(row.uri ?? `spotify:library:${sha256(JSON.stringify(row))}`), category: 'likes', occurredAt: iso(undefined, importedAt), locale: null, content: `${artist} — ${track}`, metadata: {}, rawObjectRef: pointer(index) }) }); accepted.add(file.path)
    } else if (detection.platform === 'x_twitter' && file.path === 'data/tweets.js') {
      const rows = parseJson(file) as Array<{ tweet: Record<string, unknown> }>; rows.forEach(({ tweet }, index) => records.push({ sourceRecordId: String(tweet.id_str), category: 'posts', occurredAt: iso(tweet.created_at, importedAt), locale: typeof tweet.lang === 'string' ? tweet.lang : null, content: String(tweet.full_text ?? ''), metadata: {}, rawObjectRef: pointer(index) })); accepted.add(file.path)
    } else if (detection.platform === 'x_twitter' && file.path === 'data/like.js') {
      const rows = parseJson(file) as Array<{ like: Record<string, unknown> }>; rows.forEach(({ like }, index) => records.push({ sourceRecordId: `like:${String(like.tweetId)}`, category: 'likes', occurredAt: iso(like.created_at, importedAt), locale: null, content: String(like.fullText ?? ''), metadata: {}, rawObjectRef: pointer(index) })); accepted.add(file.path)
    } else if (detection.platform === 'x_twitter' && file.path === 'data/following.js') {
      const rows = parseJson(file) as Array<{ following: Record<string, unknown> }>; rows.forEach(({ following }, index) => records.push({ sourceRecordId: `follow:${String(following.accountId)}`, category: 'follows', occurredAt: iso(undefined, importedAt), locale: null, content: String(following.userLink ?? ''), metadata: {}, rawObjectRef: pointer(index) })); accepted.add(file.path)
    } else if (detection.platform === 'mastodon_fediverse' && file.path === 'outbox.json') {
      const root = parseJson(file) as { orderedItems?: Array<Record<string, unknown>> }; (root.orderedItems ?? []).forEach((item, index) => { const object = item.object as Record<string, unknown>; records.push({ sourceRecordId: String(item.id ?? object.id), category: 'posts', occurredAt: iso(item.published ?? object.published, importedAt), locale: null, content: cleanHtml(object.content), metadata: {}, rawObjectRef: pointer(index) }) }); accepted.add(file.path)
    } else if (detection.platform === 'mastodon_fediverse' && file.path === 'following_accounts.csv') {
      const [header, ...rows] = parseCsv(file.data.toString('utf8')); const account = header?.indexOf('Account address') ?? -1; if (account < 0) throw new Error('Mastodon following CSV is missing Account address'); rows.forEach((row, index) => records.push({ sourceRecordId: row[account], category: 'follows', occurredAt: iso(undefined, importedAt), locale: null, content: row[account], metadata: {}, rawObjectRef: pointer(index + 1) })); accepted.add(file.path)
    } else if (detection.platform === 'bluesky_atproto' && file.path.startsWith('decoded/app.bsky.')) {
      const row = parseJson(file) as Record<string, unknown>; const collection = String(row.$type); const key = file.path.split('/').at(-1)!.replace(/\.json$/, ''); const occurredAt = iso(row.createdAt, importedAt)
      if (collection === 'app.bsky.feed.post') records.push({ sourceRecordId: `at-record:${key}`, category: 'posts', occurredAt, locale: null, content: String(row.text ?? ''), metadata: {}, rawObjectRef: pointer(0) })
      else if (collection === 'app.bsky.feed.like') { const subject = row.subject as Record<string, unknown>; records.push({ sourceRecordId: `${String(subject.uri)}#${String(subject.cid)}`, category: 'likes', occurredAt, locale: null, content: String(subject.uri), metadata: {}, rawObjectRef: pointer(0) }) }
      else if (collection === 'app.bsky.graph.follow') records.push({ sourceRecordId: String(row.subject), category: 'follows', occurredAt, locale: null, content: String(row.subject), metadata: {}, rawObjectRef: pointer(0) })
      else continue
      accepted.add(file.path)
    }
  }
  return { records, accepted }
}

export async function ingestArchiveUpload(buffer: Buffer, options: ArchiveUploadOptions) {
  if (options.malwareScan === 'infected') throw new Error('Archive failed malware scan')
  if (options.malwareScan !== 'clean') throw new Error('Archive malware scan unavailable; fail closed')
  assertImportEntitlement({ ...options, compressedBytes: buffer.length })
  const archiveSha256 = sha256(buffer); const files = await extractZip(buffer); const detection = detect(files)
  if (!detection) throw new Error('Archive does not match a supported platform schema')
  const parsed = parseFiles(files, detection, options.importedAt)
  if (!parsed.records.length) throw new Error('Supported platform schema promoted no records')
  const seen = new Set<string>(); const records = parsed.records.map((row) => {
    if (!row.sourceRecordId.trim() || seen.has(row.sourceRecordId)) throw new Error(`Archive records require unique source IDs: ${row.sourceRecordId}`); seen.add(row.sourceRecordId)
    const id = `event:${options.tenantId}:${options.subjectId}:${options.sourceId}:${row.sourceRecordId}`
    const { rawObjectRef, ...normalized } = row
    return { ...normalized, id, kind: 'archive-import' as const, provenance: { archiveSha256, rawObjectRef, parserVersion: detection.parserVersion, consentReceiptId: options.consentReceiptId } }
  })
  const quarantinedFiles = files.map((file) => file.path).filter((path) => !parsed.accepted.has(path)).sort()
  const acceptedCategories = [...new Set(records.map((row) => row.category))].sort()
  const completeness = Number((parsed.accepted.size / files.length).toFixed(4)); const score = Number((detection.certainty * completeness).toFixed(2))
  const level = score >= 0.85 ? 'high' : score >= 0.6 ? 'medium' : 'low'
  return {
    manifest: { schemaVersion: 'archive-manifest@1', platform: detection.platform, parserVersion: detection.parserVersion, archiveSha256, consentReceiptId: options.consentReceiptId, acceptedCategories, quarantinedFiles, generatedAt: new Date(options.importedAt).toISOString() },
    records,
    coverage: { filesDiscovered: files.length, filesParsed: parsed.accepted.size, filesQuarantined: quarantinedFiles.length, acceptedRecords: records.length, categories: Object.fromEntries(acceptedCategories.map((category) => [category, records.filter((row) => row.category === category).length])), formulaVersion: 'archive-coverage@1', formula: 'file_completeness = parsed_files / discovered_files; confidence_score = schema_certainty × file_completeness', confidence: { score, level, reasons: [`schema certainty ${detection.certainty}`, `${parsed.accepted.size}/${files.length} files parsed`, `${records.length} records normalized`] } },
    sandbox: { network: 'denied', filesystem: 'memory-only', privilege: 'unprivileged', executeContent: false },
    quotaCharge: { successfulImport: true, chargedAfterPromotion: true },
  }
}
