import type { TranscriptSegment } from './meetingWorkflow'

export type ArtifactKind = 'summary' | 'decision' | 'action_item' | 'commitment' | 'question' | 'private_reflection'
export type ArtifactStatus = 'draft' | 'approved'

export type MeetingArtifact = {
  id: string
  meetingId: string
  kind: ArtifactKind
  text: string
  citations: string[]
  status: ArtifactStatus
  owner?: string
  dueText?: string
  private: boolean
}

export type ArtifactStore = { artifacts: MeetingArtifact[] }
export type ThemeSignal = { label: string; meetingId: string }
export type RecurringTheme = { label: string; count: number; meetingIds: string[] }

const diagnosticTerms = /\b(disorder|diagnosis|diagnosed|bipolar|depression|depressed|narcissist|psychopath|adhd|autis(?:m|tic)|ptsd)\b/i

function artifact(meetingId: string, kind: ArtifactKind, text: string, citations: string[], extra: Partial<MeetingArtifact> = {}): MeetingArtifact {
  return {
    id: `${meetingId}-${kind}-${citations.join('-')}`,
    meetingId,
    kind,
    text,
    citations,
    status: 'draft',
    private: kind === 'private_reflection',
    ...extra,
  }
}

export function buildDraftArtifacts(meetingId: string, segments: TranscriptSegment[]): MeetingArtifact[] {
  const usable = segments.filter((segment) => segment.userEdited && segment.text.trim())
  if (usable.length === 0) return []

  const results: MeetingArtifact[] = [
    artifact(meetingId, 'summary', usable.map((segment) => segment.text.trim()).join(' '), usable.map((segment) => segment.id)),
  ]

  for (const segment of usable) {
    const text = segment.text.trim()
    if (/\b(decided|decision|agreed)\b/i.test(text)) results.push(artifact(meetingId, 'decision', text, [segment.id]))
    if (/\b(question|do we|should we|could we|what if)\b/i.test(text) || text.endsWith('?')) results.push(artifact(meetingId, 'question', text, [segment.id]))

    const commitment = text.match(/^(.+?)\s+(?:will|commits? to)\s+(.+?)(?:\s+by\s+([^.!?]+))?[.!?]?$/i)
    if (commitment) {
      const owner = commitment[1].trim()
      const dueText = commitment[3]?.trim()
      results.push(artifact(meetingId, 'commitment', text, [segment.id], { owner, ...(dueText ? { dueText } : {}) }))
    } else if (/\b(action item|follow up|next step)\b/i.test(text)) {
      results.push(artifact(meetingId, 'action_item', text, [segment.id]))
    }
  }

  return results
}

export function createArtifactStore(artifacts: MeetingArtifact[]): ArtifactStore {
  return { artifacts: artifacts.map((item) => ({ ...item, citations: [...item.citations] })) }
}

export function approveArtifact(store: ArtifactStore, id: string): ArtifactStore {
  if (!store.artifacts.some((item) => item.id === id)) throw new Error(`Artifact not found: ${id}`)
  return { artifacts: store.artifacts.map((item) => item.id === id ? { ...item, status: 'approved' } : item) }
}

export function deleteArtifact(store: ArtifactStore, id: string): ArtifactStore {
  if (!store.artifacts.some((item) => item.id === id)) throw new Error(`Artifact not found: ${id}`)
  return { artifacts: store.artifacts.filter((item) => item.id !== id) }
}

export function exportArtifact(store: ArtifactStore, id: string, format: 'json' | 'markdown'): string {
  const item = store.artifacts.find((artifactItem) => artifactItem.id === id)
  if (!item) throw new Error(`Artifact not found: ${id}`)
  if (format === 'json') return JSON.stringify(item, null, 2)
  return `# ${item.kind.replaceAll('_', ' ')}\n\n${item.text}\n\nSources: ${item.citations.join(', ')}\nStatus: ${item.status}\n`
}

export function recurringThemes(signals: ThemeSignal[]): RecurringTheme[] {
  const grouped = new Map<string, { label: string; meetingIds: Set<string> }>()
  for (const signal of signals) {
    const label = signal.label.trim().toLowerCase()
    if (!label || diagnosticTerms.test(label)) continue
    const current = grouped.get(label) ?? { label, meetingIds: new Set<string>() }
    current.meetingIds.add(signal.meetingId)
    grouped.set(label, current)
  }
  return [...grouped.values()]
    .filter((theme) => theme.meetingIds.size > 1)
    .map((theme) => ({ label: theme.label, count: theme.meetingIds.size, meetingIds: [...theme.meetingIds] }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label))
}
