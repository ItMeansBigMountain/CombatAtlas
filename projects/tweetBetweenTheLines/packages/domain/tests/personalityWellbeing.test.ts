import test from 'node:test'
import assert from 'node:assert/strict'

import {
  buildObservationalWellbeingReflection,
  scorePersonalitySelfReport,
  type OpenTraitInstrument,
} from '../src/index.js'

const openInstrument: OpenTraitInstrument = {
  id: 'ipip-demo-10',
  name: 'Open trait reflection demo',
  sourceUrl: 'https://ipip.ori.org/',
  license: { kind: 'open', notice: 'Public-domain IPIP items; verify exact set before release.' },
  version: 'review-candidate-1',
  validatedLocales: ['en'],
  responseScale: { minimum: 1, maximum: 5 },
  traits: [
    { id: 'curiosity', label: 'Curiosity' },
    { id: 'sociability', label: 'Sociability' },
  ],
  items: [
    { id: 'q1', traitId: 'curiosity', prompt: 'I am interested in abstract ideas.', keyed: 'forward' },
    { id: 'q2', traitId: 'curiosity', prompt: 'I avoid philosophical discussions.', keyed: 'reverse' },
    { id: 'q3', traitId: 'sociability', prompt: 'I start conversations.', keyed: 'forward' },
    { id: 'q4', traitId: 'sociability', prompt: 'I keep in the background.', keyed: 'reverse' },
  ],
  governance: { legalReviewed: true, clinicalReviewed: true, reviewedAt: '2026-08-24T00:00:00.000Z' },
}

test('self-report scoring is instrument-bound, reverse-keyed, and never mixed with observed signals', () => {
  const result = scorePersonalitySelfReport(openInstrument, {
    locale: 'en',
    consented: true,
    answers: { q1: 5, q2: 1, q3: 2, q4: 4 },
  })

  assert.equal(result.allowed, true)
  assert.equal(result.signalSource, 'self-report-questionnaire')
  assert.deepEqual(result.scores, [
    { traitId: 'curiosity', label: 'Curiosity', answeredItems: 2, possibleItems: 2, normalizedScore: 1 },
    { traitId: 'sociability', label: 'Sociability', answeredItems: 2, possibleItems: 2, normalizedScore: 0.25 },
  ])
  assert.match(result.disclosure, /not a diagnosis/i)
  assert.equal(JSON.stringify(result).includes('observedScore'), false)
})

test('self-report fails closed for missing consent, incomplete answers, unvalidated locale, licensing, or review', () => {
  const restricted = structuredClone(openInstrument)
  restricted.license.kind = 'restricted'
  restricted.governance.legalReviewed = false

  const blocked = scorePersonalitySelfReport(restricted, {
    locale: 'es',
    consented: false,
    answers: { q1: 6, q2: 1 },
  })

  assert.equal(blocked.allowed, false)
  assert.equal(blocked.scores.length, 0)
  assert.deepEqual(blocked.failures, [
    'Separate self-report consent is required.',
    'Instrument licensing is not approved for release.',
    'Instrument is not validated for locale es.',
    'Clinical and legal review are required before public release.',
    'Every instrument item requires an in-range response.',
  ])
})

test('observational wellbeing reports only slice-level language counts with uncertainty and evidence', () => {
  const reflection = buildObservationalWellbeingReflection({
    locale: 'en-US',
    generatedAt: '2026-08-24T01:00:00.000Z',
    events: [
      { id: 'a', sourceId: 'x', sourceRecordId: '1', occurredAt: '2026-08-20T00:00:00.000Z', text: 'Deadlines left me tired and stressed.' },
      { id: 'b', sourceId: 'x', sourceRecordId: '2', occurredAt: '2026-08-21T00:00:00.000Z', text: 'I feel grateful and calm today.' },
    ],
  })

  assert.equal(reflection.signalSource, 'observational-language')
  assert.equal(reflection.counts.eventsAnalyzed, 2)
  assert.equal(reflection.counts.eventsWithStrainTerms, 1)
  assert.equal(reflection.counts.eventsWithSupportiveTerms, 1)
  assert.equal(reflection.evidence[0].sourceRecordId, '1')
  assert.match(reflection.summary, /selected slice/i)
  assert.match(reflection.disclosure, /cannot diagnose/i)
  assert.match(reflection.disclosure, /absence/i)
  assert.equal(JSON.stringify(reflection).includes('depressionScore'), false)
})

test('wellbeing reflection abstains on unsupported locale and supplies help guidance without claiming crisis detection', () => {
  const reflection = buildObservationalWellbeingReflection({
    locale: 'ar',
    generatedAt: '2026-08-24T01:00:00.000Z',
    events: [{ id: 'a', sourceId: 'x', sourceRecordId: '1', occurredAt: '2026-08-20T00:00:00.000Z', text: 'متعب' }],
  })

  assert.equal(reflection.status, 'abstained')
  assert.match(reflection.summary, /not validated/i)
  assert.match(reflection.helpGuidance, /qualified professional/i)
  assert.match(reflection.helpGuidance, /local emergency services/i)
  assert.match(reflection.helpGuidance, /does not monitor/i)
})
