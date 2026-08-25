import test from 'node:test'
import assert from 'node:assert/strict'

import { buildExplainableMetrics, type MetricEvent } from '../src/index.js'

const events: MetricEvent[] = [
  { id: 'x:1', sourceId: 'x', sourceRecordId: '1', occurredAt: '2026-01-01T08:00:00Z', kind: 'post', locale: 'en', content: 'I love music and coding with my community', metadata: { community: 'builders' } },
  { id: 'youtube:2', sourceId: 'youtube', sourceRecordId: '2', occurredAt: '2026-02-01T22:00:00Z', kind: 'view', locale: 'es', content: 'música genial y tecnología', metadata: { creator: 'Creator A', mediaTitle: 'Mix A' } },
  { id: 'spotify:3', sourceId: 'spotify', sourceRecordId: '3', occurredAt: '2026-03-01T23:00:00Z', kind: 'listen', locale: 'fr', content: 'musique calme et heureuse', metadata: { artist: 'Artist B' } },
  { id: 'x:4', sourceId: 'x', sourceRecordId: '4', occurredAt: '2026-04-01T09:00:00Z', kind: 'post', locale: 'en', content: 'Feeling tired after a bad workout', metadata: { community: 'fitness' } },
]

test('builds every explainable deterministic metric lane before narrative', () => {
  const snapshot = buildExplainableMetrics(events, '2026-05-01T00:00:00Z')
  assert.equal(snapshot.eventCount, 4)
  assert.deepEqual(snapshot.cards.map((card) => card.category), [
    'interests', 'topics', 'communities', 'language-style', 'sentiment', 'attention-rhythm', 'media-affinity', 'stated-vs-observed', 'change-over-time',
  ])
  for (const card of snapshot.cards) {
    assert.equal(card.sourceCoverage.length, 3)
    assert.equal(Object.keys(card.aggregates).length > 0, true)
    assert.equal(card.confidence.reasons.length, 3)
    assert.equal(card.limitations.length >= 3, true)
    assert.equal(card.analyzer.method, 'deterministic')
    assert.match(card.formula.expression, /\S/)
    assert.match(card.formula.version, /^metric-formula@1:/)
    assert.equal(card.evidence.length > 0, true)
  }
  assert.equal(snapshot.narrativeGate.allowed, true)
})

test('keeps multilingual sentiment distributions and source-backed drill-down', () => {
  const snapshot = buildExplainableMetrics(events)
  const sentiment = snapshot.cards.find((card) => card.category === 'sentiment')!
  assert.deepEqual(sentiment.aggregates, { positive: 3, negative: 1, neutral: 0, supportedLocales: ['de', 'en', 'es', 'fr', 'pt'] })
  assert.deepEqual(sentiment.evidence.map((item) => item.eventId), ['x:1', 'youtube:2', 'spotify:3', 'x:4'])
  assert.equal(sentiment.sourceCoverage.find((item) => item.sourceId === 'x')?.events, 2)
})

test('separates stated expression from observed attention and reports time windows', () => {
  const snapshot = buildExplainableMetrics(events)
  const alignment = snapshot.cards.find((card) => card.category === 'stated-vs-observed')!
  assert.deepEqual(alignment.aggregates.alignment, [
    { label: 'fitness', stated: true, observed: false },
    { label: 'music', stated: true, observed: true },
    { label: 'technology', stated: true, observed: true },
  ])
  const change = snapshot.cards.find((card) => card.category === 'change-over-time')!
  assert.equal(typeof change.aggregates.midpoint, 'string')
  assert.match(change.limitations.at(-1)!, /not a causal trend/i)
})

test('blocks narrative when sparse or unsupported cards lack evidence', () => {
  const snapshot = buildExplainableMetrics([{ ...events[0], content: 'hello' }])
  assert.equal(snapshot.narrativeGate.allowed, false)
  assert.equal(snapshot.cards.every((card) => card.sourceCoverage.length === 1), true)
  assert.equal(snapshot.cards.some((card) => card.confidence.level === 'insufficient'), true)
})

test('rejects duplicate identifiers and invalid provenance', () => {
  assert.throws(() => buildExplainableMetrics([events[0], events[0]]), /Duplicate event id/)
  assert.throws(() => buildExplainableMetrics([{ ...events[0], sourceId: ' ' }]), /provenance/)
})
