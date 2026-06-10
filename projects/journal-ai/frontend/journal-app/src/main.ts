import './style.css'
import { analyzeJournalEntry, type JournalAnalysis, type Mood } from './journalAnalysis'

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
            <p>${entry.text.slice(0, 130)}${entry.text.length > 130 ? '…' : ''}</p>
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
