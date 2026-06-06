# Vercel Deployment Triage

Scanned: 2026-05-17

Workspace path: `/opt/data/HeRmEz/projects`

## Vercel access

- Vercel API token: available in environment.
- Vercel CLI: not installed globally. We can use the REST API or `npx vercel` when deploying.
- Existing Vercel projects found through the API:
  - `3d-react-web`
  - `ticvoter`
  - `musclemadness`
  - `codology`
  - `codology-api`

## Important deployment-protection issue

Resolved: deployment SSO protection has been disabled via the Vercel API for the currently discovered Vercel projects.

Verification after disabling:

- `3d-react-web`: anonymous HTTP 200.
- `ticvoter`: no longer 401, but skipped for now per user direction.
- `musclemadness`: no longer 401, but skipped for now per user direction.
- `codology`: no longer 401, but latest deployment returns 404 and needs redeploy/build repair.

## Immediate update — 3d-react-web redeploy

- Latest production deployment: `https://3d-react-2ghv4m4c9-itmeansbigmountains-projects.vercel.app`
- Public alias: `https://3d-react-web.vercel.app`
- Verification: both URLs return anonymous HTTP 200 with `text/html; charset=utf-8`.
- Build notes: Vercel build succeeds with warnings about stale CRA/Browserslist, a missing Mediapipe source map, and large bundle size. These are polish items, not blockers.
- Visual/browser review is still pending because this container does not currently have Chrome installed for browser automation.

## Immediate update — Codology Basic 13 no-login leaderboard redeploy

- Frontend deployment: `https://codology-ky38h3a53-itmeansbigmountains-projects.vercel.app`
- Frontend alias: `https://codology-three.vercel.app`
- API alias: `https://codology-api.vercel.app`
- Verified checks:
  - `GET /` on frontend returns anonymous HTTP 200.
  - Latest frontend JS bundle contains `Basic 13`, `Code Picture`, and Basic 13 question text, and no longer references `../assets/` question images.
  - `GET /api/highscores` returns anonymous HTTP 200.
  - `POST /api/add-highscore` accepts `{ username, score, time }` without login and the posted score appears in `GET /api/highscores`.
- Fixes made:
  - Removed the frontend Login screen from the app flow; `Home` is now the initial route.
  - Replaced broken/static question images with styled code-card visuals rendered in React Native Web text.
  - Added all 13 Basic 13 drills in both Python and JavaScript, 26 quiz cards total.
  - Added kid-friendly learning tips for every Basic 13 card.
  - Added a post-game name entry form. Players submit their display name only after completing the game.
  - Implemented a rendered leaderboard screen instead of only logging API results.
  - Kept API highscores anonymous and sorted by highest score then fastest time.
  - Added `npm test` source checks for the no-login leaderboard flow and Basic 13 content.
- Data note: no user database is needed for the current flow. The no-DB Vercel API uses demo-mode in-memory highscores, which are good for a live demo but not guaranteed durable across cold starts/redeploys. A durable leaderboard later would need a tiny hosted store/DB, but not user accounts.

## Immediate update — card-intel-scanner reframed as Card Intel Scanner

- Project path: `/opt/data/HeRmEz/projects/card-intel-scanner`
- New product direction: unofficial Pokémon card scanner + price aggregator, replacing the Pokémon Go friend-code concept.
- Type: static React/Vite MVP; no backend required.
- Local verification:
  - `npm install` completed with 0 vulnerabilities.
  - `npm run build` passes.
  - `npm run preview` returns local HTTP 200.
  - Built bundle contains scanner/pricing source logic.
  - Pokémon TCG API verification with browser-style headers returns card data containing TCGplayer and Cardmarket pricing.
- Implemented:
  - Upload/camera image intake.
  - Browser OCR via `tesseract.js` to extract likely card text.
  - Manual search/correction flow.
  - Pokémon TCG API card matching.
  - Aggregated price rows from TCGplayer and Cardmarket where available.
  - eBay sold-comps search link for reality validation.
  - Blended median estimate from numeric price signals.
- Vercel state: deployed to production and verified publicly.
- Production deployment: `https://card-intel-scanner-dxz5ue8l2-itmeansbigmountains-projects.vercel.app`
- Public alias: `https://card-intel-scanner.vercel.app`
- Anonymous verification:
  - production URL returns HTTP 200.
  - alias returns HTTP 200.
  - deployed JS bundle contains TCGplayer, Cardmarket, and eBay pricing logic.

## Full deployment review — 2026-05-26

See [`VERCEL_DEPLOYMENT_REVIEW_2026-05-26.md`](./VERCEL_DEPLOYMENT_REVIEW_2026-05-26.md). Current pass found Vercel credentials available, 54 active Vercel projects after deleting obsolete `bitcoin-bike-startup`, and public HTTP responses for the tracked deployment set. The first pass found 401 protection on `algos`, `consumer-advocate-app`, and `legacy-src`; SSO protection was disabled for those projects and follow-up checks returned 200. Only `codology-api` latest root returns 404, while its tracked `/api/highscores` endpoint remains the manual-test target. Public 200 means deploy plumbing is healthy; many projects remain static review shells that need product MVP work from their `DEVELOPMENT_PLAN.md`.


## Immediate deploy/redeploy candidates

| Project | Type | Current state | What is needed |
|---|---|---|---|
| `3d-react-web` | Create React App / Three.js | `npm run build` passes locally. Existing Vercel project exists but URL is protected. | Can redeploy now. Need deployment protection/alias fixed for manual testing. Optional: reduce bundle size and update stale CRA dependencies. |
| `Codology` | Express backend + Expo/mobile frontend | Existing `codology` and `codology-api` Vercel projects exist. Root backend has Express scripts. Mobile frontend is Expo. | Decide whether Vercel should host only API, only web build, or both as separate projects. Need manual product review. |
| `muscleMadness` | Expo React Native web build | Existing Vercel project exists. Dependencies are older Expo 44. | Skipped for now per user direction. |
| `ticVoter` | Expo React Native web build | Existing Vercel project exists. Dependencies are older Expo 44. | Skipped for now per user direction. |
| `stockNews` | Angular frontend + Django backend | Frontend and API deployed. Backend now supports no-secret latest Yahoo Finance RSS + heuristic sentiment while IBM Watson credentials are pending. | Manual browser automation blocked by missing Chrome; anonymous HTTP checks pass for frontend and API. Frontend alias: `https://stocknews-sentiment.vercel.app`; API alias: `https://stocknews-api.vercel.app`. |

## Backend/API candidates needing deployment decisions

| Project | Type | What is needed |
|---|---|---|
| `CombatAtlas` | Django REST API | Needs requirements file, production settings, DB choice, and host decision. Vercel is possible for serverless Django but Render/Railway may be simpler. |
| `muscleMadness_API` | Django API | Skipped for now per user direction. |
| `ticVoter_REST.api` | Django API | Skipped for now per user direction. |
| `tweetBetweenTheLines` | Django app | Needs requirements, production settings, dependency audit, and likely API/social credentials. |
| `MusicAI` | Flask app | Needs Spotify/Genius/Watson/Imgflip credentials if real integrations should work. Could deploy a reduced demo without them. |
| `RTS-JS-ChatRooms` | Flask + Agora client | Needs Agora app config/keys and deployment target decision. |
| `wutHappened` | Python generation scripts | Needs API credentials and probably conversion into a web app before Vercel deployment. |

## Project-plan folders that are mostly specs, not finished apps yet

These have project plans/readmes but little or no app scaffold. They need product decisions and implementation before Vercel deployment:

- `addictive-mobile-games`
- `bitcoin-bike-startup`
- `coding-school-platform`
- `consumer-advocate-app`
- `honda-tech-upgrade`
- `journal-ai`
- `local-meeting-transcriber`
- `music-mood-app`
- `oyama-productions-legal`
- `card-intel-scanner`
- `policy-pit-app`
- `portfolio-sentiment-subscription-app`
- `robinhood-email-reports`
- `scraper-project`
- `sleep-dream-app`
- `social-media-analysis`
- `store-code-content-studio`
- `survey-analytics-website`
- `tiktok-clone`
- `tiktok-shop-shopify-commerce`
- `tournament-wager-app`
- `twitter-therapy-app`

## Script/archive folders that are not Vercel app candidates as-is

These are useful code archives, learning material, notebooks, or automation scripts. They should not be prioritized for Vercel unless we wrap them in a product UI/API:

- `api.requests`
- `cellphone_scripts`
- `CloudAutomation`
- `docs`
- `Jupyter.Notebooks`
- `music`
- `networking`
- `school`
- `selenium`
- `tutoring.Repl`
- `tweet_video_generator`
- `utilityScripts`
- `watsonAI`
- `WebCrawl`

## Recommended next order

1. Fix Vercel access/protection so deployed URLs are manually testable.
2. Re-deploy and manually test `3d-react-web` because its local build already passes.
3. Triage `Codology` because it already has Vercel projects and both frontend/backend pieces.
4. Skip `ticVoter` and `muscleMadness` for now per user direction.
5. `stockNews` is deployed for live review; revisit only for IBM Watson NLU credentials or durable account storage.
6. Pick one project-plan folder to turn into a clean modern Vercel app rather than trying to rescue every legacy folder at once.

## What I need from the user

Minimum:

- Confirm whether Vercel deployment protection should be disabled or whether there is a bypass method for manual testing.
- Pick which project to polish/deploy first after `3d-react-web`.

For apps with real integrations:

- Spotify/Genius/Watson/Imgflip credentials only if `MusicAI` should run with live integrations.
- Agora app config only if `RTS-JS-ChatRooms` should be live-functional.
- Database choice/credentials for Django APIs if they should be production backends.

Things I can handle without more user input:

- Install Vercel CLI locally via `npx`.
- Redeploy existing Vercel apps using the available token.
- Add/fix `vercel.json` configs.
- Run local builds and fix dependency/build errors.
- Update `/projects/README.md` with live URLs after deploys.
- Create clean starter implementations for the project-plan folders.

## Manual smoke test — 3d-react-web — 2026-06-06T02:14:56Z

- Vercel free-plan mode: reused existing deployments; did not create a new Vercel project.
- Latest deployment from API: `3d-react-4olrp2xq4-itmeansbigmountains-projects.vercel.app` reported `readyState=BLOCKED` and browser showed “Deployment is building”.
- Prior production deployment: `https://3d-react-qx0wr2973-itmeansbigmountains-projects.vercel.app` reported `readyState=READY` and loaded successfully.
- Browser smoke test performed: opened page, verified nav/buttons visible, clicked `Add object`, clicked `Plasma`, checked console after navigation/interactions.
- Console result: no JavaScript errors observed during this smoke pass.
- Current note: keep using the READY prior deployment for review until the blocked/latest Vercel deployment resolves or is redeployed deliberately.
