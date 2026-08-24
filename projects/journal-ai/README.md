# Journal AI

A local-first clickable journal MVP for quick self-reflection.

## Status

The original Vite/TypeScript meeting MVP remains in `frontend/journal-app`. A shared Expo Router client now lives in `apps/mobile` and exports for web, iOS, and Android.

Live public URL:
- https://journal-ai-sooty.vercel.app

Additional public alias from the latest deployment:
- https://journal-app-five-delta.vercel.app

The Expo client supports private on-device journals, durable local/offline changes, permanent deletion, export, consent-gated meeting upload, processing status, notification permission/reminders, OAuth deep-link handling, and native secure session storage. OAuth and real transcription remain release-environment integrations: configure `EXPO_PUBLIC_OAUTH_URL` and a production processing service before claiming those paths are live.

## Universal client

```bash
cd apps/mobile
npm install
npm run typecheck
npx expo-doctor
npm run build:web
npm run build:ios
npm run build:android
```

`eas.json` contains development, internal-preview, and production App Bundle profiles. Store-signing credentials, TestFlight submission, Android internal-track upload, physical-device QA, and the production web deployment are intentionally delegated to the release gate; local Metro exports are not store releases.

## Architecture notes

- Meeting recording/transcription is planned as a consented Journal AI capability, not a separate product fork.
- See `MEETING_INTELLIGENCE_DIRECTION.md` for the audited Local Meeting Transcriber migration map, reusable .NET/Expo/WhisperX/pyannote/Ollama/Terraform pieces, and security/privacy gates.
- Do not archive `../local-meeting-transcriber` until the migrated behavior is implemented, verified, and traceable back to the source history.

## Local development

```bash
cd frontend/journal-app
npm install
npm test
npm run build
npm run dev
```

## Environment

Local configuration should come from `.env`. Do not commit real secrets. Keep committed examples in `.env.example`.
