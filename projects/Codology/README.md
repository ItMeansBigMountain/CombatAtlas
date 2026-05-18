# Codology

## Overview
Codology is a lightweight coding-language guessing game. Players start immediately, answer multiple-choice coding questions, then enter their name after the game to submit their score/time to the leaderboard.

## Live URLs
- **Frontend:** https://codology-three.vercel.app
- **API highscores:** https://codology-api.vercel.app/api/highscores

## Source
- **Remote URL:** https://github.com/ItMeansBigMountain/Codology.git
- **Default Branch:** main

## Current Functionality
- No login/signup required in the frontend flow.
- Home screen starts the quiz directly.
- End-of-game screen collects a display name.
- Scores are submitted anonymously to `/api/add-highscore`.
- Leaderboard screen fetches and renders `/api/highscores`.
- API sorts leaderboard rows by highest score, then fastest time.

## Data / Database Note
Codology does **not** need a user database for the current product shape because there are no user accounts. The deployed API currently uses demo-mode in-memory highscores when no database environment variable is configured. That is fine for a live demo, but scores are not guaranteed to survive Vercel cold starts/redeploys.

If a durable global leaderboard becomes important later, add a small persistent store such as Vercel KV/Redis, Supabase, Neon/Postgres, or another hosted database. That still would not require user accounts unless we decide to add real profiles.

## Development
```bash
# Source checks for no-login leaderboard flow
npm test

# Export web frontend
cd codology
npx expo export --platform web
```

## Recent Notes
- Removed login from the app flow.
- Reworked the game ending so players type their name only after completing a round.
- Redeployed frontend to Vercel alias `codology-three.vercel.app`.
- Redeployed API to Vercel alias `codology-api.vercel.app`.
