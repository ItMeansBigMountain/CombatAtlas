import type { MeetingArtifact } from './meetingIntelligence'

export type JournalEntry = {
  id: string
  body: string
  mood: string
  createdAt: string
  updatedAt: string
  private: true
  sourceMeetingIds: string[]
  deletedAt: string | null
}

export type OfflineMutation = {
  id: string
  kind: 'upsert' | 'delete'
  entryId: string
  queuedAt: string
}

export function createJournalEntry(input: { id: string; body: string; mood: string; createdAt: string }): JournalEntry {
  const body = input.body.trim()
  if (!body) throw new Error('Journal entry cannot be empty')
  return {
    id: input.id,
    body,
    mood: input.mood,
    createdAt: input.createdAt,
    updatedAt: input.createdAt,
    private: true,
    sourceMeetingIds: [],
    deletedAt: null,
  }
}

export function approveArtifactIntoJournal(entry: JournalEntry, artifact: MeetingArtifact): JournalEntry {
  if (entry.deletedAt) throw new Error('Cannot update a deleted journal entry')
  if (artifact.status !== 'approved') throw new Error('Only approved meeting artifacts can be journaled')
  const sourceMeetingIds = [...new Set([...entry.sourceMeetingIds, artifact.meetingId])]
  return {
    ...entry,
    body: `${entry.body}\n\n${artifact.text}`,
    updatedAt: new Date().toISOString(),
    sourceMeetingIds,
  }
}

export function deleteJournalEntry(entry: JournalEntry, deletedAt: string): JournalEntry {
  return { ...entry, body: '', deletedAt, updatedAt: deletedAt }
}

export function purgeDeletedEntries(entries: JournalEntry[], purgedAt: string) {
  const purgedEntryIds = entries.filter((entry) => entry.deletedAt).map((entry) => entry.id)
  return {
    entries: entries.filter((entry) => !entry.deletedAt),
    receipt: { purgedEntryIds, purgedAt },
  }
}

export function queueOfflineMutation(queue: OfflineMutation[], mutation: OfflineMutation): OfflineMutation[] {
  if (queue.some((item) => item.id === mutation.id)) return queue
  return [...queue, mutation]
}

export function journalDeepLink(id: string) {
  return `journalai://journal/${encodeURIComponent(id)}`
}

export function exportJournal(entries: JournalEntry[], format: 'json' | 'markdown') {
  const active = entries.filter((entry) => !entry.deletedAt)
  if (format === 'json') return JSON.stringify(active, null, 2)
  const body = active.map((entry) => `## ${entry.createdAt}\n\n${entry.body}`).join('\n\n')
  return `# Private journal export\n\n${body}\n`
}
