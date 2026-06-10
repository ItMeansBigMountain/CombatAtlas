import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'
import ts from 'typescript'

async function importTs(path) {
  const fileUrl = path instanceof URL ? path : pathToFileURL(path)
  const filePath = fileUrl.pathname
  const source = await readFile(fileUrl, 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.ES2022,
      target: ts.ScriptTarget.ES2022,
      verbatimModuleSyntax: true,
    },
    fileName: filePath,
  })
  const encoded = Buffer.from(outputText).toString('base64')
  return import(`data:text/javascript;base64,${encoded}`)
}

const { analyzeJournalEntry } = await importTs(new URL('../src/journalAnalysis.ts', import.meta.url))

await assert.rejects(
  () => importTs(new URL('../src/does-not-exist.ts', import.meta.url)),
  /ENOENT/,
  'test harness should surface missing source files'
)

const anxiousResult = analyzeJournalEntry({
  text: 'I feel anxious and overwhelmed about work, but a walk helped me feel grateful and calm.',
  mood: 'anxious',
})

assert.equal(anxiousResult.mood, 'anxious')
assert.equal(anxiousResult.tone, 'mixed')
assert.ok(anxiousResult.summary.includes('work'), 'summary should reflect the entry theme')
assert.ok(anxiousResult.reflectionPrompt.includes('?'), 'reflection prompt should ask a question')
assert.ok(anxiousResult.nextStep.length > 20, 'next step should be actionable')
assert.ok(anxiousResult.signals.some((signal) => signal.label === 'stress'))
assert.ok(anxiousResult.signals.some((signal) => signal.label === 'gratitude'))

const shortResult = analyzeJournalEntry({ text: '', mood: 'calm' })
assert.equal(shortResult.tone, 'needs-more-detail')
assert.equal(shortResult.signals.length, 0)
