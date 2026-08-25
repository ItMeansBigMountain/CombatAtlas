export type MetricEventKind = 'post' | 'message' | 'reaction' | 'view' | 'listen' | 'search' | 'import-note'

export type MetricEvent = {
  id: string
  sourceId: string
  sourceRecordId: string
  occurredAt: string
  kind: MetricEventKind
  content: string
  locale?: string | null
  metadata?: Record<string, string | number | boolean | null>
}

export type EvidenceRef = {
  eventId: string
  sourceId: string
  sourceRecordId: string
  occurredAt: string
  excerpt: string
  matched: string[]
}

export type SourceCoverage = {
  sourceId: string
  events: number
  firstEventAt: string
  lastEventAt: string
  kinds: Partial<Record<MetricEventKind, number>>
  locales: Record<string, number>
}

export type MetricConfidence = {
  level: 'insufficient' | 'low' | 'medium' | 'high'
  score: number
  reasons: string[]
}

export type ExplainableMetricCard = {
  id: string
  category: 'interests' | 'topics' | 'communities' | 'language-style' | 'sentiment' | 'attention-rhythm' | 'media-affinity' | 'stated-vs-observed' | 'change-over-time'
  title: string
  sourceCoverage: SourceCoverage[]
  aggregates: Record<string, unknown>
  confidence: MetricConfidence
  limitations: string[]
  evidence: EvidenceRef[]
  formula: { version: string; expression: string }
  analyzer: { schemaVersion: '1'; method: 'deterministic'; narrativeReady: boolean }
}

export type ExplainableMetricsSnapshot = {
  generatedAt: string
  eventCount: number
  cards: ExplainableMetricCard[]
  narrativeGate: { allowed: boolean; reason: string }
}

type AnalyzedEvent = MetricEvent & { tokens: string[]; detectedLocale: string }

const WORDS: Record<string, Set<string>> = {
  en: new Set(['the', 'and', 'is', 'are', 'with', 'for', 'this', 'that', 'my', 'i', 'we', 'to', 'of', 'in']),
  es: new Set(['el', 'la', 'los', 'las', 'y', 'es', 'con', 'para', 'mi', 'yo', 'de', 'en', 'que']),
  fr: new Set(['le', 'la', 'les', 'et', 'est', 'avec', 'pour', 'mon', 'je', 'de', 'dans', 'que']),
  de: new Set(['der', 'die', 'das', 'und', 'ist', 'mit', 'für', 'mein', 'ich', 'zu', 'von', 'in']),
  pt: new Set(['o', 'a', 'os', 'as', 'e', 'é', 'com', 'para', 'meu', 'eu', 'de', 'em', 'que']),
}

const SENTIMENT: Record<string, { positive: Set<string>; negative: Set<string> }> = {
  en: { positive: new Set(['good', 'great', 'love', 'happy', 'grateful', 'hopeful', 'excited', 'calm', 'proud']), negative: new Set(['bad', 'hate', 'sad', 'angry', 'worried', 'stress', 'stressed', 'tired', 'overwhelmed']) },
  es: { positive: new Set(['bueno', 'genial', 'amor', 'feliz', 'agradecido', 'esperanza', 'emocionado', 'calma']), negative: new Set(['malo', 'odio', 'triste', 'enojado', 'preocupado', 'estrés', 'cansado', 'abrumado']) },
  fr: { positive: new Set(['bon', 'super', 'amour', 'heureux', 'reconnaissant', 'espoir', 'calme']), negative: new Set(['mauvais', 'haine', 'triste', 'colère', 'inquiet', 'stress', 'fatigué', 'débordé']) },
  de: { positive: new Set(['gut', 'toll', 'liebe', 'glücklich', 'dankbar', 'hoffnung', 'ruhig']), negative: new Set(['schlecht', 'hass', 'traurig', 'wütend', 'besorgt', 'stress', 'müde', 'überfordert']) },
  pt: { positive: new Set(['bom', 'ótimo', 'amor', 'feliz', 'grato', 'esperança', 'calma']), negative: new Set(['ruim', 'ódio', 'triste', 'irritado', 'preocupado', 'estresse', 'cansado', 'sobrecarregado']) },
}

const INTERESTS: Record<string, Set<string>> = {
  music: new Set(['music', 'música', 'musique', 'musik', 'song', 'canción', 'chanson', 'playlist', 'album']),
  fitness: new Set(['fitness', 'workout', 'gym', 'running', 'correr', 'entraînement', 'training', 'treino']),
  technology: new Set(['technology', 'tech', 'software', 'coding', 'programming', 'tecnología', 'logiciel', 'programmierung', 'tecnologia']),
  gaming: new Set(['gaming', 'game', 'games', 'juego', 'jeu', 'spiel', 'jogo']),
  learning: new Set(['learn', 'learning', 'study', 'school', 'aprender', 'étudier', 'lernen', 'estudar']),
}

const STOP = new Set([...Object.values(WORDS).flatMap((set) => [...set]), 'http', 'https', 'www', 'com'])

const FORMULAS: Record<ExplainableMetricCard['category'], string> = {
  interests: 'count(label) = number of events containing at least one configured interest term for label',
  topics: 'count(token) = number of events containing token at least once after NFKC tokenization and stop-word removal',
  communities: 'count(name) = number of events whose community, channel, or subreddit metadata equals name',
  'language-style': 'average_tokens_per_event = total_tokens / imported_events; unique_tokens = cardinality(all normalized tokens)',
  sentiment: 'class(event) = positive when positive_terms > negative_terms, negative when negative_terms > positive_terms, otherwise neutral',
  'attention-rhythm': 'hourly_utc[h] = count(events where UTC hour = h); weekday_utc[d] = count(events where UTC weekday = d)',
  'media-affinity': 'count(name) = number of events whose creator, artist, channel, or mediaTitle metadata equals name',
  'stated-vs-observed': 'stated(label) = any post/message/import-note matching label; observed(label) = any view/listen/search/reaction matching label',
  'change-over-time': 'midpoint = (earliest_timestamp + latest_timestamp) / 2; early = count(timestamp <= midpoint); recent = count(timestamp > midpoint)',
}

function tokenize(text: string): string[] {
  return (text.normalize('NFKC').toLocaleLowerCase().match(/[\p{L}\p{N}][\p{L}\p{N}'’_-]*/gu) ?? []).map((word) => word.replace(/’/g, "'"))
}

function localeFor(event: MetricEvent, tokens: string[]): string {
  const declared = event.locale?.trim().toLowerCase().split(/[-_]/)[0]
  if (declared && WORDS[declared]) return declared
  const ranked = Object.entries(WORDS).map(([locale, words]) => [locale, tokens.filter((word) => words.has(word)).length] as const)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  return ranked[0]?.[1] ? ranked[0][0] : 'und'
}

function excerpt(text: string): string {
  const normalized = text.trim().replace(/\s+/g, ' ')
  return normalized.length <= 160 ? normalized : `${normalized.slice(0, 157)}...`
}

function coverage(events: AnalyzedEvent[]): SourceCoverage[] {
  const groups = new Map<string, AnalyzedEvent[]>()
  for (const event of events) groups.set(event.sourceId, [...(groups.get(event.sourceId) ?? []), event])
  return [...groups.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([sourceId, rows]) => ({
    sourceId, events: rows.length, firstEventAt: rows[0].occurredAt, lastEventAt: rows.at(-1)!.occurredAt,
    kinds: rows.reduce((out, row) => ({ ...out, [row.kind]: (out[row.kind] ?? 0) + 1 }), {} as Partial<Record<MetricEventKind, number>>),
    locales: rows.reduce((out, row) => ({ ...out, [row.detectedLocale]: (out[row.detectedLocale] ?? 0) + 1 }), {} as Record<string, number>),
  }))
}

function confidence(events: MetricEvent[], evidenceCount: number, sources: number): MetricConfidence {
  const score = Math.min(1, Number((Math.min(events.length / 20, 0.5) + Math.min(evidenceCount / 10, 0.3) + Math.min(sources / 4, 0.2)).toFixed(2)))
  const level = events.length < 3 || evidenceCount === 0 ? 'insufficient' : score >= 0.8 ? 'high' : score >= 0.5 ? 'medium' : 'low'
  return { level, score, reasons: [`${events.length} events analyzed`, `${evidenceCount} supporting events`, `${sources} source${sources === 1 ? '' : 's'} represented`] }
}

function evidence(events: AnalyzedEvent[], select: (event: AnalyzedEvent) => string[], limit = 12): EvidenceRef[] {
  return events.flatMap((event) => {
    const matched = [...new Set(select(event))].sort()
    return matched.length ? [{ eventId: event.id, sourceId: event.sourceId, sourceRecordId: event.sourceRecordId, occurredAt: event.occurredAt, excerpt: excerpt(event.content), matched }] : []
  }).slice(0, limit)
}

function ranked(counts: Map<string, number>, limit = 12): Array<{ label: string; count: number }> {
  return [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, limit).map(([label, count]) => ({ label, count }))
}

export function buildExplainableMetrics(input: MetricEvent[], generatedAt = new Date(0).toISOString()): ExplainableMetricsSnapshot {
  const seen = new Set<string>()
  const events = input.map((row) => {
    if (!row.id.trim() || !row.sourceId.trim() || !row.sourceRecordId.trim()) throw new Error('Event identity and source provenance are required')
    if (seen.has(row.id)) throw new Error(`Duplicate event id: ${row.id}`)
    seen.add(row.id)
    const occurredAt = new Date(row.occurredAt).toISOString(); const tokens = tokenize(row.content)
    return { ...row, occurredAt, content: row.content.trim(), tokens, detectedLocale: localeFor(row, tokens) }
  }).sort((a, b) => a.occurredAt.localeCompare(b.occurredAt) || a.id.localeCompare(b.id))
  const sourceCoverage = coverage(events); const sources = sourceCoverage.length
  const limitations = ['Counts describe only imported, consented data; missing or unavailable sources can change results.', 'Lexicon and metadata matches do not establish identity, intent, beliefs, or clinical state.', 'Low-volume and uneven time windows reduce representativeness.']
  const make = (id: string, category: ExplainableMetricCard['category'], title: string, aggregates: Record<string, unknown>, refs: EvidenceRef[], extra: string[] = []): ExplainableMetricCard => ({ id, category, title, sourceCoverage, aggregates, confidence: confidence(events, refs.length, sources), limitations: [...limitations, ...extra], evidence: refs, formula: { version: `metric-formula@1:${id}`, expression: FORMULAS[category] }, analyzer: { schemaVersion: '1', method: 'deterministic', narrativeReady: events.length >= 3 && refs.length > 0 } })

  const interestCounts = new Map<string, number>()
  const interestEvidence = evidence(events, (event) => Object.entries(INTERESTS).flatMap(([label, terms]) => event.tokens.some((word) => terms.has(word)) ? [label] : []))
  for (const ref of interestEvidence) for (const label of ref.matched) interestCounts.set(label, (interestCounts.get(label) ?? 0) + 1)

  const topicCounts = new Map<string, number>()
  for (const event of events) for (const token of new Set(event.tokens.filter((word) => word.length > 2 && !STOP.has(word)))) topicCounts.set(token, (topicCounts.get(token) ?? 0) + 1)
  const topicRows = ranked(topicCounts); const topicSet = new Set(topicRows.map((row) => row.label))
  const topicEvidence = evidence(events, (event) => event.tokens.filter((word) => topicSet.has(word)))

  const communityCounts = new Map<string, number>(); const communityEvidence = evidence(events, (event) => {
    const values = [event.metadata?.community, event.metadata?.channel, event.metadata?.subreddit].filter((value): value is string => typeof value === 'string' && value.trim().length > 0).map((value) => value.trim())
    for (const value of values) communityCounts.set(value, (communityCounts.get(value) ?? 0) + 1)
    return values
  })

  const sentiment = { positive: 0, negative: 0, neutral: 0 }; const sentimentEvidence = evidence(events, (event) => {
    const lexicon = SENTIMENT[event.detectedLocale]; if (!lexicon) { sentiment.neutral += 1; return [] }
    const positive = event.tokens.filter((word) => lexicon.positive.has(word)).length; const negative = event.tokens.filter((word) => lexicon.negative.has(word)).length
    sentiment[positive === negative ? 'neutral' : positive > negative ? 'positive' : 'negative'] += 1
    return [...(positive ? ['positive'] : []), ...(negative ? ['negative'] : [])]
  })

  const hours = Array.from({ length: 24 }, () => 0); const weekdays = Array.from({ length: 7 }, () => 0)
  for (const event of events) { const date = new Date(event.occurredAt); hours[date.getUTCHours()] += 1; weekdays[date.getUTCDay()] += 1 }
  const rhythmEvidence = evidence(events, () => ['timestamp'])

  const mediaCounts = new Map<string, number>(); const mediaEvidence = evidence(events, (event) => {
    const values = [event.metadata?.creator, event.metadata?.artist, event.metadata?.channel, event.metadata?.mediaTitle].filter((value): value is string => typeof value === 'string' && value.trim().length > 0).map((value) => value.trim())
    for (const value of values) mediaCounts.set(value, (mediaCounts.get(value) ?? 0) + 1)
    return values
  })

  const stated = new Set(events.filter((event) => event.kind === 'post' || event.kind === 'message' || event.kind === 'import-note').flatMap((event) => Object.entries(INTERESTS).flatMap(([label, terms]) => event.tokens.some((word) => terms.has(word)) ? [label] : [])))
  const observed = new Set(events.filter((event) => event.kind === 'view' || event.kind === 'listen' || event.kind === 'search' || event.kind === 'reaction').flatMap((event) => Object.entries(INTERESTS).flatMap(([label, terms]) => event.tokens.some((word) => terms.has(word)) ? [label] : [])))
  const alignment = [...new Set([...stated, ...observed])].sort().map((label) => ({ label, stated: stated.has(label), observed: observed.has(label) }))
  const alignmentEvidence = evidence(events, (event) => Object.entries(INTERESTS).flatMap(([label, terms]) => event.tokens.some((word) => terms.has(word)) ? [label] : []))

  const midpoint = events.length ? new Date((new Date(events[0].occurredAt).valueOf() + new Date(events.at(-1)!.occurredAt).valueOf()) / 2).toISOString() : generatedAt
  const halves = (rows: typeof events) => ({ early: rows.filter((event) => event.occurredAt <= midpoint).length, recent: rows.filter((event) => event.occurredAt > midpoint).length })
  const interestChange = [...interestCounts.keys()].sort().map((label) => ({ label, ...halves(events.filter((event) => event.tokens.some((word) => INTERESTS[label].has(word)))) }))
  const changeEvidence = evidence(events, (event) => Object.entries(INTERESTS).flatMap(([label, terms]) => event.tokens.some((word) => terms.has(word)) ? [label] : []))

  const localeCounts = events.reduce((out, event) => ({ ...out, [event.detectedLocale]: (out[event.detectedLocale] ?? 0) + 1 }), {} as Record<string, number>)
  const tokenCount = events.reduce((sum, event) => sum + event.tokens.length, 0); const uniqueTokens = new Set(events.flatMap((event) => event.tokens)).size
  const languageEvidence = evidence(events, (event) => event.tokens.length ? [event.detectedLocale] : [])

  const cards = [
    make('interests', 'interests', 'Interest signals', { ranked: ranked(interestCounts) }, interestEvidence),
    make('topics', 'topics', 'Repeated topics', { ranked: topicRows }, topicEvidence, ['Frequent words are lexical topics, not semantic topic-model conclusions.']),
    make('communities', 'communities', 'Community participation', { ranked: ranked(communityCounts) }, communityEvidence, ['Community names require connector metadata and may be absent from exports.']),
    make('language-style', 'language-style', 'Vocabulary and language style', { localeCounts, tokenCount, uniqueTokens, averageTokensPerEvent: events.length ? Number((tokenCount / events.length).toFixed(2)) : 0 }, languageEvidence, ['Language detection is deterministic and limited to declared locale or stop-word evidence for en/es/fr/de/pt.']),
    make('sentiment', 'sentiment', 'Sentiment distribution', { ...sentiment, supportedLocales: Object.keys(SENTIMENT).sort() }, sentimentEvidence, ['Sentiment is word-level lexical evidence; sarcasm, negation, context, and dialect can be missed.']),
    make('attention-rhythm', 'attention-rhythm', 'Attention rhythms (UTC)', { hourlyUtc: hours, weekdayUtc: weekdays }, rhythmEvidence, ['Timestamps are shown in UTC and may reflect platform logging rather than active attention.']),
    make('media-affinity', 'media-affinity', 'Media and creator affinity', { ranked: ranked(mediaCounts) }, mediaEvidence, ['Affinity counts require creator/media metadata and do not imply endorsement.']),
    make('stated-vs-observed', 'stated-vs-observed', 'Stated versus observed interests', { alignment }, alignmentEvidence, ['Posts/messages are treated as stated evidence; views/listens/searches/reactions are treated as observed attention, not preference.']),
    make('change-over-time', 'change-over-time', 'Changes over time', { midpoint, interests: interestChange }, changeEvidence, ['Early/recent windows are a deterministic midpoint split, not a causal trend.']),
  ]
  return { generatedAt: new Date(generatedAt).toISOString(), eventCount: events.length, cards, narrativeGate: { allowed: cards.every((card) => card.analyzer.narrativeReady), reason: cards.every((card) => card.analyzer.narrativeReady) ? 'All deterministic cards expose evidence and aggregates.' : 'Narrative blocked until every card has sufficient deterministic evidence.' } }
}
