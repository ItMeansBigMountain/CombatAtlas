# Free Hosting + SQLite / Low-Cost Data Plan

Updated: 2026-05-17

## Decision

Default to the simplest free/low-friction option per app:

1. **Frontend-only apps** → Vercel static/site deployment.
2. **Small demo APIs** → SQLite if the host supports persistent disk; otherwise JSON/sample-data mode for Vercel previews.
3. **Django/Flask apps with writes** → prefer Render/Railway/Fly free-ish tiers with SQLite + persistent disk, or convert to serverless with an external free DB only if needed.
4. **Auth/data-heavy apps** → use Firebase/Supabase free tier only when the app already depends on it or needs hosted auth.

## Vercel protection status

Deployment SSO protection has been disabled via the Vercel API for the currently discovered projects:

- `3d-react-web`
- `ticvoter`
- `musclemadness`
- `codology`
- `codology-api`

Verification:

- `3d-react-web` now loads anonymously with HTTP 200.
- `ticvoter`, `musclemadness`, and `codology` no longer show 401 protection, but their latest deployments currently return 404, so they need redeploy/build repair.

## Per-project data/storage plan

| Project | Current backend/data | Recommended free/simple path | Notes |
|---|---|---|---|
| `3d-react-web` | Static React app | Vercel static only | No database needed. Build passes locally. |
| `Codology` | Express API + frontend/mobile app | Start with JSON/SQLite API, deploy API separately | Existing `codology-api` Vercel project exists. Need to decide whether to keep Express serverless or move to SQLite on a persistent host. |
| `ticVoter` | Expo frontend + Django API + Firebase auth | Keep Django API on SQLite for demo; Firebase only if auth required | Django settings already use SQLite. For no-credential demo, replace Firebase requirement with anonymous/demo mode. |
| `ticVoter_REST.api` | Django API | SQLite already configured | Needs production settings and seed data. Host with persistent disk if writes matter. |
| `muscleMadness` | Expo frontend + Django API | SQLite-backed Django API with seed workouts | Django settings already use SQLite. Frontend can point to demo API URL. |
| `muscleMadness_API` | Django API | SQLite already configured | Needs requirements, production settings, seed data. |
| `stockNews` | Angular frontend + Django backend | Angular on Vercel; Django on SQLite/sample data | Backend settings already use SQLite. External news/market APIs can be optional/sample mode. |
| `CombatAtlas` | Django REST API | SQLite + seed martial arts drills | SQLite already configured. Good candidate for Render/Railway persistent disk or static JSON API demo. |
| `tweetBetweenTheLines` | Django app | SQLite for local/demo data; external X/Twitter APIs optional | SQLite already configured, but live social API credentials are needed for full function. |
| `MusicAI` | Flask app with Spotify/Genius/Watson/Imgflip | SQLite/local JSON cache + demo mode until credentials are provided | Live integrations require tokens. Can still ship a sample-data demo. |
| `RTS-JS-ChatRooms` | Flask + Agora | Static/demo mode or Flask with SQLite sessions | Agora credentials required for real-time functionality. |
| `portfolio-sentiment-subscription-app` | Python app | Already configured for `sqlite:///./local.db` | Can run with sample market/news data until API credentials are added. |

## General implementation checklist

For each backend project:

1. Add `.env.example` with only placeholder values.
2. Use SQLite by default for local/demo mode.
3. Add seed/sample data so the UI works without external credentials.
4. Gate paid/external APIs behind optional env vars.
5. Add `/health` endpoint for deployment verification.
6. Add CORS config for the deployed frontend URL.
7. If hosted on Vercel serverless, avoid relying on persistent local SQLite writes; use read-only bundled seed data or a free hosted DB. If writes matter, deploy backend to a host with persistent disk.

## Recommended next execution order

1. Redeploy `3d-react-web` to confirm the protection fix and update the tracker URL.
2. Fix/redeploy `Codology` API and decide on frontend mode.
3. Convert `ticVoter` to demo mode with SQLite-backed API and optional Firebase.
4. Convert `muscleMadness` to demo mode with SQLite-backed API and seed workouts.
5. Build/deploy `stockNews` frontend, then wire backend sample data.
