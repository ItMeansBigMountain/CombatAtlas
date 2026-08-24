export type ReleaseTarget = 'web' | 'ios' | 'android'
export type EvidenceStatus = 'verified' | 'blocked' | 'not-started'

export type DeploymentEvidence = {
  target: ReleaseTarget
  build: EvidenceStatus
  smokeTest: EvidenceStatus
  distribution: EvidenceStatus
  monitoring: EvidenceStatus
  rollback: EvidenceStatus
  notes: string
}

export type OperationalControlEvidence = {
  observability: EvidenceStatus
  backupsRestore: EvidenceStatus
  incidentResponse: EvidenceStatus
  costControls: EvidenceStatus
  privacyRequests: EvidenceStatus
  closedBetaConsent: EvidenceStatus
}

export type ClosedBetaCandidate = {
  id: string
  consented: boolean
  syntheticOrConsentedFixture: boolean
  ageGatePassed: boolean
  jurisdictionSupported: boolean
  safetyCopyAccepted: boolean
}

export type ClosedBetaDecision = {
  acceptedIds: string[]
  rejected: Array<{ id: string; reasons: string[] }>
}

const requiredTargets: ReleaseTarget[] = ['web', 'ios', 'android']
const verified = (status: EvidenceStatus) => status === 'verified'

function missingStatus(label: string, status: EvidenceStatus, failures: string[]) {
  if (!verified(status)) failures.push(`${label} is ${status}`)
}

export function evaluateDeploymentReadiness(input: {
  evidence: DeploymentEvidence[]
  operations: OperationalControlEvidence
  diagnosticsClaimsPresent: boolean
  fakePlatformCoverageClaimsPresent: boolean
}) {
  const failures: string[] = []
  for (const target of requiredTargets) {
    const evidence = input.evidence.find((item) => item.target === target)
    if (!evidence) {
      failures.push(`${target} deployment evidence is missing`)
      continue
    }
    missingStatus(`${target} production build`, evidence.build, failures)
    missingStatus(`${target} smoke test`, evidence.smokeTest, failures)
    missingStatus(`${target} distribution`, evidence.distribution, failures)
    missingStatus(`${target} monitoring`, evidence.monitoring, failures)
    missingStatus(`${target} rollback`, evidence.rollback, failures)
  }
  missingStatus('observability', input.operations.observability, failures)
  missingStatus('backup restore drill', input.operations.backupsRestore, failures)
  missingStatus('incident response', input.operations.incidentResponse, failures)
  missingStatus('cost controls', input.operations.costControls, failures)
  missingStatus('privacy request operations', input.operations.privacyRequests, failures)
  missingStatus('closed-beta consent operations', input.operations.closedBetaConsent, failures)
  if (input.diagnosticsClaimsPresent) failures.push('Diagnostic or clinical claims must be removed before release')
  if (input.fakePlatformCoverageClaimsPresent) failures.push('Platform coverage claims must match verified sources only')
  return { decision: failures.length ? 'BLOCK' as const : 'GO' as const, failures }
}

export function selectClosedBetaParticipants(candidates: ClosedBetaCandidate[]): ClosedBetaDecision {
  const acceptedIds: string[] = []
  const rejected: ClosedBetaDecision['rejected'] = []
  for (const candidate of candidates) {
    const reasons: string[] = []
    if (!candidate.consented) reasons.push('explicit closed-beta consent missing')
    if (!candidate.syntheticOrConsentedFixture) reasons.push('requires synthetic or consented fixture data')
    if (!candidate.ageGatePassed) reasons.push('age gate not passed')
    if (!candidate.jurisdictionSupported) reasons.push('jurisdiction not supported by current privacy copy')
    if (!candidate.safetyCopyAccepted) reasons.push('non-diagnostic safety copy not accepted')
    if (reasons.length) rejected.push({ id: candidate.id, reasons })
    else acceptedIds.push(candidate.id)
  }
  return { acceptedIds, rejected }
}

export function estimateMonthlyCost(input: {
  users: number
  archiveImports: number
  oauthSyncs: number
  modelRuns: number
  storageGb: number
  unitCosts: { user: number; archiveImport: number; oauthSync: number; modelRun: number; storageGb: number }
  monthlyBudget: number
}) {
  const amounts = [input.users, input.archiveImports, input.oauthSyncs, input.modelRuns, input.storageGb, input.monthlyBudget, ...Object.values(input.unitCosts)]
  if (amounts.some((value) => !Number.isFinite(value) || value < 0)) throw new Error('Cost inputs must be non-negative finite numbers')
  const total =
    input.users * input.unitCosts.user +
    input.archiveImports * input.unitCosts.archiveImport +
    input.oauthSyncs * input.unitCosts.oauthSync +
    input.modelRuns * input.unitCosts.modelRun +
    input.storageGb * input.unitCosts.storageGb
  return { total, withinBudget: total <= input.monthlyBudget, overBy: Math.max(0, total - input.monthlyBudget) }
}
