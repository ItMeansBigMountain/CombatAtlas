import { useMemo, useState } from 'react'
import { Alert, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native'

import { createPrivacyClient, type ImportJob, type SourceConnection, validateArchiveSelection } from '../lib/privacyClient'

type ProfileEvidence = { source: string; sourceRecordId: string; occurredAt: string; excerpt: string }
const evidenceItems: ProfileEvidence[] = [
  { source: 'x-archive', sourceRecordId: 'tweet-1', occurredAt: '2026-08-24T01:00:00Z', excerpt: 'I am grateful for family but overwhelmed by work deadlines.' },
  { source: 'youtube', sourceRecordId: 'video-1', occurredAt: '2026-08-25T01:00:00Z', excerpt: 'Watched music production and fitness creators while thinking about data freedom.' },
]
const profile = {
  safetyBoundary: 'This profile is not a diagnosis. Validated self-report screening stays separate from observational social-media signals.',
  cards: [
    { kind: 'attention', title: 'Attention clusters: music, fitness, data', summary: 'Your imported events point toward music production, fitness, and data freedom.', confidence: 'medium', evidence: evidenceItems },
    { kind: 'language', title: 'Language balance', summary: 'Both constructive and strain language appear in this small slice.', confidence: 'low', evidence: evidenceItems.slice(0, 1) },
    { kind: 'wellbeing-pattern', title: 'Non-diagnostic wellbeing pattern', summary: 'Some language contains stress signals; use this as a reflection prompt, not a medical conclusion.', confidence: 'low', evidence: evidenceItems.slice(0, 1) },
  ],
} as const

const initialSources: SourceConnection[] = [
  { id: 'youtube', name: 'Google / YouTube', coverage: 'Recent API activity; Takeout adds archive history.', status: 'available', method: 'oauth' },
  { id: 'reddit', name: 'Reddit', coverage: 'Official API history within provider limits.', status: 'available', method: 'oauth' },
  { id: 'x', name: 'X', coverage: 'Official archive recommended; API access is paid and incomplete.', status: 'available', method: 'archive' },
]

const operationsChecklist = [
  { label: 'Observability', status: 'planned', detail: 'Sentry/OpenTelemetry IDs only; no raw posts, tokens, prompts, filenames, or archive text in telemetry.' },
  { label: 'Backups and restore', status: 'blocked', detail: 'Needs a real restore drill proving deletion keys, exports, queues, caches, and backup retention reconcile.' },
  { label: 'Incident response', status: 'planned', detail: 'Privacy/security runbook is drafted; on-call, severity, notification, and regulator timelines must be rehearsed.' },
  { label: 'Cost controls', status: 'planned', detail: 'Closed beta has hard caps for API quota, archive jobs, storage, and model calls before any public launch.' },
  { label: 'Closed beta', status: 'blocked', detail: 'Only synthetic or explicitly consented fixtures; TestFlight/Internal-track evidence is still required.' },
] as const

type Section = 'sources' | 'profile' | 'privacy' | 'ops'

function ActionButton({ label, onPress, danger = false, disabled = false }: { label: string; onPress: () => void; danger?: boolean; disabled?: boolean }) {
  return <Pressable accessibilityRole="button" accessibilityState={{ disabled }} disabled={disabled} onPress={onPress} style={({ pressed }) => [styles.button, danger && styles.dangerButton, disabled && styles.disabled, pressed && styles.pressed]}><Text style={styles.buttonText}>{label}</Text></Pressable>
}

export default function HomeScreen() {
  const client = useMemo(createPrivacyClient, [])
  const [section, setSection] = useState<Section>('sources')
  const [consented, setConsented] = useState(false)
  const [sources, setSources] = useState(initialSources)
  const [job, setJob] = useState<ImportJob | null>(null)
  const [evidence, setEvidence] = useState<ProfileEvidence[] | null>(null)
  const [notice, setNotice] = useState('Your data stays under your control.')

  const connect = async (id: string) => {
    if (!consented) return setNotice('Review and accept the specific analysis consent first.')
    const source = sources.find((item) => item.id === id)
    if (!source) return
    if (source.method === 'archive') return chooseArchive()
    setNotice(`OAuth will open in your browser and return to ${client.oauthRedirectUri}. Tokens are never exposed to analytics.`)
    setSources((items) => items.map((item) => item.id === id ? { ...item, status: 'connected' } : item))
  }

  const chooseArchive = async () => {
    if (!consented) return setNotice('Archive analysis requires explicit consent first.')
    const file = await client.chooseArchive()
    if (!file) return
    const error = validateArchiveSelection(file)
    if (error) return setNotice(error)
    setJob({ id: `local-${Date.now()}`, fileName: file.name, progress: 15, status: 'uploading', message: 'Encrypted upload queued. Server-side malware and archive checks are required.' })
    setNotice('Archive selected. Closing this screen will not grant broader access.')
  }

  const revoke = (id: string) => {
    setSources((items) => items.map((item) => item.id === id ? { ...item, status: 'revoked' } : item))
    setNotice('Source revoked. New ingestion stopped; deletion reconciliation is queued for derived data and backups.')
  }

  const confirmDestructive = (kind: 'delete' | 'revoke all') => Alert.alert(
    kind === 'delete' ? 'Delete account and data?' : 'Revoke every source?',
    'This requires step-up authentication. Deletion remains pending until descendants, caches, exports, and backup retention are reconciled.',
    [{ text: 'Cancel', style: 'cancel' }, { text: 'Continue', style: 'destructive', onPress: () => setNotice(`${kind} request queued; a completion receipt will appear after reconciliation.`) }],
  )

  return <View style={styles.root}>
    <ScrollView contentContainerStyle={styles.page}>
      <Text style={styles.eyebrow}>tweetBetweenTheLines</Text>
      <Text accessibilityRole="header" style={styles.title}>Your data. Your evidence. Your call.</Text>
      <Text style={styles.body}>Connect only the sources you choose, inspect why every reflection appears, correct it, or erase it.</Text>

      <View accessibilityLiveRegion="polite" style={styles.notice}><Text style={styles.noticeText}>{notice}</Text></View>

      <View accessibilityRole="tablist" style={styles.tabs}>
        {(['sources', 'profile', 'privacy', 'ops'] as Section[]).map((item) => <Pressable key={item} accessibilityRole="tab" accessibilityState={{ selected: section === item }} onPress={() => setSection(item)} style={[styles.tab, section === item && styles.activeTab]}><Text style={styles.tabText}>{item}</Text></Pressable>)}
      </View>

      {section === 'sources' && <>
        <View style={styles.panel}>
          <Text accessibilityRole="header" style={styles.panelTitle}>Consent before collection</Text>
          <Text style={styles.body}>Purpose: build explainable personal reflections. Categories: posts, viewing/listening activity, reactions, and account metadata. Retention: until you revoke or delete. No sale, ads, diagnosis, or silent scope expansion.</Text>
          <Pressable accessibilityRole="checkbox" accessibilityState={{ checked: consented }} onPress={() => setConsented((value) => !value)} style={styles.checkRow}><View style={[styles.checkbox, consented && styles.checked]} /><Text style={styles.checkText}>I choose to allow this analysis. I can withdraw consent at any time.</Text></Pressable>
        </View>
        <View style={styles.panel}>
          <Text accessibilityRole="header" style={styles.panelTitle}>Source coverage dashboard</Text>
          <Text style={styles.body}>Coverage is intentionally conservative: “connected” means this app has a consented OAuth handoff or official archive selected, not that the platform provides complete history.</Text>
          <Text style={styles.meta}>Available now: YouTube/Reddit OAuth handoff contracts and X official archive import. Restricted/roadmap platforms stay unlisted in the active connector UI until verified.</Text>
        </View>
        {sources.map((source) => <View key={source.id} style={styles.card}>
          <View style={styles.row}><Text style={styles.cardTitle}>{source.name}</Text><Text style={styles.badge}>{source.status}</Text></View>
          <Text style={styles.body}>{source.coverage}</Text>
          <Text style={styles.meta}>{source.method === 'oauth' ? `Browser OAuth + mobile PKCE · ${client.platform}` : 'Official archive import'}</Text>
          <View style={styles.actions}><ActionButton label={source.method === 'oauth' ? 'Connect' : 'Choose archive'} onPress={() => void connect(source.id)} disabled={source.status === 'revoked'} />{source.status === 'connected' && <ActionButton label="Revoke" danger onPress={() => revoke(source.id)} />}</View>
        </View>)}
        <ActionButton label="Import another official archive" onPress={() => void chooseArchive()} />
        {job && <View style={styles.panel} accessible accessibilityLabel={`Import ${job.progress} percent complete`}><Text style={styles.panelTitle}>{job.fileName}</Text><View style={styles.track}><View style={[styles.progress, { width: `${job.progress}%` }]} /></View><Text style={styles.meta}>{job.progress}% · {job.message}</Text></View>}
      </>}

      {section === 'profile' && <>
        <Text style={styles.safety}>{profile.safetyBoundary}</Text>
        {profile.cards.map((card) => <View key={card.kind} style={styles.card}>
          <Text style={styles.kind}>{card.kind}</Text><Text style={styles.cardTitle}>{card.title}</Text><Text style={styles.body}>{card.summary}</Text><Text style={styles.meta}>{card.confidence} confidence · {card.evidence.length} evidence item(s)</Text>
          <View style={styles.actions}><ActionButton label="See evidence" onPress={() => setEvidence(card.evidence)} /><ActionButton label="Correct this" onPress={() => setNotice('Correction opened. The original and your correction remain distinguishable in provenance.')} /></View>
        </View>)}
        {evidence && <View style={styles.panel}><Text accessibilityRole="header" style={styles.panelTitle}>Evidence behind this reflection</Text>{evidence.length ? evidence.map((item) => <View key={`${item.source}:${item.sourceRecordId}`} style={styles.evidence}><Text style={styles.meta}>{item.source} · {item.occurredAt.slice(0, 10)}</Text><Text style={styles.body}>{item.excerpt}</Text></View>) : <Text style={styles.body}>No supporting evidence. This reflection should abstain.</Text>}<ActionButton label="Close evidence" onPress={() => setEvidence(null)} /></View>}
        <View style={styles.crisis}><Text style={styles.crisisTitle}>Need immediate support?</Text><Text style={styles.body}>These reflections are not medical advice. If you may hurt yourself or someone else, contact local emergency services now. In the U.S. or Canada, call or text 988.</Text></View>
      </>}

      {section === 'privacy' && <>
        <View style={styles.panel}><Text style={styles.panelTitle}>Platform privacy</Text><Text style={styles.body}>{Platform.OS === 'web' ? 'Web sessions use server-managed secure, HttpOnly cookies; provider tokens never enter browser storage.' : 'Native session references use this device’s Keychain/Keystore. Provider tokens stay server-side.'}</Text><Text style={styles.meta}>Analytics is opt-in. Notifications are off until requested in context. No contacts, precise location, microphone, camera, or tracking permission is requested.</Text></View>
        <ActionButton label="Download my data" onPress={() => setNotice('Step-up authentication required. A signed export job will be queued.')} />
        <ActionButton label="Revoke all sources" danger onPress={() => confirmDestructive('revoke all')} />
        <ActionButton label="Delete account and data" danger onPress={() => confirmDestructive('delete')} />
      </>}

      {section === 'ops' && <>
        <View style={styles.panel}>
          <Text accessibilityRole="header" style={styles.panelTitle}>Production and closed-beta readiness</Text>
          <Text style={styles.body}>This screen tracks operational truth for testers. Web, iOS, and Android bundles can be exported locally, but signed deployment, device evidence, TestFlight, Android internal testing, monitoring, and restore drills are still release gates.</Text>
        </View>
        {operationsChecklist.map((item) => <View key={item.label} style={styles.card}>
          <View style={styles.row}><Text style={styles.cardTitle}>{item.label}</Text><Text style={[styles.badge, item.status === 'blocked' && styles.blockedBadge]}>{item.status}</Text></View>
          <Text style={styles.body}>{item.detail}</Text>
        </View>)}
        <View style={styles.crisis}><Text style={styles.crisisTitle}>No diagnosis claims</Text><Text style={styles.body}>Closed beta copy may describe source-backed reflections and uncertainty only. It must not claim diagnosis, crisis prediction, or complete platform coverage.</Text></View>
      </>}
    </ScrollView>
  </View>
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#07111f' }, page: { width: '100%', maxWidth: 760, alignSelf: 'center', gap: 16, padding: 20, paddingTop: 54, paddingBottom: 80 },
  eyebrow: { color: '#67e8f9', fontSize: 13, fontWeight: '800', letterSpacing: 1.4, textTransform: 'uppercase' }, title: { color: '#f8fafc', fontSize: 34, fontWeight: '900', lineHeight: 40 }, body: { color: '#cbd5e1', fontSize: 16, lineHeight: 24 },
  notice: { backgroundColor: '#0c4a6e', borderRadius: 12, padding: 12 }, noticeText: { color: '#e0f2fe', fontSize: 14, lineHeight: 20 }, tabs: { flexDirection: 'row', gap: 8 }, tab: { flex: 1, borderColor: '#334155', borderWidth: 1, borderRadius: 12, padding: 12, alignItems: 'center' }, activeTab: { backgroundColor: '#155e75', borderColor: '#67e8f9' }, tabText: { color: '#f8fafc', fontWeight: '700', textTransform: 'capitalize' },
  panel: { gap: 12, padding: 18, borderRadius: 20, backgroundColor: '#10213a', borderColor: '#1e40af', borderWidth: 1 }, panelTitle: { color: '#f8fafc', fontSize: 20, fontWeight: '800' }, card: { gap: 10, padding: 18, borderRadius: 18, backgroundColor: '#111827', borderColor: '#334155', borderWidth: 1 }, cardTitle: { color: '#f8fafc', fontSize: 18, fontWeight: '800', flexShrink: 1 }, row: { flexDirection: 'row', justifyContent: 'space-between', gap: 12 }, badge: { color: '#a5f3fc', fontSize: 12, fontWeight: '800', textTransform: 'uppercase' }, meta: { color: '#94a3b8', fontSize: 13, lineHeight: 19 }, kind: { color: '#67e8f9', fontSize: 12, fontWeight: '800', letterSpacing: 1, textTransform: 'uppercase' },
  actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 }, button: { minHeight: 44, justifyContent: 'center', backgroundColor: '#0369a1', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10 }, dangerButton: { backgroundColor: '#991b1b' }, buttonText: { color: '#fff', fontWeight: '800' }, pressed: { opacity: 0.75 }, disabled: { opacity: 0.45 }, checkRow: { flexDirection: 'row', gap: 12, alignItems: 'flex-start', minHeight: 44 }, checkbox: { width: 24, height: 24, borderRadius: 5, borderWidth: 2, borderColor: '#67e8f9' }, checked: { backgroundColor: '#0891b2' }, checkText: { color: '#f1f5f9', flex: 1, lineHeight: 22 }, blockedBadge: { color: '#fecaca' },
  safety: { color: '#fde68a', fontSize: 14, lineHeight: 21 }, evidence: { borderTopColor: '#334155', borderTopWidth: 1, paddingTop: 10, gap: 4 }, track: { height: 10, overflow: 'hidden', borderRadius: 5, backgroundColor: '#334155' }, progress: { height: '100%', backgroundColor: '#22d3ee' }, crisis: { gap: 8, padding: 18, borderRadius: 18, borderColor: '#f59e0b', borderWidth: 1, backgroundColor: '#451a03' }, crisisTitle: { color: '#fef3c7', fontSize: 18, fontWeight: '800' },
})