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

const { confidenceLabel, createMeetingJob, editSegment, provisionalSpeaker, retryJob, transitionJob } =
  await importTs(new URL('../src/meetingWorkflow.ts', import.meta.url))

assert.throws(() => createMeetingJob({ id: '1', fileName: 'private.webm', retention: 'delete-after-transcription' }), /consent/i)
let job = createMeetingJob({ id: '1', fileName: 'private.webm', retention: 'delete-after-transcription', consentedAt: '2026-08-24T00:00:00Z' })
assert.equal(job.state, 'queued')
assert.equal(job.encrypted, true)
job = transitionJob(job, 'normalizing')
job = transitionJob(job, 'transcribing')
job = transitionJob(job, 'diarizing')
job = transitionJob(job, 'needs_review')
assert.equal(job.progress, 90)
assert.throws(() => transitionJob(job, 'queued'), /Invalid meeting job transition/)

const edited = editSegment({ id: 's1', startSeconds: 0, endSeconds: 1, text: 'helo', speakerLabel: provisionalSpeaker(0), confidence: 0.4, userEdited: false }, { text: 'hello', speakerLabel: 'Alex' })
assert.equal(edited.text, 'hello')
assert.equal(edited.speakerLabel, 'Alex')
assert.equal(edited.userEdited, true)
assert.match(confidenceLabel(0.4), /Low confidence/)
assert.equal(provisionalSpeaker(1), 'Speaker 2')

const cancelled = transitionJob(createMeetingJob({ id: '2', fileName: 'x.wav', retention: 'keep-24-hours', consentedAt: 'now' }), 'cancelled')
assert.equal(retryJob(cancelled).attempts, 2)
