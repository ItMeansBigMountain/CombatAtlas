# HeRmEz Projects Workspace

Active and legacy projects live here so we can finish them, deploy them to Vercel, and manually test/refine each app.

> Runtime path in this container: `/opt/data/HeRmEz/projects`  
> User-facing mapped path requested: `/docker/hermes-agent-xbit/data/HeRmEz/projects`


## Full Vercel deployment pass — 2026-05-22

All deployable project folders now have a public Vercel URL verified with anonymous HTTP `200`. Many plan-only/script/archive folders are intentionally deployed as safe static review shells so they can be edited from a visible baseline without adding secrets, accounts, payments, or paid integrations.

See the complete verified URL list: [`DEPLOY_FINAL_URLS.md`](./DEPLOY_FINAL_URLS.md).

Full project review sheet with tech stacks, legacy-modernization notes, consumer-psychology UX recommendations, and verified Vercel URLs: [`PROJECT_REVIEW_SHEET.md`](./PROJECT_REVIEW_SHEET.md) / [`PROJECT_REVIEW_SHEET.csv`](./PROJECT_REVIEW_SHEET.csv). Standing review goal: [`PROJECT_REVIEW_GOAL.md`](./PROJECT_REVIEW_GOAL.md).

## Vercel manual testing tracker

Use this table as the single place to record Vercel preview/production URLs as projects are completed and deployed. Add notes after each manual test pass.

| Project | Status | Vercel production / preview URL | Alias / friendly URL | Manual testing notes |
|---|---|---|---|---|
| 3d-react-web | Redeployed / publicly accessible | https://3d-react-2ghv4m4c9-itmeansbigmountains-projects.vercel.app | https://3d-react-web.vercel.app | Build passes; anonymous HTTP check returns 200 for production and alias. Browser visual review still pending because Chrome is not installed in this container. |
| addictive-mobile-games | Needs triage | — | — | — |
| api.requests | Needs triage | — | — | — |
| az204 | Active study/reference repo | local clone | https://github.com/ItMeansBigMountain/az204 | AZ-204 certification practice repo; Function App lab reviewed for daily portfolio reporting architecture. |
| cellphone_scripts | Needs triage | — | — | — |
| CloudAutomation | Needs triage | — | — | — |
| coding-school-platform | Needs triage | — | — | — |
| Codology | Redeployed frontend + API / Basic 13 no-login leaderboard flow | https://codology-ky38h3a53-itmeansbigmountains-projects.vercel.app | https://codology-three.vercel.app; API: https://codology-api.vercel.app/api/highscores | Frontend and API return anonymous HTTP 200. Login is removed. Game now reviews the Basic 13 in Python + JavaScript with code-card visuals instead of broken image assets; players enter a name after the game and submit to the leaderboard. API highscores run in demo-mode memory unless durable score storage is added. |
| CombatAtlas | Complete React/Vite drill atlas / publicly accessible | https://combatatlas-kogc89o9c-itmeansbigmountains-projects.vercel.app | https://combatatlas-flame.vercel.app | Full martial arts drill database: 22 arts, 882 searchable drills, art exploration, safety/contact/equipment filters, optional Wikipedia/Wikidata/Wikimedia/Kaggle/BJJ import hooks. Anonymous HTTP/browser checks return 200. |
| consumer-advocate-app | Needs triage | — | — | — |
| honda-tech-upgrade | Needs triage | — | — | — |
| journal-ai | Needs triage | — | — | — |
| local-meeting-transcriber | Needs triage | — | — | — |
| muscleMadness | Skipped for now | https://musclemadness-lvdo5n1l9-itmeansbigmountains-projects.vercel.app | https://musclemadness-theta.vercel.app | User said to skip `muscleMadness` for now. |
| muscleMadness_API | Skipped for now | — | — | User said to skip `muscleMadness` for now. |
| music-mood-app | Needs triage | — | — | — |
| MusicAI | Needs triage | — | — | — |
| oyama-productions-legal | Needs triage | — | — | — |
| card-intel-scanner | Deployed / publicly accessible | https://card-intel-scanner-dxz5ue8l2-itmeansbigmountains-projects.vercel.app | https://card-intel-scanner.vercel.app | Pokémon card scanner + price aggregator: upload/camera OCR, search Pokémon TCG API, aggregate TCGplayer + Cardmarket pricing and eBay sold-comps link. Anonymous HTTP checks return 200 for production and alias. |
| policy-pit-app | Needs triage | — | — | — |
| portfolio-sentiment-subscription-app | Needs triage | — | — | — |
| robinhood-email-reports | Needs triage | — | — | — |
| robinhood-daily-portfolio-report | New standalone repo scaffold | local / GitHub | https://github.com/ItMeansBigMountain/robinhood-daily-portfolio-report | Lightweight daily portfolio report generator created after reviewing az204 Function App pattern. |
| RTS-JS-ChatRooms | Needs triage | — | — | — |
| scraper-project | Needs triage | — | — | — |
| sleep-dream-app | Needs triage | — | — | — |
| social-media-analysis | Merge target / product direction set | https://social-media-analysis-five.vercel.app | — | Personal presence intelligence app combining social imports, uploaded user data archives, topic/mood/sentiment/communication insights, tweetBetweenTheLines, and twitter-therapy-app. |
| stockNews | Deployed / needs manual browser review | https://stock-news-frontend-norfaejlp-itmeansbigmountains-projects.vercel.app | https://stocknews-sentiment.vercel.app | Angular demo dashboard uses local browser portfolio storage and calls Django API at https://stocknews-api.vercel.app for latest Yahoo Finance RSS + heuristic sentiment. |
| store-code-content-studio | Needs triage | — | — | — |
| survey-analytics-website | Needs triage | — | — | — |
| ticVoter | Skipped for now | https://ticvoter-ep90g308p-itmeansbigmountains-projects.vercel.app | https://ticvoter.vercel.app | User said to skip `ticVoter` for now. |
| ticVoter_REST.api | Skipped for now | — | — | User said to skip `ticVoter` for now. |
| tiktok-clone | Needs triage | — | — | — |
| tiktok-shop-shopify-commerce | Needs triage | — | — | — |
| tournament-wager-app | Needs triage | — | — | — |
| tutoring.Repl | Needs triage | — | — | — |
| tweet_video_generator | Needs triage | — | — | — |
| tweetBetweenTheLines | Merge into social-media-analysis | https://tweetbetweenthelines.vercel.app | — | Keep Twitter/X parsing, topic, trend, and mood scripts as import modules. |
| twitter-therapy-app | Merge into social-media-analysis | https://twitter-therapy-app.vercel.app | — | Keep reflection and non-diagnostic mental-health-adjacent insight layer. |
| watsonAI | Needs triage | — | — | — |
| WebCrawl | Needs triage | — | — | — |
| wutHappened | Product direction set | https://wuthappened.vercel.app | — | Portfolio-aware news intelligence: import holdings and explain relevant stock/news/sentiment changes. |

## Already deployed legacy URLs found

- **3d-react-web**
  - Frontend: https://3d-react-2ghv4m4c9-itmeansbigmountains-projects.vercel.app
  - Frontend alias: https://3d-react-web.vercel.app
- **Codology**
  - Frontend: https://codology-ky38h3a53-itmeansbigmountains-projects.vercel.app
  - Frontend alias: https://codology-three.vercel.app
  - API highscores: https://codology-api.vercel.app/api/highscores
- **muscleMadness**
  - https://musclemadness-lvdo5n1l9-itmeansbigmountains-projects.vercel.app
  - https://musclemadness-theta.vercel.app
- **ticVoter**
  - https://ticvoter-ep90g308p-itmeansbigmountains-projects.vercel.app
  - https://ticvoter.vercel.app

## Triage notes

Detailed deployment scan: [`VERCEL_TRIAGE.md`](./VERCEL_TRIAGE.md)

Current finding: the Vercel API token is available. Deployment SSO protection has now been disabled for the currently discovered Vercel projects. `3d-react-web` and `codology` verify publicly with HTTP 200. `muscleMadness` and `ticVoter` are intentionally skipped for now per user direction.

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
