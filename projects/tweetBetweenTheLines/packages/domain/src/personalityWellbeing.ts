export type OpenTraitInstrument = {
  id: string
  name: string
  sourceUrl: string
  license: { kind: 'open' | 'restricted' | 'unknown'; notice: string }
  version: string
  validatedLocales: string[]
  responseScale: { minimum: number; maximum: number }
  traits: Array<{ id: string; label: string }>
  items: Array<{ id: string; traitId: string; prompt: string; keyed: 'forward' | 'reverse' }>
  governance: { legalReviewed: boolean; clinicalReviewed: boolean; reviewedAt: string | null }
}

export type SelfReportSubmission = {
  locale: string
  consented: boolean
  answers: Record<string, number>
}

export type PersonalitySelfReportResult = {
  allowed: boolean
  signalSource: 'self-report-questionnaire'
  instrument: { id: string; name: string; version: string; sourceUrl: string; licenseNotice: string }
  locale: string
  scores: Array<{ traitId: string; label: string; answeredItems: number; possibleItems: number; normalizedScore: number }>
  failures: string[]
  disclosure: string
}

function language(locale: string): string {
  return locale.trim().toLowerCase().split(/[-_]/)[0]
}

export function scorePersonalitySelfReport(
  instrument: OpenTraitInstrument,
  submission: SelfReportSubmission,
): PersonalitySelfReportResult {
  const locale = language(submission.locale)
  const failures: string[] = []
  if (!submission.consented) failures.push('Separate self-report consent is required.')
  if (instrument.license.kind !== 'open') failures.push('Instrument licensing is not approved for release.')
  if (!instrument.validatedLocales.map(language).includes(locale)) failures.push(`Instrument is not validated for locale ${locale}.`)
  if (!instrument.governance.clinicalReviewed || !instrument.governance.legalReviewed) {
    failures.push('Clinical and legal review are required before public release.')
  }

  const { minimum, maximum } = instrument.responseScale
  const itemIds = new Set(instrument.items.map((item) => item.id))
  const answersAreComplete = instrument.items.every((item) => {
    const answer = submission.answers[item.id]
    return Number.isFinite(answer) && answer >= minimum && answer <= maximum
  }) && Object.keys(submission.answers).every((id) => itemIds.has(id))
  if (!answersAreComplete) failures.push('Every instrument item requires an in-range response.')

  const scores = failures.length === 0 ? instrument.traits.map((trait) => {
    const items = instrument.items.filter((item) => item.traitId === trait.id)
    const values = items.map((item) => {
      const answer = submission.answers[item.id]
      const keyed = item.keyed === 'reverse' ? maximum + minimum - answer : answer
      return (keyed - minimum) / (maximum - minimum)
    })
    return {
      traitId: trait.id,
      label: trait.label,
      answeredItems: values.length,
      possibleItems: items.length,
      normalizedScore: values.length ? Number((values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(4)) : 0,
    }
  }) : []

  return {
    allowed: failures.length === 0,
    signalSource: 'self-report-questionnaire',
    instrument: { id: instrument.id, name: instrument.name, version: instrument.version, sourceUrl: instrument.sourceUrl, licenseNotice: instrument.license.notice },
    locale,
    scores,
    failures,
    disclosure: 'These optional self-report trait scores describe answers to this questionnaire only. They are not a diagnosis, clinical assessment, fixed personality type, or conclusion drawn from social activity.',
  }
}

export type WellbeingObservationEvent = {
  id: string
  sourceId: string
  sourceRecordId: string
  occurredAt: string
  text: string
}

export type ObservationalWellbeingReflection = {
  status: 'ready' | 'abstained'
  signalSource: 'observational-language'
  locale: string
  generatedAt: string
  summary: string
  counts: { eventsAnalyzed: number; eventsWithStrainTerms: number; eventsWithSupportiveTerms: number }
  evidence: Array<{ eventId: string; sourceId: string; sourceRecordId: string; occurredAt: string; excerpt: string; matchedCategories: string[] }>
  limitations: string[]
  disclosure: string
  helpGuidance: string
}

const WELLBEING_LEXICON: Record<string, { strain: Set<string>; supportive: Set<string> }> = {
  en: {
    strain: new Set(['angry', 'deadline', 'deadlines', 'overwhelmed', 'sad', 'stress', 'stressed', 'tired', 'worried']),
    supportive: new Set(['calm', 'connected', 'grateful', 'hopeful', 'rested', 'supported']),
  },
  es: {
    strain: new Set(['abrumado', 'cansado', 'enojado', 'estrés', 'preocupado', 'triste']),
    supportive: new Set(['agradecido', 'apoyado', 'calma', 'conectado', 'descansado', 'esperanza']),
  },
  fr: {
    strain: new Set(['colère', 'débordé', 'fatigué', 'inquiet', 'stress', 'triste']),
    supportive: new Set(['calme', 'connecté', 'espoir', 'reconnaissant', 'reposé', 'soutenu']),
  },
  de: {
    strain: new Set(['besorgt', 'müde', 'stress', 'traurig', 'überfordert', 'wütend']),
    supportive: new Set(['dankbar', 'erholt', 'hoffnung', 'ruhig', 'unterstützt', 'verbunden']),
  },
  pt: {
    strain: new Set(['cansado', 'estresse', 'irritado', 'preocupado', 'sobrecarregado', 'triste']),
    supportive: new Set(['apoiado', 'calma', 'conectado', 'descansado', 'esperança', 'grato']),
  },
}

function tokens(text: string): string[] {
  return text.normalize('NFKC').toLocaleLowerCase().match(/[\p{L}\p{N}][\p{L}\p{N}'’_-]*/gu) ?? []
}

function safeExcerpt(text: string): string {
  const compact = text.trim().replace(/\s+/g, ' ')
  return compact.length <= 160 ? compact : `${compact.slice(0, 157)}...`
}

const disclosure = 'Language counts from posts cannot diagnose depression, anxiety, crisis, or any other condition. Absence of matched terms is not evidence of wellbeing.'
const helpGuidance = 'If you are concerned about your wellbeing, consider contacting a qualified professional. If you may be in immediate danger, contact local emergency services or a verified crisis service for your location. This product does not monitor for emergencies or dispatch help.'

export function buildObservationalWellbeingReflection(input: {
  locale: string
  generatedAt: string
  events: WellbeingObservationEvent[]
}): ObservationalWellbeingReflection {
  const locale = language(input.locale)
  const lexicon = WELLBEING_LEXICON[locale]
  const base = {
    signalSource: 'observational-language' as const,
    locale,
    generatedAt: new Date(input.generatedAt).toISOString(),
    limitations: ['Lexical matches miss context, negation, sarcasm, slang, dialect, and code-switching.', 'The selected time window and available sources may not be representative.'],
    disclosure,
    helpGuidance,
  }
  if (!lexicon) {
    return {
      ...base,
      status: 'abstained',
      summary: `No reflection is shown because this lexical method is not validated for locale ${locale}.`,
      counts: { eventsAnalyzed: input.events.length, eventsWithStrainTerms: 0, eventsWithSupportiveTerms: 0 },
      evidence: [],
    }
  }

  let eventsWithStrainTerms = 0
  let eventsWithSupportiveTerms = 0
  const evidence = input.events.flatMap((event) => {
    const words = tokens(event.text)
    const matchedCategories: string[] = []
    if (words.some((word) => lexicon.strain.has(word))) { eventsWithStrainTerms += 1; matchedCategories.push('strain-language') }
    if (words.some((word) => lexicon.supportive.has(word))) { eventsWithSupportiveTerms += 1; matchedCategories.push('supportive-language') }
    return matchedCategories.length ? [{
      eventId: event.id,
      sourceId: event.sourceId,
      sourceRecordId: event.sourceRecordId,
      occurredAt: new Date(event.occurredAt).toISOString(),
      excerpt: safeExcerpt(event.text),
      matchedCategories,
    }] : []
  })
  return {
    ...base,
    status: 'ready',
    summary: `In this selected slice, ${eventsWithStrainTerms} of ${input.events.length} events included strain terms and ${eventsWithSupportiveTerms} included supportive terms. This is a descriptive reflection, not an assessment of the person.`,
    counts: { eventsAnalyzed: input.events.length, eventsWithStrainTerms, eventsWithSupportiveTerms },
    evidence,
  }
}
