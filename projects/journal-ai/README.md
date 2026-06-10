# Journal AI

A local-first clickable journal MVP for quick self-reflection.

## Status

Functional Vite/TypeScript MVP implemented in `frontend/journal-app`.

Live public URL:
- https://journal-ai-sooty.vercel.app

Additional public alias from the latest deployment:
- https://journal-app-five-delta.vercel.app

The app currently keeps all behavior in the browser: users can enter a journal entry, select a mood, run a demo/local analysis, and see a reflection prompt plus next step. No paid APIs, credentials, auth, or backend storage are wired yet.

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
