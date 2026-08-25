import test from 'node:test'
import assert from 'node:assert/strict'

import { buildPrivateReflection, type PrivateReflectionInput } from '../src/index.js'

const input: PrivateReflectionInput = {
  id: 'reflection-1',
  title: 'A chapter I named',
  purpose: 'breakup-recovery',
  visibility: 'private',
  consented: true,
  startAt: '2026-01-01T00:00:00Z',
  endAt: '2026-02-01T00:00:00Z',
  selectedEventIds: ['post-1', 'post-2', 'post-3'],
  notes: [
    { id: 'note-1', occurredAt: '2026-01-05T00:00:00Z', text: 'I want to remember that I asked for support.' },
  ],
  events: [
    { id: 'post-1', sourceId: 'x-archive', sourceRecordId: '1', occurredAt: '2026-01-04T00:00:00Z', text: 'I felt sad and overwhelmed.' },
    { id: 'post-2', sourceId: 'x-archive', sourceRecordId: '2', occurredAt: '2026-01-20T00:00:00Z', text: 'I feel hopeful and supported.' },
    { id: 'post-3', sourceId: 'x-archive', sourceRecordId: '3', occurredAt: '2025-12-20T00:00:00Z', text: 'Outside the period and must be excluded.' },
    { id: 'post-4', sourceId: 'x-archive', sourceRecordId: '4', occurredAt: '2026-01-22T00:00:00Z', text: 'Not selected and must be excluded.' },
  ],
}

test('private reflection is user-initiated, private, and limited to selected in-window evidence', () => {
  const result = buildPrivateReflection(input)

  assert.equal(result.status, 'ready')
  assert.equal(result.visibility, 'private')
  assert.deepEqual(result.evidence.map((row) => row.eventId), ['post-1', 'post-2'])
  assert.equal(result.notes.length, 1)
  assert.match(result.boundary, /not mental-health assessment/i)
  assert.match(result.boundary, /relationship judgment/i)
  assert.equal(JSON.stringify(result).includes('post-3'), false)
  assert.equal(JSON.stringify(result).includes('post-4'), false)
})

test('private reflection reports descriptive change without diagnosing recovery', () => {
  const result = buildPrivateReflection(input)

  assert.deepEqual(result.progress, {
    earlier: { events: 1, strainLanguageEvents: 1, supportiveLanguageEvents: 0 },
    later: { events: 1, strainLanguageEvents: 0, supportiveLanguageEvents: 1 },
  })
  assert.match(result.summary, /selected events/i)
  assert.doesNotMatch(result.summary, /you (recovered|healed|are depressed)/i)
  assert.match(result.limitations.join(' '), /not prove/i)
})

test('reflection fails closed without consent or private visibility', () => {
  const noConsent = buildPrivateReflection({ ...input, consented: false })
  const publicAttempt = buildPrivateReflection({ ...input, visibility: 'shared' })

  assert.equal(noConsent.status, 'blocked')
  assert.match(noConsent.failures.join(' '), /consent/i)
  assert.equal(publicAttempt.status, 'blocked')
  assert.match(publicAttempt.failures.join(' '), /private/i)
  assert.deepEqual(publicAttempt.evidence, [])
})
