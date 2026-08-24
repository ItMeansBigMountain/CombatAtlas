import test from 'node:test'
import assert from 'node:assert/strict'

import {
  estimateMonthlyCost,
  evaluateDeploymentReadiness,
  selectClosedBetaParticipants,
  type DeploymentEvidence,
  type OperationalControlEvidence,
  type ReleaseTarget,
} from '../src/index.js'

const targets: ReleaseTarget[] = ['web', 'ios', 'android']
const completeEvidence: DeploymentEvidence[] = targets.map((target) => ({
  target,
  build: 'verified',
  smokeTest: 'verified',
  distribution: 'verified',
  monitoring: 'verified',
  rollback: 'verified',
  notes: `${target} synthetic fixture smoke passed`,
}))

const completeOperations: OperationalControlEvidence = {
  observability: 'verified',
  backupsRestore: 'verified',
  incidentResponse: 'verified',
  costControls: 'verified',
  privacyRequests: 'verified',
  closedBetaConsent: 'verified',
}

test('deployment readiness blocks unverified platform or operations evidence', () => {
  const decision = evaluateDeploymentReadiness({
    evidence: [completeEvidence[0]],
    operations: { ...completeOperations, backupsRestore: 'blocked' },
    diagnosticsClaimsPresent: false,
    fakePlatformCoverageClaimsPresent: false,
  })

  assert.equal(decision.decision, 'BLOCK')
  assert.equal(decision.failures.some((failure) => failure.includes('ios deployment evidence')), true)
  assert.equal(decision.failures.some((failure) => failure.includes('backup restore drill')), true)
})

test('deployment readiness rejects diagnosis and fake coverage claims even with passing evidence', () => {
  const decision = evaluateDeploymentReadiness({
    evidence: completeEvidence,
    operations: completeOperations,
    diagnosticsClaimsPresent: true,
    fakePlatformCoverageClaimsPresent: true,
  })

  assert.equal(decision.decision, 'BLOCK')
  assert.equal(decision.failures.some((failure) => failure.includes('Diagnostic')), true)
  assert.equal(decision.failures.some((failure) => failure.includes('Platform coverage')), true)
})

test('deployment readiness can pass only when every platform and operation is verified', () => {
  assert.equal(evaluateDeploymentReadiness({
    evidence: completeEvidence,
    operations: completeOperations,
    diagnosticsClaimsPresent: false,
    fakePlatformCoverageClaimsPresent: false,
  }).decision, 'GO')
})

test('closed beta accepts only consented synthetic-or-consented fixtures in supported jurisdictions', () => {
  const decision = selectClosedBetaParticipants([
    { id: 'tester-a', consented: true, syntheticOrConsentedFixture: true, ageGatePassed: true, jurisdictionSupported: true, safetyCopyAccepted: true },
    { id: 'tester-b', consented: false, syntheticOrConsentedFixture: false, ageGatePassed: true, jurisdictionSupported: true, safetyCopyAccepted: true },
  ])

  assert.deepEqual(decision.acceptedIds, ['tester-a'])
  assert.equal(decision.rejected[0].id, 'tester-b')
  assert.equal(decision.rejected[0].reasons.some((reason) => reason.includes('consent')), true)
})

test('cost estimates fail closed on invalid input and surface budget overrun', () => {
  const estimate = estimateMonthlyCost({
    users: 25,
    archiveImports: 10,
    oauthSyncs: 200,
    modelRuns: 100,
    storageGb: 20,
    unitCosts: { user: 0.1, archiveImport: 0.75, oauthSync: 0.01, modelRun: 0.05, storageGb: 0.15 },
    monthlyBudget: 15,
  })
  assert.equal(estimate.withinBudget, false)
  assert.equal(estimate.overBy > 0, true)
  assert.throws(() => estimateMonthlyCost({ users: -1, archiveImports: 0, oauthSyncs: 0, modelRuns: 0, storageGb: 0, unitCosts: { user: 0, archiveImport: 0, oauthSync: 0, modelRun: 0, storageGb: 0 }, monthlyBudget: 0 }), /non-negative/)
})
