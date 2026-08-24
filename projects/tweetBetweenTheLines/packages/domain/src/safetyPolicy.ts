export type ConsentReceiptInput = {
  tenantId: string
  subjectId: string
  sourceId: string
  purposes: string[]
  dataCategories: string[]
  grantedAt: string
  policyVersion: string
}

export type ConsentReceipt = ConsentReceiptInput & {
  id: string
  status: 'active' | 'revoked'
  revokedAt: string | null
}

function canonical(values: string[]): string[] {
  return [...new Set(values.map((value) => value.trim()).filter(Boolean))].sort()
}

export function createConsentReceipt(input: ConsentReceiptInput): ConsentReceipt {
  const grantedAt = new Date(input.grantedAt).toISOString()
  const identity = [input.tenantId, input.subjectId, input.sourceId, input.policyVersion, grantedAt]
    .map((value) => encodeURIComponent(value.trim()))
    .join(':')
  return {
    ...input,
    tenantId: input.tenantId.trim(),
    subjectId: input.subjectId.trim(),
    sourceId: input.sourceId.trim(),
    purposes: canonical(input.purposes),
    dataCategories: canonical(input.dataCategories),
    grantedAt,
    id: `consent:${identity}`,
    status: 'active',
    revokedAt: null,
  }
}

export type ProcessingEnvelopeInput = {
  tenantId: string
  subjectId: string
  sourceId: string
  tokenRef: string
  rawObjectRef: string
  featureSetRef: string
  aggregateEvidence: Record<string, unknown>
}

export function createProcessingEnvelope(input: ProcessingEnvelopeInput) {
  return {
    partitionKey: `${input.tenantId}:${input.subjectId}`,
    secrets: { tenantId: input.tenantId, tokenRef: input.tokenRef },
    raw: { tenantId: input.tenantId, objectRef: input.rawObjectRef },
    features: { tenantId: input.tenantId, featureSetRef: input.featureSetRef },
    modelPayload: {
      tenantId: input.tenantId,
      subjectId: input.subjectId,
      sourceId: input.sourceId,
      aggregateEvidence: structuredClone(input.aggregateEvidence),
    },
  }
}

export type DeletionPlanInput = {
  tenantId: string
  subjectId: string
  sourceId: string
  consentReceiptIds: string[]
  rawObjectRefs: string[]
  normalizedEventIds: string[]
  featureSetIds: string[]
  insightIds: string[]
}

export type DataLayer = 'insight' | 'feature' | 'normalized' | 'raw' | 'token' | 'consent'

export function buildDeletionPlan(input: DeletionPlanInput) {
  const deletionLineage = `${input.tenantId}:${input.subjectId}:${input.sourceId}`
  return {
    deletionLineage,
    deleteOrder: [
      { layer: 'insight', ids: canonical(input.insightIds) },
      { layer: 'feature', ids: canonical(input.featureSetIds) },
      { layer: 'normalized', ids: canonical(input.normalizedEventIds) },
      { layer: 'raw', ids: canonical(input.rawObjectRefs) },
      { layer: 'token', ids: [`vault://${input.tenantId}/${input.subjectId}/${input.sourceId}`] },
      { layer: 'consent', ids: canonical(input.consentReceiptIds) },
    ] satisfies Array<{ layer: DataLayer; ids: string[] }>,
    auditTombstone: {
      deletionLineage,
      action: 'source-data-deleted' as const,
      containsPersonalData: false as const,
    },
  }
}

export type InsightReleaseInput = {
  category: 'general' | 'observational-wellbeing' | 'self-report-screener'
  text: string
  professionalReview: boolean
  crisisFlowConfigured: boolean
  instrument: null | {
    name: string
    license: 'open' | 'restricted' | 'unknown'
    validatedLocales: string[]
    locale: string
  }
}

const diagnosticClaims = /\b(clinically|you (?:are|have|suffer from|seem|appear)|mental disorder|depressed|anxiety disorder|suicidal|psychotic)\b/i
const harmfulMentalHealthDirection = /\b(?:stop|skip|avoid) (?:taking )?(?:your )?(?:medication|medicine|therapy)|\bdo not (?:seek|contact|tell) (?:a )?(?:doctor|professional|therapist|emergency service)\b/i

export function assessInsightRelease(input: InsightReleaseInput) {
  const failures: string[] = []
  if (diagnosticClaims.test(input.text)) {
    failures.push('Diagnostic or clinical claim is prohibited.')
  }
  if (harmfulMentalHealthDirection.test(input.text)) failures.push('Unsafe mental-health direction is prohibited.')
  if (input.category === 'self-report-screener') {
    if (!input.instrument) failures.push('A named validated instrument is required.')
    if (input.instrument?.license !== 'open') failures.push('Instrument licensing is not approved.')
    if (input.instrument && !input.instrument.validatedLocales.includes(input.instrument.locale)) {
      failures.push('Instrument is not validated for the requested locale.')
    }
    if (!input.professionalReview) failures.push('Professional review is required before release.')
    if (!input.crisisFlowConfigured) failures.push('A locale-aware crisis escalation flow is required.')
    if (!/not a diagnosis/i.test(input.text)) failures.push('Non-diagnostic disclosure is required.')
  }
  return { allowed: failures.length === 0, failures }
}

export type ModelProvenanceInput = {
  provider: string
  model: string
  version: string
  promptVersion: string
  featureSchemaVersion: string
  inputDigest: string
  generatedAt: string
}

export function buildModelProvenance(input: ModelProvenanceInput) {
  for (const [field, value] of Object.entries(input)) {
    if (typeof value !== 'string' || !value.trim()) throw new Error(`Model provenance ${field} is required`)
  }
  if (!/^sha256:[a-f0-9]{64}$/.test(input.inputDigest)) throw new Error('Model provenance requires a SHA-256 input digest')
  return {
    ...input,
    generatedAt: new Date(input.generatedAt).toISOString(),
    reviewStatus: 'unreviewed' as const,
  }
}

export type CohortEvaluation = {
  locale: string
  sampleSize: number
  falsePositiveRate: number
  falseNegativeRate: number
  calibrationError: number
}

export type EvaluationThresholds = {
  minimumSampleSize: number
  maximumErrorRate: number
  maximumCalibrationError: number
  maximumInterCohortDisparity: number
}

export function evaluateCohortReadiness(cohorts: CohortEvaluation[], thresholds: EvaluationThresholds) {
  const failures: string[] = []
  for (const cohort of cohorts) {
    if (!cohort.locale.trim() || !Number.isSafeInteger(cohort.sampleSize) || cohort.sampleSize < 0 ||
        [cohort.falsePositiveRate, cohort.falseNegativeRate, cohort.calibrationError].some((value) => !Number.isFinite(value) || value < 0 || value > 1)) {
      failures.push(`${cohort.locale || 'unknown'}: invalid cohort metrics`)
      continue
    }
    if (cohort.sampleSize < thresholds.minimumSampleSize) failures.push(`${cohort.locale}: sample too small`)
    if (cohort.falsePositiveRate > thresholds.maximumErrorRate) failures.push(`${cohort.locale}: false-positive rate too high`)
    if (cohort.falseNegativeRate > thresholds.maximumErrorRate) failures.push(`${cohort.locale}: false-negative rate too high`)
    if (cohort.calibrationError > thresholds.maximumCalibrationError) failures.push(`${cohort.locale}: calibration error too high`)
  }
  const rates = cohorts.flatMap((cohort) => [cohort.falsePositiveRate, cohort.falseNegativeRate])
  if (rates.length > 0 && Math.max(...rates) - Math.min(...rates) > thresholds.maximumInterCohortDisparity) {
    failures.push('Inter-cohort error disparity exceeds threshold.')
  }
  return { ready: cohorts.length > 0 && failures.length === 0, failures }
}

export type SensitiveOperation = 'export' | 'delete' | 'support-access' | 'token-read'
export function authorizeSensitiveOperation(input: {
  actorId: string
  actorClass: 'user' | 'connector' | 'worker' | 'support' | 'admin'
  subjectId: string
  operation: SensitiveOperation
  stepUpAuthenticated: boolean
  supportCaseId?: string
}) {
  const failures: string[] = []
  if (!input.actorId.trim() || !input.subjectId.trim()) failures.push('Actor and subject identity are required.')
  if (!input.stepUpAuthenticated) failures.push('Step-up authentication is required.')
  if (input.actorClass === 'user' && input.actorId !== input.subjectId) failures.push('Users may act only on their own account.')
  if ((input.actorClass === 'support' || input.actorClass === 'admin') && !input.supportCaseId?.trim()) failures.push('Privileged access requires a support case.')
  if (input.operation === 'token-read' && !['connector'].includes(input.actorClass)) failures.push('Only the connector runtime may read provider tokens.')
  if (['worker', 'connector'].includes(input.actorClass) && input.operation !== 'token-read') failures.push('Service actors may not perform user privacy operations.')
  return { allowed: failures.length === 0, failures }
}

export function buildReleaseGate(input: {
  criticalFindings: number
  highFindings: number
  regressionTestsPassing: boolean
  modelProvenanceVerified: boolean
  deletionReconciliationPassing: boolean
  cohortEvaluationReady: boolean
  safetyReviewApproved: boolean
}) {
  const failures: string[] = []
  if (input.criticalFindings !== 0) failures.push('Open critical security findings remain.')
  if (input.highFindings !== 0) failures.push('Open high security findings remain.')
  if (!input.regressionTestsPassing) failures.push('Security regression tests are not passing.')
  if (!input.modelProvenanceVerified) failures.push('Model provenance is not verified.')
  if (!input.deletionReconciliationPassing) failures.push('Deletion reconciliation is not passing.')
  if (!input.cohortEvaluationReady) failures.push('Multilingual cohort evaluation is not ready.')
  if (!input.safetyReviewApproved) failures.push('Safety review is not approved.')
  return { decision: failures.length ? 'BLOCK' as const : 'GO' as const, failures }
}
