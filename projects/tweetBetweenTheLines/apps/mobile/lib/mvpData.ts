import {
  buildExplainableMetrics,
  type ExplainableMetricsSnapshot,
  type MetricEvent,
} from '../../../packages/domain/src/explainableMetrics'

export type MvpDataset = {
  label: string
  consent: 'synthetic-demo' | 'user-import'
  events: MetricEvent[]
}

export const syntheticDataset: MvpDataset = {
  label: 'Synthetic demo — no personal account data',
  consent: 'synthetic-demo',
  events: [
    { id: 'demo:x:1', sourceId: 'synthetic-x-archive', sourceRecordId: 'tweet-1', occurredAt: '2026-08-01T08:15:00Z', kind: 'post', content: 'I love music production and learning software with my community.', locale: 'en', metadata: { community: 'makers' } },
    { id: 'demo:x:2', sourceId: 'synthetic-x-archive', sourceRecordId: 'tweet-2', occurredAt: '2026-08-03T19:45:00Z', kind: 'post', content: 'Fitness training felt great today; grateful for friends.', locale: 'en', metadata: { community: 'fitness-club' } },
    { id: 'demo:yt:1', sourceId: 'synthetic-youtube-takeout', sourceRecordId: 'watch-1', occurredAt: '2026-08-07T21:10:00Z', kind: 'view', content: 'Music production workflow and software tools', locale: 'en', metadata: { channel: 'Example Creator', mediaTitle: 'Music production workflow' } },
    { id: 'demo:yt:2', sourceId: 'synthetic-youtube-takeout', sourceRecordId: 'watch-2', occurredAt: '2026-08-10T06:30:00Z', kind: 'view', content: 'Running workout and fitness training basics', locale: 'en', metadata: { channel: 'Example Fitness', mediaTitle: 'Running basics' } },
    { id: 'demo:reddit:1', sourceId: 'synthetic-reddit-export', sourceRecordId: 'comment-1', occurredAt: '2026-08-12T23:05:00Z', kind: 'message', content: 'Learning programming is exciting, but deadlines made me stressed and tired.', locale: 'en', metadata: { subreddit: 'learnprogramming' } },
    { id: 'demo:yt:3', sourceId: 'synthetic-youtube-takeout', sourceRecordId: 'search-1', occurredAt: '2026-08-18T17:20:00Z', kind: 'search', content: 'calm music playlist for coding', locale: 'en' },
  ],
}

const eventKinds = new Set<MetricEvent['kind']>(['post', 'message', 'reaction', 'view', 'listen', 'search', 'import-note'])

export function parseDatasetJson(text: string): MvpDataset {
  const parsed: unknown = JSON.parse(text)
  const root = Array.isArray(parsed) ? { events: parsed } : parsed
  if (!root || typeof root !== 'object' || !Array.isArray((root as { events?: unknown }).events)) {
    throw new Error('Expected a JSON array of events or an object with an events array.')
  }
  const rows = (root as { events: unknown[]; label?: unknown }).events
  const events = rows.map((row, index): MetricEvent => {
    if (!row || typeof row !== 'object') throw new Error(`Event ${index + 1} must be an object.`)
    const item = row as Record<string, unknown>
    const required = (key: string) => {
      const value = item[key]
      if (typeof value !== 'string' || !value.trim()) throw new Error(`Event ${index + 1} requires ${key}.`)
      return value.trim()
    }
    const kind = required('kind')
    if (!eventKinds.has(kind as MetricEvent['kind'])) throw new Error(`Event ${index + 1} has unsupported kind ${kind}.`)
    const metadata = item.metadata
    if (metadata !== undefined && (!metadata || typeof metadata !== 'object' || Array.isArray(metadata))) throw new Error(`Event ${index + 1} metadata must be an object.`)
    return {
      id: required('id'), sourceId: required('sourceId'), sourceRecordId: required('sourceRecordId'),
      occurredAt: new Date(required('occurredAt')).toISOString(), kind: kind as MetricEvent['kind'], content: required('content'),
      locale: typeof item.locale === 'string' ? item.locale : null,
      metadata: metadata as MetricEvent['metadata'],
    }
  })
  if (!events.length) throw new Error('The archive contains no events to analyze.')
  return { label: typeof (root as { label?: unknown }).label === 'string' ? (root as { label: string }).label : 'Consented JSON import', consent: 'user-import', events }
}

export function analyzeDataset(dataset: MvpDataset): ExplainableMetricsSnapshot {
  return buildExplainableMetrics(dataset.events, new Date().toISOString())
}
