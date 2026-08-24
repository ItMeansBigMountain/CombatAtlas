import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import ts from 'typescript'

async function importTs(url) {
  const source = await readFile(url, 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.ES2022, target: ts.ScriptTarget.ES2022, verbatimModuleSyntax: true },
  })
  return import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`)
}

const {
  approveArtifactIntoJournal,
  createJournalEntry,
  deleteJournalEntry,
  exportJournal,
  journalDeepLink,
  purgeDeletedEntries,
  queueOfflineMutation,
} = await importTs(new URL('../src/journalDomain.ts', import.meta.url))

const created = createJournalEntry({
  id: 'journal-1',
  body: '  I need to protect focus time.  ',
  mood: 'steady',
  createdAt: '2026-08-24T01:00:00Z',
})
assert.equal(created.body, 'I need to protect focus time.')
assert.equal(created.private, true)
assert.equal(created.deletedAt, null)
assert.throws(() => createJournalEntry({ id: 'empty', body: ' ', mood: 'low', createdAt: 'now' }), /empty/i)

const linked = approveArtifactIntoJournal(created, {
  id: 'meeting-1-summary-s1',
  meetingId: 'meeting-1',
  kind: 'summary',
  text: 'We agreed to reserve Friday for deep work.',
  citations: ['s1'],
  status: 'approved',
  private: false,
})
assert.deepEqual(linked.sourceMeetingIds, ['meeting-1'])
assert.match(linked.body, /reserve Friday/)
assert.equal(journalDeepLink(linked.id), 'journalai://journal/journal-1')

const queued = queueOfflineMutation([], { id: 'mutation-1', kind: 'upsert', entryId: linked.id, queuedAt: 'now' })
assert.equal(queued.length, 1)
assert.equal(queueOfflineMutation(queued, queued[0]).length, 1)
assert.match(exportJournal([linked], 'markdown'), /# Private journal export/)
assert.match(exportJournal([linked], 'json'), /"journal-1"/)

const deleted = deleteJournalEntry(linked, '2026-08-24T02:00:00Z')
assert.equal(deleted.body, '')
assert.equal(deleted.deletedAt, '2026-08-24T02:00:00Z')
assert.throws(() => approveArtifactIntoJournal(deleted, {
  id: 'x', meetingId: 'm2', kind: 'summary', text: 'x', citations: ['s2'], status: 'approved', private: false,
}), /deleted/i)

const purge = purgeDeletedEntries([deleted], '2026-08-24T02:01:00Z')
assert.deepEqual(purge.entries, [])
assert.deepEqual(purge.receipt, { purgedEntryIds: ['journal-1'], purgedAt: '2026-08-24T02:01:00Z' })
