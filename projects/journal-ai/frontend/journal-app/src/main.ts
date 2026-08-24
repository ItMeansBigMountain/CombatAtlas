import './style.css'
import { analyzeJournalEntry, type JournalAnalysis, type Mood } from './journalAnalysis'
import { escapeUserText } from './safeText'
import {
  confidenceLabel, createMeetingJob, editSegment, failJob, provisionalSpeaker, retryJob, transitionJob,
  type MeetingJob, type RetentionPolicy, type TranscriptSegment,
} from './meetingWorkflow'
import {
  approveArtifact, buildDraftArtifacts, createArtifactStore, deleteArtifact, exportArtifact,
  type ArtifactStore, type MeetingArtifact,
} from './meetingIntelligence'

type SavedEntry = {
  id: number
  text: string
  mood: Mood
  analysis: JournalAnalysis
  createdAt: string
}

const moods: { value: Mood; label: string; emoji: string }[] = [
  { value: 'calm', label: 'Calm', emoji: '😌' },
  { value: 'happy', label: 'Happy', emoji: '🙂' },
  { value: 'anxious', label: 'Anxious', emoji: '😟' },
  { value: 'sad', label: 'Sad', emoji: '😔' },
  { value: 'angry', label: 'Angry', emoji: '😤' },
  { value: 'tired', label: 'Tired', emoji: '🥱' },
]

const starterEntries = [
  'I feel anxious about work deadlines, but I am grateful that a walk helped me calm down.',
  'I felt proud after calling my family and finishing the small task I kept avoiding.',
]

const app = document.querySelector<HTMLDivElement>('#app')

if (!app) {
  throw new Error('App root not found')
}

app.innerHTML = `
  <main class="shell">
    <section class="hero-card" aria-labelledby="app-title">
      <p class="eyebrow">Local-first demo • no paid API keys</p>
      <h1 id="app-title">Journal AI</h1>
      <p class="lede">Write a quick check-in, choose your mood, and get a simple reflection you can act on today.</p>
      <div class="hero-actions">
        <a class="button primary" href="#journal-flow">Start journaling</a>
        <a class="button ghost" href="#analysis-panel">See analysis</a>
      </div>
    </section>

    <section id="journal-flow" class="panel grid-panel" aria-label="Journal entry workflow">
      <form id="journal-form" class="entry-card">
        <div class="section-heading">
          <p class="eyebrow">Step 1</p>
          <h2>Capture the entry</h2>
        </div>
        <label for="entry-text">Journal entry</label>
        <textarea id="entry-text" name="entry" rows="9" placeholder="What happened today? What did you feel? What do you want to do next?" required></textarea>

        <fieldset>
          <legend>Step 2: pick your mood signal</legend>
          <div class="mood-grid">
            ${moods
              .map(
                (mood, index) => `
                  <label class="mood-option">
                    <input type="radio" name="mood" value="${mood.value}" ${index === 0 ? 'checked' : ''} />
                    <span>${mood.emoji}</span>
                    ${mood.label}
                  </label>
                `,
              )
              .join('')}
          </div>
        </fieldset>

        <div class="form-actions">
          <button class="button primary" type="submit">Analyze entry</button>
          <button class="button ghost" id="load-sample" type="button">Load sample</button>
        </div>
      </form>

      <aside id="analysis-panel" class="analysis-card" aria-live="polite">
        <div class="section-heading">
          <p class="eyebrow">Step 3</p>
          <h2>Reflection result</h2>
        </div>
        <div id="empty-state" class="empty-state">
          <p>Submit an entry to see tone, signals, a reflection prompt, and one next step.</p>
        </div>
        <div id="analysis-result" class="analysis-result hidden"></div>
      </aside>
    </section>

    <section id="meeting-flow" class="panel meeting-panel" aria-labelledby="meeting-title">
      <div class="section-heading">
        <p class="eyebrow">Private meeting capture</p>
        <h2 id="meeting-title">Record only with everyone’s permission</h2>
        <p class="muted">Recording never starts in the background. Audio stays in this browser demo, is encrypted in memory, and is not uploaded to a cloud service.</p>
      </div>
      <div class="meeting-grid">
        <div class="meeting-controls">
          <label class="consent-check"><input id="meeting-consent" type="checkbox" /> I confirm every participant has agreed to this recording or import.</label>
          <label for="retention-policy">Encrypted raw audio retention</label>
          <select id="retention-policy"><option value="delete-after-transcription">Delete after transcription (recommended)</option><option value="keep-24-hours">Keep for 24 hours</option><option value="keep-until-deleted">Keep until I delete it</option></select>
          <div class="form-actions"><button id="record-meeting" class="button primary" type="button" disabled>Start visible recording</button><label class="button ghost file-button">Import audio<input id="meeting-file" type="file" accept="audio/*" disabled /></label></div>
          <div id="recording-indicator" class="recording-indicator hidden" role="status">● Recording is active — tell participants and keep this page visible.</div>
          <p id="meeting-message" class="muted" aria-live="polite">Consent is required before recording or importing audio.</p>
        </div>
        <div id="meeting-job" class="job-card empty-state"><p>No private processing job yet.</p></div>
      </div>
      <div id="transcript-review" class="transcript-review hidden" aria-live="polite"></div>
      <div id="meeting-insights" class="transcript-review hidden" aria-live="polite"></div>
    </section>

    <section class="panel history-panel" aria-labelledby="history-title">
      <div class="section-heading">
        <p class="eyebrow">Local demo history</p>
        <h2 id="history-title">Recent check-ins</h2>
      </div>
      <div id="entry-history" class="entry-history"></div>
    </section>
  </main>
`

const form = document.querySelector<HTMLFormElement>('#journal-form')!
const textarea = document.querySelector<HTMLTextAreaElement>('#entry-text')!
const loadSampleButton = document.querySelector<HTMLButtonElement>('#load-sample')!
const emptyState = document.querySelector<HTMLDivElement>('#empty-state')!
const resultPanel = document.querySelector<HTMLDivElement>('#analysis-result')!
const historyPanel = document.querySelector<HTMLDivElement>('#entry-history')!
const entries: SavedEntry[] = []
let sampleIndex = 0

function getSelectedMood(): Mood {
  const checked = document.querySelector<HTMLInputElement>('input[name="mood"]:checked')
  return (checked?.value as Mood | undefined) ?? 'calm'
}

function renderSignals(analysis: JournalAnalysis) {
  if (analysis.signals.length === 0) {
    return '<p class="muted">No strong signals yet. Add more detail to sharpen the reflection.</p>'
  }

  return `
    <div class="signal-list">
      ${analysis.signals
        .map(
          (signal) => `
            <div class="signal-pill">
              <strong>${signal.label}</strong>
              <span>${signal.evidence.join(', ')}</span>
            </div>
          `,
        )
        .join('')}
    </div>
  `
}

function renderAnalysis(entry: SavedEntry) {
  emptyState.classList.add('hidden')
  resultPanel.classList.remove('hidden')
  resultPanel.innerHTML = `
    <div class="tone-row">
      <span class="mood-badge">${entry.mood}</span>
      <span class="tone-badge">${entry.analysis.tone}</span>
    </div>
    <h3>${entry.analysis.summary}</h3>
    ${renderSignals(entry.analysis)}
    <div class="prompt-card">
      <p class="label">Reflection prompt</p>
      <p>${entry.analysis.reflectionPrompt}</p>
    </div>
    <div class="prompt-card next-step">
      <p class="label">Next step</p>
      <p>${entry.analysis.nextStep}</p>
    </div>
  `
}

function renderHistory() {
  if (entries.length === 0) {
    historyPanel.innerHTML = '<p class="muted">No saved demo entries yet.</p>'
    return
  }

  historyPanel.innerHTML = entries
    .map(
      (entry) => `
        <article class="history-item">
          <div>
            <strong>${entry.mood} • ${entry.analysis.tone}</strong>
            <p>${escapeUserText(entry.text.slice(0, 130))}${entry.text.length > 130 ? '…' : ''}</p>
          </div>
          <time>${entry.createdAt}</time>
        </article>
      `,
    )
    .join('')
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  const text = textarea.value
  const mood = getSelectedMood()
  const analysis = analyzeJournalEntry({ text, mood })
  const entry: SavedEntry = {
    id: Date.now(),
    text: text.trim(),
    mood,
    analysis,
    createdAt: new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date()),
  }

  entries.unshift(entry)
  renderAnalysis(entry)
  renderHistory()
})

loadSampleButton.addEventListener('click', () => {
  textarea.value = starterEntries[sampleIndex % starterEntries.length]
  sampleIndex += 1
  textarea.focus()
})

renderHistory()

const consentInput = document.querySelector<HTMLInputElement>('#meeting-consent')!
const retentionSelect = document.querySelector<HTMLSelectElement>('#retention-policy')!
const recordButton = document.querySelector<HTMLButtonElement>('#record-meeting')!
const fileInput = document.querySelector<HTMLInputElement>('#meeting-file')!
const recordingIndicator = document.querySelector<HTMLDivElement>('#recording-indicator')!
const meetingMessage = document.querySelector<HTMLParagraphElement>('#meeting-message')!
const jobPanel = document.querySelector<HTMLDivElement>('#meeting-job')!
const transcriptReview = document.querySelector<HTMLDivElement>('#transcript-review')!
const meetingInsights = document.querySelector<HTMLDivElement>('#meeting-insights')!
const encryptedAudio = new Map<string, { cipher: ArrayBuffer; expiresAt: number | null }>()
let currentJob: MeetingJob | null = null
let artifactStore: ArtifactStore = createArtifactStore([])
let recorder: MediaRecorder | null = null
let recordingStream: MediaStream | null = null
let chunks: Blob[] = []

function escapeHtml(value: string) {
  const node = document.createElement('div')
  node.textContent = value
  return node.innerHTML
}

async function encryptAudio(jobId: string, blob: Blob, retention: RetentionPolicy) {
  const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, false, ['encrypt'])
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const cipher = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, await blob.arrayBuffer())
  encryptedAudio.set(jobId, { cipher, expiresAt: retention === 'keep-24-hours' ? Date.now() + 86_400_000 : null })
}

function renderJob() {
  if (!currentJob) return
  const job = currentJob
  jobPanel.className = 'job-card'
  jobPanel.innerHTML = `<div class="job-heading"><strong>${escapeHtml(job.fileName)}</strong><span class="state-badge">${job.state.replace('_', ' ')}</span></div><progress max="100" value="${job.progress}">${job.progress}%</progress><p class="muted">Local-first job • attempt ${job.attempts} • AES-GCM encrypted • ${job.retention.replaceAll('-', ' ')}</p>${job.error ? `<p class="error-message">Processing stopped: ${escapeHtml(job.error)}</p>` : ''}<div class="form-actions">${['queued', 'normalizing', 'transcribing', 'diarizing'].includes(job.state) ? '<button id="cancel-job" class="button ghost" type="button">Cancel processing</button>' : ''}${['failed', 'cancelled'].includes(job.state) ? '<button id="retry-job" class="button primary" type="button">Retry locally</button>' : ''}${encryptedAudio.has(job.id) ? '<button id="delete-audio" class="button danger" type="button">Delete raw audio now</button>' : ''}</div>`
  document.querySelector<HTMLButtonElement>('#cancel-job')?.addEventListener('click', () => { if (currentJob) { currentJob = transitionJob(currentJob, 'cancelled'); renderJob() } })
  document.querySelector<HTMLButtonElement>('#retry-job')?.addEventListener('click', () => { if (currentJob) { currentJob = retryJob(currentJob); renderJob(); void runLocalPipeline() } })
  document.querySelector<HTMLButtonElement>('#delete-audio')?.addEventListener('click', () => { if (currentJob) { encryptedAudio.delete(currentJob.id); meetingMessage.textContent = 'Encrypted raw audio deleted. The transcript remains separate.'; renderJob() } })
}

function renderTranscript() {
  if (!currentJob || currentJob.state !== 'needs_review') return
  transcriptReview.classList.remove('hidden')
  transcriptReview.innerHTML = `<div class="section-heading"><p class="eyebrow">Human review required</p><h3>Correct words and provisional speakers</h3><p class="muted">No names are inferred. Rename a speaker only when you know who spoke.</p></div>${currentJob.segments.map((segment) => `<div class="segment-row" data-segment="${segment.id}"><label>Speaker label<input class="speaker-input" value="${escapeHtml(segment.speakerLabel)}" /></label><label>Transcript<textarea class="segment-input" rows="2">${escapeHtml(segment.text)}</textarea></label><span class="confidence ${segment.confidence !== null && segment.confidence < 0.6 ? 'uncertain' : ''}">${confidenceLabel(segment.confidence)}</span></div>`).join('')}<div class="form-actions"><button id="approve-transcript" class="button primary" type="button">Approve reviewed transcript</button></div>`
  document.querySelector<HTMLButtonElement>('#approve-transcript')!.addEventListener('click', () => {
    if (!currentJob) return
    const segments = currentJob.segments.map((segment) => {
      const row = document.querySelector<HTMLElement>(`[data-segment="${segment.id}"]`)!
      return editSegment(segment, { text: row.querySelector<HTMLTextAreaElement>('.segment-input')!.value, speakerLabel: row.querySelector<HTMLInputElement>('.speaker-input')!.value })
    })
    currentJob = transitionJob({ ...currentJob, segments }, 'completed')
    transcriptReview.innerHTML = '<p class="success-message">Transcript approved. No speaker identity was assigned automatically.</p>'
    artifactStore = createArtifactStore(buildDraftArtifacts(currentJob.id, segments))
    renderMeetingInsights()
    renderJob()
  })
}

function downloadArtifact(item: MeetingArtifact) {
  const url = URL.createObjectURL(new Blob([exportArtifact(artifactStore, item.id, 'json')], { type: 'application/json' }))
  const link = document.createElement('a')
  link.href = url
  link.download = `${item.kind}-${item.id}.json`
  link.click()
  URL.revokeObjectURL(url)
}

function renderMeetingInsights() {
  meetingInsights.classList.remove('hidden')
  meetingInsights.innerHTML = `<div class="section-heading"><p class="eyebrow">Review before saving</p><h3>Review meeting intelligence</h3><p class="muted">Every draft cites reviewed transcript segments. Recurring themes describe topics, not a diagnosis of anyone.</p></div><div class="form-actions"><button id="add-private-reflection" class="button ghost" type="button">Add private reflection</button></div>${artifactStore.artifacts.length ? artifactStore.artifacts.map((item) => `<article class="history-item" data-artifact="${item.id}"><div><strong>${escapeHtml(item.kind.replaceAll('_', ' '))} • ${item.status}${item.private ? ' • private' : ''}</strong><p>${escapeHtml(item.text)}</p><small>Sources: ${item.citations.map(escapeHtml).join(', ')}</small></div><div class="form-actions">${item.status === 'draft' ? '<button class="approve-artifact button primary" type="button">Approve</button>' : ''}<button class="export-artifact button ghost" type="button">Export JSON</button><button class="delete-artifact button danger" type="button">Delete artifact</button></div></article>`).join('') : '<p class="muted">No meeting artifacts remain.</p>'}`

  document.querySelector<HTMLButtonElement>('#add-private-reflection')?.addEventListener('click', () => {
    if (!currentJob) return
    const text = window.prompt('Write a private reflection. It stays separate from the meeting record.')?.trim()
    if (!text) return
    const reflection: MeetingArtifact = { id: `${currentJob.id}-private-${crypto.randomUUID()}`, meetingId: currentJob.id, kind: 'private_reflection', text, citations: currentJob.segments.map((segment) => segment.id), status: 'draft', private: true }
    artifactStore = { artifacts: [...artifactStore.artifacts, reflection] }
    renderMeetingInsights()
  })
  document.querySelectorAll<HTMLElement>('[data-artifact]').forEach((row) => {
    const id = row.dataset.artifact!
    row.querySelector<HTMLButtonElement>('.approve-artifact')?.addEventListener('click', () => { artifactStore = approveArtifact(artifactStore, id); renderMeetingInsights() })
    row.querySelector<HTMLButtonElement>('.export-artifact')?.addEventListener('click', () => { const item = artifactStore.artifacts.find((candidate) => candidate.id === id); if (item) downloadArtifact(item) })
    row.querySelector<HTMLButtonElement>('.delete-artifact')?.addEventListener('click', () => { artifactStore = deleteArtifact(artifactStore, id); renderMeetingInsights() })
  })
}

async function runLocalPipeline() {
  if (!currentJob) return
  try {
    for (const state of ['normalizing', 'transcribing', 'diarizing'] as const) {
      await new Promise((resolve) => setTimeout(resolve, 260))
      if (!currentJob || currentJob.state === 'cancelled') return
      currentJob = transitionJob(currentJob, state)
      renderJob()
    }
    await new Promise((resolve) => setTimeout(resolve, 260))
    if (!currentJob || currentJob.state === 'cancelled') return
    const segments: TranscriptSegment[] = [{ id: 'segment-1', startSeconds: 0, endSeconds: 4.2, text: '[Connect an installed local Whisper adapter to replace this placeholder.]', speakerLabel: provisionalSpeaker(0), confidence: 0.52, userEdited: false }]
    currentJob = transitionJob({ ...currentJob, segments }, 'needs_review')
    if (currentJob.retention === 'delete-after-transcription') encryptedAudio.delete(currentJob.id)
    renderJob()
    renderTranscript()
  } catch {
    if (currentJob && currentJob.state !== 'cancelled') { currentJob = failJob(currentJob, 'LOCAL_ADAPTER_ERROR'); renderJob() }
  }
}

async function queueAudio(blob: Blob, fileName: string) {
  if (!consentInput.checked) return
  const retention = retentionSelect.value as RetentionPolicy
  currentJob = createMeetingJob({ id: crypto.randomUUID(), fileName, retention, consentedAt: new Date().toISOString() })
  transcriptReview.classList.add('hidden')
  meetingInsights.classList.add('hidden')
  artifactStore = createArtifactStore([])
  await encryptAudio(currentJob.id, blob, retention)
  meetingMessage.textContent = 'Audio encrypted locally. Processing can be cancelled or retried.'
  renderJob()
  await runLocalPipeline()
}

consentInput.addEventListener('change', () => {
  recordButton.disabled = !consentInput.checked
  fileInput.disabled = !consentInput.checked
  meetingMessage.textContent = consentInput.checked ? 'Consent attested. Record visibly or choose an audio file.' : 'Consent is required before recording or importing audio.'
})

fileInput.addEventListener('change', () => {
  const file = fileInput.files?.[0]
  if (!file || !file.type.startsWith('audio/')) { meetingMessage.textContent = 'Choose a supported audio file.'; return }
  void queueAudio(file, file.name)
})

recordButton.addEventListener('click', async () => {
  if (recorder?.state === 'recording') {
    recorder.stop(); recordingStream?.getTracks().forEach((track) => track.stop())
    recordingIndicator.classList.add('hidden'); recordButton.textContent = 'Start visible recording'
    return
  }
  try {
    recordingStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    chunks = []; recorder = new MediaRecorder(recordingStream)
    recorder.addEventListener('dataavailable', (event) => chunks.push(event.data))
    recorder.addEventListener('stop', () => { const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' }); void queueAudio(blob, `meeting-${new Date().toISOString().slice(0, 19)}.webm`) })
    recorder.start(); recordingIndicator.classList.remove('hidden'); recordButton.textContent = 'Stop recording'
  } catch { meetingMessage.textContent = 'Microphone access was unavailable. No recording was created.' }
})
