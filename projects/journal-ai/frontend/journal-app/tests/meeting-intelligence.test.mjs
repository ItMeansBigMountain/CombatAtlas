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
  approveArtifact,
  buildDraftArtifacts,
  createArtifactStore,
  deleteArtifact,
  exportArtifact,
  recurringThemes,
} = await importTs(new URL('../src/meetingIntelligence.ts', import.meta.url))

const segments = [
  { id: 's1', startSeconds: 0, endSeconds: 4, text: 'We decided to ship the beta Friday.', speakerLabel: 'Alex', confidence: 0.9, userEdited: true },
  { id: 's2', startSeconds: 4, endSeconds: 8, text: 'Sam will send the launch checklist by Thursday.', speakerLabel: 'Sam', confidence: 0.88, userEdited: true },
  { id: 's3', startSeconds: 8, endSeconds: 12, text: 'Question: do we need legal review?', speakerLabel: 'Alex', confidence: 0.82, userEdited: true },
]

const drafts = buildDraftArtifacts('meeting-1', segments)
assert.ok(drafts.some((artifact) => artifact.kind === 'summary'))
assert.ok(drafts.some((artifact) => artifact.kind === 'decision'))
assert.ok(drafts.some((artifact) => artifact.kind === 'commitment'))
assert.ok(drafts.some((artifact) => artifact.kind === 'question'))
assert.ok(drafts.every((artifact) => artifact.status === 'draft' && artifact.citations.length > 0))
assert.ok(drafts.every((artifact) => artifact.citations.every((id) => segments.some((segment) => segment.id === id))))

const commitment = drafts.find((artifact) => artifact.kind === 'commitment')
assert.equal(commitment.owner, 'Sam')
assert.equal(commitment.dueText, 'Thursday')

let store = createArtifactStore(drafts)
const summary = drafts.find((artifact) => artifact.kind === 'summary')
store = approveArtifact(store, summary.id)
assert.equal(store.artifacts.find((artifact) => artifact.id === summary.id).status, 'approved')
const exported = JSON.parse(exportArtifact(store, summary.id, 'json'))
assert.equal(exported.id, summary.id)
assert.equal(exported.status, 'approved')
store = deleteArtifact(store, summary.id)
assert.equal(store.artifacts.some((artifact) => artifact.id === summary.id), false)
assert.throws(() => exportArtifact(store, summary.id, 'json'), /not found/i)

const themes = recurringThemes([
  { label: 'launch planning', meetingId: 'm1' },
  { label: 'Launch Planning', meetingId: 'm2' },
  { label: 'stress disorder', meetingId: 'm3' },
])
assert.deepEqual(themes, [{ label: 'launch planning', count: 2, meetingIds: ['m1', 'm2'] }])
assert.throws(() => approveArtifact(createArtifactStore(drafts), 'missing'), /not found/i)

const mainSource = await readFile(new URL('../src/main.ts', import.meta.url), 'utf8')
assert.match(mainSource, /Review meeting intelligence/)
assert.match(mainSource, /Add private reflection/)
assert.match(mainSource, /Export JSON/)
assert.match(mainSource, /Delete artifact/)
assert.match(mainSource, /not a diagnosis/i)
