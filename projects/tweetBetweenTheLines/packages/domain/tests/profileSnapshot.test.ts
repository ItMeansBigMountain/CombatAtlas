import test from 'node:test'
import assert from 'node:assert/strict'

import {
  buildProfileSnapshot,
  normalizePersonalEvent,
  type PersonalEventInput,
} from '../src/index.js'

const baseEvent = {
  occurredAt: '2026-08-24T01:00:00.000Z',
  source: 'x-archive',
  sourceRecordId: 'tweet-1',
  kind: 'post',
  text: 'I am grateful for family but overwhelmed by work deadlines.',
} satisfies PersonalEventInput

test('normalizes personal events with source provenance and deterministic text features', () => {
  const event = normalizePersonalEvent(baseEvent)

  assert.equal(event.id, 'x-archive:tweet-1')
  assert.equal(event.provenance.source, 'x-archive')
  assert.equal(event.provenance.sourceRecordId, 'tweet-1')
  assert.deepEqual(event.features.keywords.slice(0, 4), ['grateful', 'family', 'overwhelmed', 'work'])
  assert.equal(event.features.wordCount, 9)
})

test('builds non-diagnostic profile snapshots with evidence-backed cards', () => {
  const snapshot = buildProfileSnapshot([
    baseEvent,
    {
      ...baseEvent,
      sourceRecordId: 'tweet-2',
      occurredAt: '2026-08-25T01:00:00.000Z',
      text: 'Music and friends helped me feel clear and hopeful after school.',
    },
  ])

  assert.equal(snapshot.mission, 'Free the minds of the consumer with data')
  assert.equal(snapshot.cards[0].kind, 'attention')
  assert.equal(snapshot.cards[0].evidence.length > 0, true)
  assert.equal(snapshot.cards.some((card) => card.kind === 'wellbeing-pattern'), true)
  assert.match(snapshot.safetyBoundary, /not a diagnosis/i)
  assert.equal(snapshot.cards.some((card) => /depressed|diagnosed/i.test(card.title + card.summary)), false)
})

test('revocation removes source events and preserves deletion lineage', () => {
  const snapshot = buildProfileSnapshot([
    baseEvent,
    {
      ...baseEvent,
      source: 'youtube',
      sourceRecordId: 'video-1',
      text: 'Watched music production and fitness creators all night.',
    },
  ], { revokedSources: ['x-archive'] })

  assert.deepEqual(snapshot.revokedSources, ['x-archive'])
  assert.equal(snapshot.eventsAnalyzed, 1)
  assert.equal(snapshot.cards.every((card) => card.evidence.every((item) => item.source !== 'x-archive')), true)
})
