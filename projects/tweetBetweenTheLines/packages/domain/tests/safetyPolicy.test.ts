import test from 'node:test'
import assert from 'node:assert/strict'

import {
  assessInsightRelease,
  buildDeletionPlan,
  buildModelProvenance,
  createConsentReceipt,
  createProcessingEnvelope,
  evaluateCohortReadiness,
  type CohortEvaluation,
} from '../src/index.js'

test('consent receipts are per tenant and source, versioned, purpose-limited, and revocable', () => {
  const receipt = createConsentReceipt({
    tenantId: 'tenant-a',
    subjectId: 'user-1',
    sourceId: 'x-archive',
    purposes: ['profile-reflection'],
    dataCategories: ['posts'],
    grantedAt: '2026-08-24T00:00:00.000Z',
    policyVersion: 'privacy-3',
  })

  assert.match(receipt.id, /^consent:/)
  assert.equal(receipt.tenantId, 'tenant-a')
  assert.equal(receipt.sourceId, 'x-archive')
  assert.equal(receipt.status, 'active')
  assert.deepEqual(receipt.purposes, ['profile-reflection'])
})

test('processing envelope separates tokens, raw records, features, and model-safe payloads', () => {
  const envelope = createProcessingEnvelope({
    tenantId: 'tenant-a',
    subjectId: 'user-1',
    sourceId: 'youtube',
    tokenRef: 'vault://tenant-a/user-1/youtube',
    rawObjectRef: 'raw://tenant-a/user-1/youtube/export-1',
    featureSetRef: 'features://tenant-a/user-1/set-1',
    aggregateEvidence: { topicCounts: { music: 4 } },
  })

  assert.equal(envelope.modelPayload.tenantId, 'tenant-a')
  assert.equal(JSON.stringify(envelope.modelPayload).includes('vault://'), false)
  assert.equal(JSON.stringify(envelope.modelPayload).includes('raw://'), false)
  assert.equal(envelope.secrets.tokenRef.startsWith('vault://'), true)
})

test('deletion plans preserve auditable tombstones while deleting source descendants', () => {
  const plan = buildDeletionPlan({
    tenantId: 'tenant-a',
    subjectId: 'user-1',
    sourceId: 'x-archive',
    consentReceiptIds: ['consent:1'],
    rawObjectRefs: ['raw:1'],
    normalizedEventIds: ['event:1'],
    featureSetIds: ['features:1'],
    insightIds: ['insight:1'],
  })

  assert.deepEqual(plan.deleteOrder.map((step) => step.layer), [
    'insight', 'feature', 'normalized', 'raw', 'token', 'consent',
  ])
  assert.equal(plan.auditTombstone.containsPersonalData, false)
})

test('health-related releases enforce non-diagnostic boundaries and review gates', () => {
  assert.deepEqual(assessInsightRelease({
    category: 'observational-wellbeing',
    text: 'Your posts show that you are clinically depressed.',
    professionalReview: false,
    crisisFlowConfigured: true,
    instrument: null,
  }).allowed, false)

  const screener = assessInsightRelease({
    category: 'self-report-screener',
    text: 'Your self-reported answers suggest follow-up may be useful; this is not a diagnosis.',
    professionalReview: true,
    crisisFlowConfigured: true,
    instrument: { name: 'PHQ-9', license: 'open', validatedLocales: ['en'], locale: 'en' },
  })
  assert.equal(screener.allowed, true)
})

test('model provenance is complete and cohorts must pass multilingual disparity gates', () => {
  const provenance = buildModelProvenance({
    provider: 'internal',
    model: 'transparent-lexicon',
    version: '1.0.0',
    promptVersion: 'none',
    featureSchemaVersion: '1',
    inputDigest: `sha256:${'a'.repeat(64)}`,
    generatedAt: '2026-08-24T00:00:00.000Z',
  })
  assert.equal(provenance.reviewStatus, 'unreviewed')

  const cohorts: CohortEvaluation[] = [
    { locale: 'en', sampleSize: 100, falsePositiveRate: 0.04, falseNegativeRate: 0.05, calibrationError: 0.03 },
    { locale: 'es', sampleSize: 100, falsePositiveRate: 0.15, falseNegativeRate: 0.06, calibrationError: 0.04 },
  ]
  const evaluation = evaluateCohortReadiness(cohorts, {
    minimumSampleSize: 50,
    maximumErrorRate: 0.1,
    maximumCalibrationError: 0.05,
    maximumInterCohortDisparity: 0.05,
  })
  assert.equal(evaluation.ready, false)
  assert.equal(evaluation.failures.some((failure) => failure.includes('es')), true)
})
