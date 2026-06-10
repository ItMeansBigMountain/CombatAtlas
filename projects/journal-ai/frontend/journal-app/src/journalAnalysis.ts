export type Mood = 'calm' | 'happy' | 'anxious' | 'sad' | 'angry' | 'tired'

export type JournalEntryInput = {
  text: string
  mood: Mood
}

export type JournalSignal = {
  label: string
  score: number
  evidence: string[]
}

export type JournalAnalysis = {
  mood: Mood
  tone: 'positive' | 'heavy' | 'mixed' | 'neutral' | 'needs-more-detail'
  summary: string
  signals: JournalSignal[]
  reflectionPrompt: string
  nextStep: string
}

const signalLexicon: Record<string, string[]> = {
  stress: ['anxious', 'overwhelmed', 'work', 'deadline', 'pressure', 'stress', 'worried'],
  gratitude: ['grateful', 'thankful', 'appreciate', 'blessed', 'helped'],
  energy: ['energized', 'motivated', 'clear', 'focused', 'excited', 'proud'],
  depletion: ['tired', 'drained', 'sad', 'lonely', 'angry', 'stuck', 'numb'],
  connection: ['friend', 'family', 'partner', 'relationship', 'talked', 'called'],
}

const positiveWords = ['grateful', 'calm', 'happy', 'proud', 'excited', 'hopeful', 'clear', 'better', 'helped']
const heavyWords = ['anxious', 'overwhelmed', 'sad', 'angry', 'worried', 'tired', 'stuck', 'lonely', 'stress']

function normalizeWords(text: string): string[] {
  return text.toLowerCase().match(/[a-z']+/g) ?? []
}

function countMatches(words: string[], lexicon: string[]) {
  return words.filter((word) => lexicon.includes(word)).length
}

function pickTheme(words: string[]) {
  const themes = ['work', 'relationship', 'family', 'health', 'money', 'school', 'sleep', 'habit']
  return themes.find((theme) => words.includes(theme)) ?? 'what happened today'
}

export function analyzeJournalEntry(input: JournalEntryInput): JournalAnalysis {
  const text = input.text.trim()
  const words = normalizeWords(text)

  if (words.length < 3) {
    return {
      mood: input.mood,
      tone: 'needs-more-detail',
      summary: 'Add a few more sentences so the reflection can find a useful pattern.',
      signals: [],
      reflectionPrompt: 'What happened, what did you feel in your body, and what do you want to do next?',
      nextStep: 'Write at least three concrete details: the situation, the feeling, and one small action you can take.',
    }
  }

  const positiveCount = countMatches(words, positiveWords)
  const heavyCount = countMatches(words, heavyWords)
  const tone =
    positiveCount > 0 && heavyCount > 0
      ? 'mixed'
      : heavyCount > positiveCount
        ? 'heavy'
        : positiveCount > heavyCount
          ? 'positive'
          : 'neutral'

  const signals = Object.entries(signalLexicon)
    .map(([label, terms]) => {
      const evidence = terms.filter((term) => words.includes(term))
      return { label, score: evidence.length, evidence }
    })
    .filter((signal) => signal.score > 0)
    .sort((a, b) => b.score - a.score)

  const mainTheme = pickTheme(words)
  const strongestSignal = signals[0]?.label ?? 'clarity'
  const nextStepByTone: Record<JournalAnalysis['tone'], string> = {
    positive: 'Capture what worked and schedule one repeatable action that protects this momentum tomorrow.',
    heavy: 'Pick one controllable next action: a reset walk, a direct message, or a 10-minute cleanup of the biggest stressor.',
    mixed: 'Separate the hard part from the hopeful part, then choose one small action that supports the hopeful part.',
    neutral: 'Name the most important detail and decide whether it deserves action, acceptance, or a follow-up note.',
    'needs-more-detail': 'Write at least three concrete details: the situation, the feeling, and one small action you can take.',
  }

  return {
    mood: input.mood,
    tone,
    summary: `Your entry centers on ${mainTheme}, with ${strongestSignal} showing up as the strongest signal.`,
    signals,
    reflectionPrompt: `What is one thing about ${mainTheme} that you can influence before your next check-in?`,
    nextStep: nextStepByTone[tone],
  }
}
