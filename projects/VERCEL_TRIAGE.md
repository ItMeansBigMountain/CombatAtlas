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

The existing Vercel deployment URLs currently return `401 Unauthorized` from anonymous/manual browser checks. This usually means Vercel Deployment Protection / authentication is enabled for those deployments or the public aliases are not configured correctly.

Needed before manual testing is easy:

1. Either disable protection for preview/production deployments, or
2. Provide the intended public alias/domain per app, or
3. Provide the deployment-bypass setting/token if the team wants protected previews.

## Immediate deploy/redeploy candidates

| Project | Type | Current state | What is needed |
|---|---|---|---|
| `3d-react-web` | Create React App / Three.js | `npm run build` passes locally. Existing Vercel project exists but URL is protected. | Can redeploy now. Need deployment protection/alias fixed for manual testing. Optional: reduce bundle size and update stale CRA dependencies. |
| `Codology` | Express backend + Expo/mobile frontend | Existing `codology` and `codology-api` Vercel projects exist. Root backend has Express scripts. Mobile frontend is Expo. | Decide whether Vercel should host only API, only web build, or both as separate projects. Need manual product review. |
| `muscleMadness` | Expo React Native web build | Existing Vercel project exists. Dependencies are older Expo 44. | Need dependency install/build check, likely Expo web export/update work. Also needs API endpoint decision. |
| `ticVoter` | Expo React Native web build | Existing Vercel project exists. Dependencies are older Expo 44. | Need dependency install/build check, Firebase/API env values, and backend endpoint decision. |
| `stockNews` | Angular frontend + Django backend | Angular frontend exists; local build failed only because deps were not installed (`ng` missing). | Run `npm ci`, build Angular, then deploy frontend to Vercel. Backend likely needs separate Render/Railway/Fly/Vercel serverless refactor. |

## Backend/API candidates needing deployment decisions

| Project | Type | What is needed |
|---|---|---|
| `CombatAtlas` | Django REST API | Needs requirements file, production settings, DB choice, and host decision. Vercel is possible for serverless Django but Render/Railway may be simpler. |
| `muscleMadness_API` | Django API | Needs requirements, production settings, database/env config. Match it to the `muscleMadness` frontend. |
| `ticVoter_REST.api` | Django API | Has requirements and Django app. Needs secrets/env, database plan, and API URL for frontend. |
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
- `pokemon-go-qr-trade-site`
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
4. Triage `ticVoter` and `muscleMadness` together because both are older Expo apps with similar deployment problems.
5. Build/deploy `stockNews` frontend, then decide backend hosting.
6. Pick one project-plan folder to turn into a clean modern Vercel app rather than trying to rescue every legacy folder at once.

## What I need from the user

Minimum:

- Confirm whether Vercel deployment protection should be disabled or whether there is a bypass method for manual testing.
- Pick which project to polish/deploy first after `3d-react-web`.

For apps with real integrations:

- Firebase config for `ticVoter`, if it should be functional.
- API/backend URL decisions for `ticVoter` and `muscleMadness`.
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
