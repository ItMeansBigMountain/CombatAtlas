# Journal AI + Dream Analysis Direction

`journal-ai` and `sleep-dream-app` should merge into one privacy-first reflection product.

## Product goal

A private emotional intelligence app for journaling, dreams, mood patterns, themes, and self-reflection.

## Core flows

- Daily journal entry.
- Dream log with symbol/theme analysis.
- Mood and sleep context.
- Consented voice/meeting capture for transcripts, commitments, and post-meeting reflection.
- Weekly recurring themes and insights.
- Local/demo mode before account creation.

## Merge note

Use `journal-ai` as the primary product surface and treat `sleep-dream-app` as a specialized module.

## Meeting intelligence note

Treat `local-meeting-transcriber` as source material for a Journal AI module, not a standalone destination. The migration must preserve source history, require recording consent, keep local-first transcription as the default, avoid invented speaker identities or uncited insights, and honor separate export/delete controls for raw audio, transcripts, summaries, embeddings, and journal reflections. See `MEETING_INTELLIGENCE_DIRECTION.md` for the architecture/audit map.
