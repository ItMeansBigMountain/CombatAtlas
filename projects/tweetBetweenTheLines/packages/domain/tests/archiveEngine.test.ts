import assert from 'node:assert/strict'
import test from 'node:test'
import { Buffer } from 'node:buffer'
import { ZipFile } from 'yazl'

import {
  ENTITLEMENTS,
  assertImportEntitlement,
  ingestArchiveUpload,
  type ArchiveUploadOptions,
} from '../src/archiveEngine.js'

const defaults: ArchiveUploadOptions = {
  tenantId: 'tenant-a',
  subjectId: 'person-a',
  sourceId: 'spotify:account-a',
  consentReceiptId: 'consent:archive:1',
  malwareScan: 'clean',
  plan: 'free',
  successfulImportsInRolling30Days: 0,
  activeAccounts: 1,
  importedAt: '2026-08-25T00:00:00.000Z',
}

async function zip(entries: Record<string, string>): Promise<Buffer> {
  const file = new ZipFile()
  for (const [path, content] of Object.entries(entries)) file.addBuffer(Buffer.from(content), path)
  file.end()
  const chunks: Buffer[] = []
  for await (const chunk of file.outputStream) chunks.push(Buffer.from(chunk))
  return Buffer.concat(chunks)
}

test('admits a clean ZIP and deterministically parses Spotify JSON with provenance', async () => {
  const upload = await zip({
    'StreamingHistory_music_0.json': JSON.stringify([{ endTime: '2026-08-25 00:03', artistName: 'Synthetic Artist', trackName: 'Parser Song', msPlayed: 180000 }]),
    'YourLibrary.json': JSON.stringify({ tracks: [{ artist: 'Synthetic Artist', track: 'Saved Track', uri: 'spotify:track:synthetic1' }] }),
  })
  const result = await ingestArchiveUpload(upload, defaults)
  assert.equal(result.manifest.platform, 'spotify')
  assert.equal(result.manifest.parserVersion, 'spotify_archive@1')
  assert.deepEqual(result.manifest.acceptedCategories, ['likes', 'watch_history'])
  assert.equal(result.records.length, 2)
  assert.equal(result.records[0].provenance.archiveSha256, result.manifest.archiveSha256)
  assert.equal(result.coverage.acceptedRecords, 2)
  assert.equal(result.coverage.confidence.level, 'high')
  assert.equal(result.coverage.formulaVersion, 'archive-coverage@1')
})

test('parses X JavaScript wrappers and quarantines unrecognized files without executing content', async () => {
  const upload = await zip({
    'data/tweets.js': 'window.YTD.tweets.part0 = [{"tweet":{"id_str":"1","created_at":"Tue Aug 25 00:00:00 +0000 2026","full_text":"Synthetic post","lang":"en"}}]',
    'data/like.js': 'window.YTD.like.part0 = [{"like":{"tweetId":"2","fullText":"Synthetic liked post"}}]',
    'unknown/run.js': 'throw new Error("must never execute")',
  })
  const result = await ingestArchiveUpload(upload, { ...defaults, sourceId: 'x:account-a' })
  assert.equal(result.manifest.platform, 'x_twitter')
  assert.deepEqual(result.records.map((row) => row.category), ['posts', 'likes'])
  assert.deepEqual(result.manifest.quarantinedFiles, ['unknown/run.js'])
  assert.equal(result.coverage.filesQuarantined, 1)
})

test('parses Mastodon JSON and RFC4180 CSV fields deterministically', async () => {
  const upload = await zip({
    'outbox.json': JSON.stringify({ orderedItems: [{ id: 'https://example.test/status/1', published: '2026-08-25T00:00:00Z', object: { type: 'Note', content: '<p>Hello &amp; welcome.</p>' } }] }),
    'following_accounts.csv': 'Account address,Show boosts\r\n"person@example.test",true\r\n',
  })
  const result = await ingestArchiveUpload(upload, { ...defaults, sourceId: 'mastodon:account-a' })
  assert.equal(result.manifest.platform, 'mastodon_fediverse')
  assert.deepEqual(result.records.map((row) => row.content), ['Hello & welcome.', 'person@example.test'])
})

test('fails closed for unavailable malware scan, malformed ZIP, bombs and unsupported schemas', async () => {
  const valid = await zip({ 'unknown.json': '{}' })
  await assert.rejects(() => ingestArchiveUpload(valid, { ...defaults, malwareScan: 'unavailable' }), /malware scan unavailable/i)
  await assert.rejects(() => ingestArchiveUpload(Buffer.from('not a zip'), defaults), /ZIP/i)
  await assert.rejects(() => ingestArchiveUpload(valid, defaults), /supported platform schema/i)

  const compressible = await zip({ 'StreamingHistory_music_0.json': JSON.stringify([{ endTime: '2026-08-25 00:03', artistName: 'A', trackName: 'B', msPlayed: 1, padding: 'x'.repeat(200_000) }]) })
  await assert.rejects(() => ingestArchiveUpload(compressible, defaults), /expansion ratio/i)
})

test('enforces canonical free and premium import entitlements before parsing', () => {
  assert.equal(ENTITLEMENTS.free.maxCompressedImportBytes, 262_144_000)
  assert.equal(ENTITLEMENTS.premium.maxCompressedImportBytes, 2_147_483_648)
  assert.throws(() => assertImportEntitlement({ plan: 'free', compressedBytes: 1, successfulImportsInRolling30Days: 2, activeAccounts: 1 }), /rolling 30-day import limit/i)
  assert.throws(() => assertImportEntitlement({ plan: 'free', compressedBytes: 1, successfulImportsInRolling30Days: 0, activeAccounts: 2 }), /active account limit/i)
  assert.doesNotThrow(() => assertImportEntitlement({ plan: 'premium_ai', compressedBytes: 1_000_000_000, successfulImportsInRolling30Days: 19, activeAccounts: 10 }))
})
