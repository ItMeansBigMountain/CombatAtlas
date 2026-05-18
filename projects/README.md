# HeRmEz Projects Workspace

Active and legacy projects live here so we can finish them, deploy them to Vercel, and manually test/refine each app.

> Runtime path in this container: `/opt/data/HeRmEz/projects`  
> User-facing mapped path requested: `/docker/hermes-agent-xbit/data/HeRmEz/projects`

## Vercel manual testing tracker

Use this table as the single place to record Vercel preview/production URLs as projects are completed and deployed. Add notes after each manual test pass.

| Project | Status | Vercel production / preview URL | Alias / friendly URL | Manual testing notes |
|---|---|---|---|---|
| 3d-react-web | Redeployed / publicly accessible | https://3d-react-2ghv4m4c9-itmeansbigmountains-projects.vercel.app | https://3d-react-web.vercel.app | Build passes; anonymous HTTP check returns 200 for production and alias. Browser visual review still pending because Chrome is not installed in this container. |
| addictive-mobile-games | Needs triage | — | — | — |
| api.requests | Needs triage | — | — | — |
| bitcoin-bike-startup | Needs triage | — | — | — |
| cellphone_scripts | Needs triage | — | — | — |
| CloudAutomation | Needs triage | — | — | — |
| coding-school-platform | Needs triage | — | — | — |
| Codology | Redeployed frontend + API / login fixed in demo mode | https://codology-6wk56qa0o-itmeansbigmountains-projects.vercel.app | https://codology-three.vercel.app; API: https://codology-api.vercel.app/api/public | Frontend and API return anonymous HTTP 200. Signup/login now return tokens and `/api/private` verifies them. Runs in demo-mode auth/highscores until a real MySQL `DATABASE_URL`/`MYSQL_URL` is added. |
| CombatAtlas | Needs triage | — | — | — |
| consumer-advocate-app | Needs triage | — | — | — |
| honda-tech-upgrade | Needs triage | — | — | — |
| journal-ai | Needs triage | — | — | — |
| local-meeting-transcriber | Needs triage | — | — | — |
| muscleMadness | Deployed / needs manual review | https://musclemadness-lvdo5n1l9-itmeansbigmountains-projects.vercel.app | https://musclemadness-theta.vercel.app | — |
| muscleMadness_API | Needs triage | — | — | — |
| music-mood-app | Needs triage | — | — | — |
| MusicAI | Needs triage | — | — | — |
| oyama-productions-legal | Needs triage | — | — | — |
| pokemon-go-qr-trade-site | Needs triage | — | — | — |
| policy-pit-app | Needs triage | — | — | — |
| portfolio-sentiment-subscription-app | Needs triage | — | — | — |
| robinhood-email-reports | Needs triage | — | — | — |
| RTS-JS-ChatRooms | Needs triage | — | — | — |
| scraper-project | Needs triage | — | — | — |
| sleep-dream-app | Needs triage | — | — | — |
| social-media-analysis | Needs triage | — | — | — |
| stockNews | Needs triage | — | — | — |
| store-code-content-studio | Needs triage | — | — | — |
| survey-analytics-website | Needs triage | — | — | — |
| ticVoter | Deployed / needs manual review | https://ticvoter-ep90g308p-itmeansbigmountains-projects.vercel.app | https://ticvoter.vercel.app | — |
| ticVoter_REST.api | Needs triage | — | — | — |
| tiktok-clone | Needs triage | — | — | — |
| tiktok-shop-shopify-commerce | Needs triage | — | — | — |
| tournament-wager-app | Needs triage | — | — | — |
| tutoring.Repl | Needs triage | — | — | — |
| tweet_video_generator | Needs triage | — | — | — |
| tweetBetweenTheLines | Needs triage | — | — | — |
| twitter-therapy-app | Needs triage | — | — | — |
| watsonAI | Needs triage | — | — | — |
| WebCrawl | Needs triage | — | — | — |
| wutHappened | Needs triage | — | — | — |

## Already deployed legacy URLs found

- **3d-react-web**
  - Frontend: https://3d-react-2ghv4m4c9-itmeansbigmountains-projects.vercel.app
  - Frontend alias: https://3d-react-web.vercel.app
- **Codology**
  - Frontend: https://codology-6wk56qa0o-itmeansbigmountains-projects.vercel.app
  - Frontend alias: https://codology-three.vercel.app
  - API public check: https://codology-api.vercel.app/api/public
- **muscleMadness**
  - https://musclemadness-lvdo5n1l9-itmeansbigmountains-projects.vercel.app
  - https://musclemadness-theta.vercel.app
- **ticVoter**
  - https://ticvoter-ep90g308p-itmeansbigmountains-projects.vercel.app
  - https://ticvoter.vercel.app

## Triage notes

Detailed deployment scan: [`VERCEL_TRIAGE.md`](./VERCEL_TRIAGE.md)

Current finding: the Vercel API token is available. Deployment SSO protection has now been disabled for the currently discovered Vercel projects. `3d-react-web` verifies publicly with HTTP 200; `ticvoter`, `musclemadness`, and `codology` now need redeploy/build repair because their latest public URLs return 404 instead of 401.

Free hosting/data plan: [`FREE_HOSTING_AND_SQLITE_PLAN.md`](./FREE_HOSTING_AND_SQLITE_PLAN.md)

Credential status / missing tokens: [`CREDENTIALS_STATUS.md`](./CREDENTIALS_STATUS.md)

## Workflow for each project

1. Open the project folder in `/opt/data/HeRmEz/projects/<project-name>`.
2. Audit framework, dependencies, env vars, and build command.
3. Remove or template secrets; keep real credentials out of Git.
4. Make the app run locally or in a preview environment.
5. Deploy to Vercel, then paste the preview/production URL into this README.
6. Manually test the live URL and record refinement notes in the table.
7. Iterate until the app is polished enough for production/custom domain work.

## Notes

- The old `legacy-projects` source folder was root-owned in this environment, so its contents were copied into this workspace instead of deleted from the original location.
- Local `.env` files and nested `.git` internals are ignored by the HeRmEz parent repo and should not be committed.
- Cox Elementary PTA is tracked separately and deployed on Render, not Vercel.
