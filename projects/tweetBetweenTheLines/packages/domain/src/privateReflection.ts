export type ReflectionVisibility = 'private' | 'shared'
export type ReflectionPurpose = 'breakup-recovery' | 'emotion-reflection' | 'life-chapter'

export type PrivateReflectionEvent = {
  id: string
  sourceId: string
  sourceRecordId: string
  occurredAt: string
  text: string
}

export type PrivateReflectionInput = {
  id: string
  title: string
  purpose: ReflectionPurpose
  visibility: ReflectionVisibility
  consented: boolean
  startAt: string
  endAt: string
  selectedEventIds: string[]
  notes: Array<{ id: string; occurredAt: string; text: string }>
  events: PrivateReflectionEvent[]
}

export type PrivateReflection = {
  id: string
  title: string
  purpose: ReflectionPurpose
  status: 'ready' | 'blocked'
  visibility: 'private'
  failures: string[]
  summary: string
  progress: {
    earlier: { events: number; strainLanguageEvents: number; supportiveLanguageEvents: number }
    later: { events: number; strainLanguageEvents: number; supportiveLanguageEvents: number }
  }
  evidence: Array<PrivateReflectionEvent & { eventId: string; matchedCategories: string[] }>
  notes: PrivateReflectionInput['notes']
  prompts: string[]
  limitations: string[]
  boundary: string
}

const strainTerms = new Set(['angry', 'heartbroken', 'lonely', 'overwhelmed', 'sad', 'stress', 'stressed', 'tired', 'worried'])
const supportiveTerms = new Set(['calm', 'connected', 'grateful', 'hopeful', 'rested', 'supported'])
const boundary = 'This is not mental-health assessment, crisis detection, or relationship judgment. It reflects only the memories and records you selected.'

function words(text: string): string[] {
  return text.normalize('NFKC').toLocaleLowerCase().match(/[\p{L}\p{N}][\p{L}\p{N}'’_-]*/gu) ?? []
}

function categories(text: string): string[] {
  const tokens = words(text)
  const result: string[] = []
  if (tokens.some((token) => strainTerms.has(token))) result.push('strain-language')
  if (tokens.some((token) => supportiveTerms.has(token))) result.push('supportive-language')
  return result
}

function counts(events: Array<PrivateReflectionEvent & { eventId: string; matchedCategories: string[] }>) {
  return {
    events: events.length,
    strainLanguageEvents: events.filter((event) => event.matchedCategories.includes('strain-language')).length,
    supportiveLanguageEvents: events.filter((event) => event.matchedCategories.includes('supportive-language')).length,
  }
}

export function buildPrivateReflection(input: PrivateReflectionInput): PrivateReflection {
  const failures: string[] = []
  if (!input.consented) failures.push('Explicit reflection consent is required.')
  if (input.visibility !== 'private') failures.push('Reflection must remain private; sharing is not available in this release.')
  if (!input.title.trim()) failures.push('A user-authored reflection title is required.')

  const blocked = failures.length > 0
  const start = new Date(input.startAt).getTime()
  const end = new Date(input.endAt).getTime()
  const selected = new Set(input.selectedEventIds)
  const evidence = blocked ? [] : input.events
    .filter((event) => selected.has(event.id))
    .filter((event) => {
      const time = new Date(event.occurredAt).getTime()
      return time >= start && time <= end
    })
    .sort((a, b) => a.occurredAt.localeCompare(b.occurredAt))
    .map((event) => ({ ...event, eventId: event.id, matchedCategories: categories(event.text) }))

  const midpoint = start + ((end - start) / 2)
  const earlier = evidence.filter((event) => new Date(event.occurredAt).getTime() < midpoint)
  const later = evidence.filter((event) => new Date(event.occurredAt).getTime() >= midpoint)

  return {
    id: input.id,
    title: input.title.trim(),
    purpose: input.purpose,
    status: blocked ? 'blocked' : 'ready',
    visibility: 'private',
    failures,
    summary: blocked
      ? 'Private reflection was not created.'
      : `${evidence.length} selected events and ${input.notes.length} self-authored note${input.notes.length === 1 ? '' : 's'} are included. Earlier and later language counts are descriptive only and do not establish recovery, healing, or how anyone should feel.`,
    progress: { earlier: counts(earlier), later: counts(later) },
    evidence,
    notes: blocked ? [] : input.notes,
    prompts: blocked ? [] : [
      'What changed in your own words during this period?',
      'Which people, routines, or places felt supportive?',
      'What would you want your future self to remember?',
    ],
    limitations: [
      'Selected records may be incomplete or unrepresentative.',
      'Language counts miss context, sarcasm, negation, dialect, and private experiences.',
      'A change in matched words does not prove recovery, healing, or causation.',
    ],
    boundary,
  }
}
