export type MeetingJobState =
  | 'queued'
  | 'normalizing'
  | 'transcribing'
  | 'diarizing'
  | 'needs_review'
  | 'failed'
  | 'cancelled'
  | 'completed'

export type RetentionPolicy = 'delete-after-transcription' | 'keep-24-hours' | 'keep-until-deleted'

export type TranscriptSegment = {
  id: string
  startSeconds: number
  endSeconds: number
  text: string
  speakerLabel: string
  confidence: number | null
  userEdited: boolean
}

export type MeetingJob = {
  id: string
  fileName: string
  state: MeetingJobState
  progress: number
  retention: RetentionPolicy
  encrypted: boolean
  consentedAt: string
  error: string | null
  attempts: number
  segments: TranscriptSegment[]
}

const transitions: Record<MeetingJobState, MeetingJobState[]> = {
  queued: ['normalizing', 'cancelled', 'failed'],
  normalizing: ['transcribing', 'cancelled', 'failed'],
  transcribing: ['diarizing', 'needs_review', 'cancelled', 'failed'],
  diarizing: ['needs_review', 'cancelled', 'failed'],
  needs_review: ['completed', 'cancelled'],
  failed: ['queued', 'cancelled'],
  cancelled: ['queued'],
  completed: [],
}

export function transitionJob(job: MeetingJob, next: MeetingJobState): MeetingJob {
  if (!transitions[job.state].includes(next)) {
    throw new Error(`Invalid meeting job transition: ${job.state} -> ${next}`)
  }

  const progressByState: Record<MeetingJobState, number> = {
    queued: 0,
    normalizing: 15,
    transcribing: 35,
    diarizing: 70,
    needs_review: 90,
    failed: job.progress,
    cancelled: job.progress,
    completed: 100,
  }

  return { ...job, state: next, progress: progressByState[next], error: null }
}

export function createMeetingJob(input: {
  id: string
  fileName: string
  retention: RetentionPolicy
  consentedAt?: string
}): MeetingJob {
  if (!input.consentedAt) throw new Error('Explicit recording consent is required')
  return {
    id: input.id,
    fileName: input.fileName,
    state: 'queued',
    progress: 0,
    retention: input.retention,
    encrypted: true,
    consentedAt: input.consentedAt,
    error: null,
    attempts: 1,
    segments: [],
  }
}

export function retryJob(job: MeetingJob): MeetingJob {
  if (job.state !== 'failed' && job.state !== 'cancelled') throw new Error('Only failed or cancelled jobs can be retried')
  return { ...transitionJob(job, 'queued'), attempts: job.attempts + 1, segments: [] }
}

export function failJob(job: MeetingJob, code: string): MeetingJob {
  if (!transitions[job.state].includes('failed')) throw new Error(`Cannot fail a ${job.state} job`)
  return { ...job, state: 'failed', error: code }
}

export function editSegment(
  segment: TranscriptSegment,
  update: { text?: string; speakerLabel?: string },
): TranscriptSegment {
  const text = update.text?.trim() ?? segment.text
  const speakerLabel = update.speakerLabel?.trim() ?? segment.speakerLabel
  if (!text) throw new Error('Transcript text cannot be empty')
  if (!speakerLabel) throw new Error('Speaker label cannot be empty')
  return { ...segment, text, speakerLabel, userEdited: true }
}

export function provisionalSpeaker(index: number) {
  return `Speaker ${index + 1}`
}

export function confidenceLabel(confidence: number | null) {
  if (confidence === null) return 'Confidence unavailable'
  if (confidence < 0.6) return 'Low confidence — review speaker and words'
  if (confidence < 0.85) return 'Moderate confidence — review recommended'
  return 'High confidence'
}
