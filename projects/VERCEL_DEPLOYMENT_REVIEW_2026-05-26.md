# Vercel Deployment Review — 2026-05-26

- Vercel API projects found: 54
- Unique URLs checked: 105
- Status counts: 200: 104, 404: 1

## Important cleanup

- Deleted obsolete Vercel project `bitcoin-bike-startup` because the local project was already removed per user direction.
- Disabled deployment protection on `algos`, `consumer-advocate-app`, and `legacy-src` latest deployments after the first pass found 401 responses; follow-up checks return 200.
- `codology-api` latest deployment root returns 404, but the API alias endpoint tracked elsewhere (`https://codology-api.vercel.app/api/highscores`) is expected for manual testing.

## API project inventory

| Vercel project | Framework | Latest deployment | Ready state |
|---|---|---|---|
| `3d-react-web` | create-react-app | https://3d-react-qx0wr2973-itmeansbigmountains-projects.vercel.app | READY |
| `addictive-mobile-games` | vite | https://addictive-mobile-games-93znhpmjz-itmeansbigmountains-projects.vercel.app | READY |
| `algos` | vite | https://algos-qr2kwrdcu-itmeansbigmountains-projects.vercel.app | READY |
| `api-requests` | vite | https://api-requests-k0fawando-itmeansbigmountains-projects.vercel.app | READY |
| `api.requests` | vite | https://apirequests-1pntxt66f-itmeansbigmountains-projects.vercel.app | READY |
| `card-intel-scanner` | vite | https://card-intel-scanner-rcos7zn54-itmeansbigmountains-projects.vercel.app | READY |
| `cellphone_scripts` | vite | https://cellphonescripts-fp147lbsh-itmeansbigmountains-projects.vercel.app | READY |
| `cloudautomation` | vite | https://cloudautomation-7rx3hmny2-itmeansbigmountains-projects.vercel.app | READY |
| `coding-school-platform` | vite | https://coding-school-platform-epgt7zyry-itmeansbigmountains-projects.vercel.app | READY |
| `codology` |  | https://codology-p0hscgzls-itmeansbigmountains-projects.vercel.app | READY |
| `codology-api` | express | https://codology-145ue1ypf-itmeansbigmountains-projects.vercel.app | READY |
| `combatatlas` | vite | https://combatatlas-gtzv58b0l-itmeansbigmountains-projects.vercel.app | READY |
| `consumer-advocate-app` | vite | https://consumer-advocate-jbnx8bpq3-itmeansbigmountains-projects.vercel.app | READY |
| `cox-elementary-pta` | vite | https://cox-elementary-d4raizwqa-itmeansbigmountains-projects.vercel.app | READY |
| `deployment_docs` | vite | https://deploymentdocs-kl94n8e0i-itmeansbigmountains-projects.vercel.app | READY |
| `docs` | vite | https://docs-agvde8o1m-itmeansbigmountains-projects.vercel.app | READY |
| `honda-tech-upgrade` | vite | https://honda-tech-upgrade-f62krixi3-itmeansbigmountains-projects.vercel.app | READY |
| `journal-ai` | vite | https://journal-4gx44o85h-itmeansbigmountains-projects.vercel.app | READY |
| `jupyter-notebooks` | vite | https://jupyter-notebooks-pbninjam0-itmeansbigmountains-projects.vercel.app | READY |
| `legacy-src` | vite | https://legacy-83p5fc87p-itmeansbigmountains-projects.vercel.app | READY |
| `local-meeting-transcriber` | vite | https://local-meeting-transcriber-9hq9z1l4s.vercel.app | READY |
| `musclemadness` |  | https://musclemadness-ro6gd6z8x-itmeansbigmountains-projects.vercel.app | READY |
| `musclemadness-api` | vite | https://musclemadness-q5gendrfd-itmeansbigmountains-projects.vercel.app | READY |
| `music` | vite | https://music-kdw85q93c-itmeansbigmountains-projects.vercel.app | READY |
| `music-mood-app` | vite | https://music-mood-mrahbfuj1-itmeansbigmountains-projects.vercel.app | READY |
| `musicai` | vite | https://musicai-3upwf0b67-itmeansbigmountains-projects.vercel.app | READY |
| `networking` | vite | https://networking-nk7cgbofi-itmeansbigmountains-projects.vercel.app | READY |
| `oyama-productions-legal` | vite | https://oyama-productions-legal-aga0qfqqb-itmeansbigmountains-projects.vercel.app | READY |
| `policy-pit-app` | vite | https://policy-pit-6d80ak1qd-itmeansbigmountains-projects.vercel.app | READY |
| `portfolio-sentiment-subscription-app` | vite | https://portfolio-sentiment-subscription-fi1fdh28h.vercel.app | READY |
| `robinhood-email-reports` | vite | https://robinhood-email-reports-q52c1d1tn-itmeansbigmountains-projects.vercel.app | READY |
| `rts-js-chatrooms` | vite | https://rts-js-chatrooms-1ql6l49h9-itmeansbigmountains-projects.vercel.app | READY |
| `school` | vite | https://school-3uzd9xf86-itmeansbigmountains-projects.vercel.app | READY |
| `scraper-project` | vite | https://scraper-project-6ypi33354-itmeansbigmountains-projects.vercel.app | READY |
| `selenium` | vite | https://selenium-6pzej25xt-itmeansbigmountains-projects.vercel.app | READY |
| `sleep-dream-app` | vite | https://sleep-dream-1b7d4zkk3-itmeansbigmountains-projects.vercel.app | READY |
| `social-media-analysis` | vite | https://social-media-analysis-di2o1difc-itmeansbigmountains-projects.vercel.app | READY |
| `stock-news-frontend` | angular | https://stock-news-frontend-iyr2jromi-itmeansbigmountains-projects.vercel.app | READY |
| `stock_news_backend` |  | https://stocknewsbackend-8mx7ni3zb-itmeansbigmountains-projects.vercel.app | READY |
| `store-code-content-studio` | vite | https://store-code-content-studio-jm1r8hkyp.vercel.app | READY |
| `survey-analytics-website` | vite | https://survey-analytics-website-gzpg2gjvy-itmeansbigmountains-projects.vercel.app | READY |
| `ticvoter` |  | https://ticvoter-eajc3saby-itmeansbigmountains-projects.vercel.app | READY |
| `ticvoter-rest-api` | vite | https://ticvoter-rest-p5og04e8t-itmeansbigmountains-projects.vercel.app | READY |
| `tiktok-clone` | vite | https://tiktok-clone-jjw6oyktc-itmeansbigmountains-projects.vercel.app | READY |
| `tiktok-shop-shopify-commerce` | vite | https://tiktok-shop-shopify-commerce-1at2oq8zz.vercel.app | READY |
| `tournament-wager-app` | vite | https://tournament-wager-5iap7mgcs-itmeansbigmountains-projects.vercel.app | READY |
| `tutoring-repl` | vite | https://tutoring-repl-1as4pvhqq-itmeansbigmountains-projects.vercel.app | READY |
| `tweet_video_generator` | vite | https://tweetvideogenerator-i4m3rw5cx-itmeansbigmountains-projects.vercel.app | READY |
| `tweetbetweenthelines` | vite | https://tweetbetweenthelines-ajw57fpq3-itmeansbigmountains-projects.vercel.app | READY |
| `twitter-therapy-app` | vite | https://twitter-therapy-k9qd3eozf-itmeansbigmountains-projects.vercel.app | READY |
| `utilityscripts` | vite | https://utilityscripts-imhyba23x-itmeansbigmountains-projects.vercel.app | READY |
| `watsonai` | vite | https://watsonai-k1h14aqon-itmeansbigmountains-projects.vercel.app | READY |
| `webcrawl` | vite | https://webcrawl-e1i2qrx5b-itmeansbigmountains-projects.vercel.app | READY |
| `wuthappened` | vite | https://wuthappened-nhil745qb-itmeansbigmountains-projects.vercel.app | READY |

## Anonymous HTTP checks

| Project | Source | Status | URL | Title / notes |
|---|---|---:|---|---|
| `3d-react-web` | tracker | 200 | https://3d-react-web.vercel.app | 3 Dimentional App — public response |
| `CloudAutomation` | tracker | 200 | https://cloudautomation.vercel.app |  — public response |
| `Codology` | tracker | 200 | https://codology-three.vercel.app | codology — public response |
| `CombatAtlas` | tracker | 200 | https://combatatlas-flame.vercel.app | CombatAtlas — Martial Arts Drill Database — public response |
| `Jupyter.Notebooks` | tracker | 200 | https://jupyter-notebooks-green.vercel.app |  — public response |
| `MusicAI` | tracker | 200 | https://musicai-rouge.vercel.app | MusicAI — Your cross-platform music taste map — public response |
| `RTS-JS-ChatRooms` | tracker | 200 | https://rts-js-chatrooms.vercel.app |  — public response |
| `WebCrawl` | tracker | 200 | https://webcrawl-ochre.vercel.app |  — public response |
| `addictive-mobile-games` | tracker | 200 | https://addictive-mobile-games.vercel.app |  — public response |
| `algos` | tracker | 200 | https://algos-beta.vercel.app |  — public response |
| `api.requests` | tracker | 200 | https://api-requests-one.vercel.app |  — public response |
| `card-intel-scanner` | tracker | 200 | https://card-intel-scanner.vercel.app | Card Intel Scanner — public response |
| `cellphone_scripts` | tracker | 200 | https://cellphonescripts.vercel.app |  — public response |
| `coding-school-platform` | tracker | 200 | https://coding-school-platform.vercel.app |  — public response |
| `consumer-advocate-app` | tracker | 200 | https://consumer-advocate-app.vercel.app |  — public response |
| `cox-elementary-pta` | tracker | 200 | https://cox-elementary-pta.vercel.app |  — public response |
| `deployment_docs` | tracker | 200 | https://deploymentdocs.vercel.app |  — public response |
| `docs` | tracker | 200 | https://docs-umber-two-76.vercel.app |  — public response |
| `honda-tech-upgrade` | tracker | 200 | https://honda-tech-upgrade.vercel.app |  — public response |
| `journal-ai` | tracker | 200 | https://journal-ai-sooty.vercel.app |  — public response |
| `legacy-src` | tracker | 200 | https://legacy-src.vercel.app |  — public response |
| `local-meeting-transcriber` | tracker | 200 | https://local-meeting-transcriber.vercel.app |  — public response |
| `muscleMadness` | tracker | 200 | https://musclemadness-theta.vercel.app |  — public response |
| `muscleMadness_API` | tracker | 200 | https://musclemadness-api.vercel.app |  — public response |
| `music` | tracker | 200 | https://music-lac-seven.vercel.app |  — public response |
| `music-mood-app` | tracker | 200 | https://music-mood-app-chi.vercel.app |  — public response |
| `networking` | tracker | 200 | https://networking-ebon.vercel.app |  — public response |
| `oyama-productions-legal` | tracker | 200 | https://oyama-productions-legal.vercel.app |  — public response |
| `policy-pit-app` | tracker | 200 | https://policy-pit-app.vercel.app |  — public response |
| `portfolio-sentiment-subscription-app` | tracker | 200 | https://portfolio-sentiment-subscription-ap.vercel.app |  — public response |
| `robinhood-email-reports` | tracker | 200 | https://robinhood-email-reports.vercel.app |  — public response |
| `school` | tracker | 200 | https://school-plum-beta.vercel.app |  — public response |
| `scraper-project` | tracker | 200 | https://scraper-project-five.vercel.app |  — public response |
| `selenium` | tracker | 200 | https://selenium-alpha.vercel.app |  — public response |
| `sleep-dream-app` | tracker | 200 | https://sleep-dream-app.vercel.app |  — public response |
| `social-media-analysis` | tracker | 200 | https://social-media-analysis-five.vercel.app |  — public response |
| `stockNews` | tracker | 200 | https://stocknews-sentiment.vercel.app | StockNewsFrontend — public response |
| `store-code-content-studio` | tracker | 200 | https://store-code-content-studio.vercel.app |  — public response |
| `survey-analytics-website` | tracker | 200 | https://survey-analytics-website.vercel.app |  — public response |
| `ticVoter` | tracker | 200 | https://ticvoter.vercel.app |  — public response |
| `ticVoter_REST.api` | tracker | 200 | https://ticvoter-rest-api.vercel.app |  — public response |
| `tiktok-clone` | tracker | 200 | https://tiktok-clone-eta-one.vercel.app |  — public response |
| `tiktok-shop-shopify-commerce` | tracker | 200 | https://tiktok-shop-shopify-commerce.vercel.app |  — public response |
| `tournament-wager-app` | tracker | 200 | https://tournament-wager-app.vercel.app |  — public response |
| `tutoring.Repl` | tracker | 200 | https://tutoring-repl.vercel.app |  — public response |
| `tweetBetweenTheLines` | tracker | 200 | https://tweetbetweenthelines.vercel.app |  — public response |
| `tweet_video_generator` | tracker | 200 | https://tweetvideogenerator.vercel.app |  — public response |
| `twitter-therapy-app` | tracker | 200 | https://twitter-therapy-app.vercel.app |  — public response |
| `utilityScripts` | tracker | 200 | https://utilityscripts.vercel.app |  — public response |
| `watsonAI` | tracker | 200 | https://watsonai.vercel.app |  — public response |
| `wutHappened` | tracker | 200 | https://wuthappened.vercel.app |  — public response |
| `3d-react-web` | vercel-latest | 200 | https://3d-react-qx0wr2973-itmeansbigmountains-projects.vercel.app | 3 Dimentional App — public response |
| `addictive-mobile-games` | vercel-latest | 200 | https://addictive-mobile-games-93znhpmjz-itmeansbigmountains-projects.vercel.app |  — public response |
| `algos` | vercel-latest | 200 | https://algos-qr2kwrdcu-itmeansbigmountains-projects.vercel.app |  — public response |
| `api-requests` | vercel-latest | 200 | https://api-requests-k0fawando-itmeansbigmountains-projects.vercel.app |  — public response |
| `api.requests` | vercel-latest | 200 | https://apirequests-1pntxt66f-itmeansbigmountains-projects.vercel.app |  — public response |
| `card-intel-scanner` | vercel-latest | 200 | https://card-intel-scanner-rcos7zn54-itmeansbigmountains-projects.vercel.app | Card Intel Scanner — public response |
| `cellphone_scripts` | vercel-latest | 200 | https://cellphonescripts-fp147lbsh-itmeansbigmountains-projects.vercel.app |  — public response |
| `cloudautomation` | vercel-latest | 200 | https://cloudautomation-7rx3hmny2-itmeansbigmountains-projects.vercel.app |  — public response |
| `coding-school-platform` | vercel-latest | 200 | https://coding-school-platform-epgt7zyry-itmeansbigmountains-projects.vercel.app |  — public response |
| `codology` | vercel-latest | 200 | https://codology-p0hscgzls-itmeansbigmountains-projects.vercel.app | codology — public response |
| `combatatlas` | vercel-latest | 200 | https://combatatlas-gtzv58b0l-itmeansbigmountains-projects.vercel.app | CombatAtlas — Martial Arts Drill Database — public response |
| `consumer-advocate-app` | vercel-latest | 200 | https://consumer-advocate-jbnx8bpq3-itmeansbigmountains-projects.vercel.app |  — public response |
| `cox-elementary-pta` | vercel-latest | 200 | https://cox-elementary-d4raizwqa-itmeansbigmountains-projects.vercel.app |  — public response |
| `deployment_docs` | vercel-latest | 200 | https://deploymentdocs-kl94n8e0i-itmeansbigmountains-projects.vercel.app |  — public response |
| `docs` | vercel-latest | 200 | https://docs-agvde8o1m-itmeansbigmountains-projects.vercel.app |  — public response |
| `honda-tech-upgrade` | vercel-latest | 200 | https://honda-tech-upgrade-f62krixi3-itmeansbigmountains-projects.vercel.app |  — public response |
| `journal-ai` | vercel-latest | 200 | https://journal-4gx44o85h-itmeansbigmountains-projects.vercel.app |  — public response |
| `jupyter-notebooks` | vercel-latest | 200 | https://jupyter-notebooks-pbninjam0-itmeansbigmountains-projects.vercel.app |  — public response |
| `legacy-src` | vercel-latest | 200 | https://legacy-83p5fc87p-itmeansbigmountains-projects.vercel.app |  — public response |
| `local-meeting-transcriber` | vercel-latest | 200 | https://local-meeting-transcriber-9hq9z1l4s.vercel.app |  — public response |
| `musclemadness` | vercel-latest | 200 | https://musclemadness-ro6gd6z8x-itmeansbigmountains-projects.vercel.app |  — public response |
| `musclemadness-api` | vercel-latest | 200 | https://musclemadness-q5gendrfd-itmeansbigmountains-projects.vercel.app |  — public response |
| `music` | vercel-latest | 200 | https://music-kdw85q93c-itmeansbigmountains-projects.vercel.app |  — public response |
| `music-mood-app` | vercel-latest | 200 | https://music-mood-mrahbfuj1-itmeansbigmountains-projects.vercel.app |  — public response |
| `musicai` | vercel-latest | 200 | https://musicai-3upwf0b67-itmeansbigmountains-projects.vercel.app | MusicAI — Your cross-platform music taste map — public response |
| `networking` | vercel-latest | 200 | https://networking-nk7cgbofi-itmeansbigmountains-projects.vercel.app |  — public response |
| `oyama-productions-legal` | vercel-latest | 200 | https://oyama-productions-legal-aga0qfqqb-itmeansbigmountains-projects.vercel.app |  — public response |
| `policy-pit-app` | vercel-latest | 200 | https://policy-pit-6d80ak1qd-itmeansbigmountains-projects.vercel.app |  — public response |
| `portfolio-sentiment-subscription-app` | vercel-latest | 200 | https://portfolio-sentiment-subscription-fi1fdh28h.vercel.app |  — public response |
| `robinhood-email-reports` | vercel-latest | 200 | https://robinhood-email-reports-q52c1d1tn-itmeansbigmountains-projects.vercel.app |  — public response |
| `rts-js-chatrooms` | vercel-latest | 200 | https://rts-js-chatrooms-1ql6l49h9-itmeansbigmountains-projects.vercel.app |  — public response |
| `school` | vercel-latest | 200 | https://school-3uzd9xf86-itmeansbigmountains-projects.vercel.app |  — public response |
| `scraper-project` | vercel-latest | 200 | https://scraper-project-6ypi33354-itmeansbigmountains-projects.vercel.app |  — public response |
| `selenium` | vercel-latest | 200 | https://selenium-6pzej25xt-itmeansbigmountains-projects.vercel.app |  — public response |
| `sleep-dream-app` | vercel-latest | 200 | https://sleep-dream-1b7d4zkk3-itmeansbigmountains-projects.vercel.app |  — public response |
| `social-media-analysis` | vercel-latest | 200 | https://social-media-analysis-di2o1difc-itmeansbigmountains-projects.vercel.app |  — public response |
| `stock-news-frontend` | vercel-latest | 200 | https://stock-news-frontend-iyr2jromi-itmeansbigmountains-projects.vercel.app | StockNewsFrontend — public response |
| `stock_news_backend` | vercel-latest | 200 | https://stocknewsbackend-8mx7ni3zb-itmeansbigmountains-projects.vercel.app |  — public response |
| `store-code-content-studio` | vercel-latest | 200 | https://store-code-content-studio-jm1r8hkyp.vercel.app |  — public response |
| `survey-analytics-website` | vercel-latest | 200 | https://survey-analytics-website-gzpg2gjvy-itmeansbigmountains-projects.vercel.app |  — public response |
| `ticvoter` | vercel-latest | 200 | https://ticvoter-eajc3saby-itmeansbigmountains-projects.vercel.app |  — public response |
| `ticvoter-rest-api` | vercel-latest | 200 | https://ticvoter-rest-p5og04e8t-itmeansbigmountains-projects.vercel.app |  — public response |
| `tiktok-clone` | vercel-latest | 200 | https://tiktok-clone-jjw6oyktc-itmeansbigmountains-projects.vercel.app |  — public response |
| `tiktok-shop-shopify-commerce` | vercel-latest | 200 | https://tiktok-shop-shopify-commerce-1at2oq8zz.vercel.app |  — public response |
| `tournament-wager-app` | vercel-latest | 200 | https://tournament-wager-5iap7mgcs-itmeansbigmountains-projects.vercel.app |  — public response |
| `tutoring-repl` | vercel-latest | 200 | https://tutoring-repl-1as4pvhqq-itmeansbigmountains-projects.vercel.app |  — public response |
| `tweet_video_generator` | vercel-latest | 200 | https://tweetvideogenerator-i4m3rw5cx-itmeansbigmountains-projects.vercel.app |  — public response |
| `tweetbetweenthelines` | vercel-latest | 200 | https://tweetbetweenthelines-ajw57fpq3-itmeansbigmountains-projects.vercel.app |  — public response |
| `twitter-therapy-app` | vercel-latest | 200 | https://twitter-therapy-k9qd3eozf-itmeansbigmountains-projects.vercel.app |  — public response |
| `utilityscripts` | vercel-latest | 200 | https://utilityscripts-imhyba23x-itmeansbigmountains-projects.vercel.app |  — public response |
| `watsonai` | vercel-latest | 200 | https://watsonai-k1h14aqon-itmeansbigmountains-projects.vercel.app |  — public response |
| `webcrawl` | vercel-latest | 200 | https://webcrawl-e1i2qrx5b-itmeansbigmountains-projects.vercel.app |  — public response |
| `wuthappened` | vercel-latest | 200 | https://wuthappened-nhil745qb-itmeansbigmountains-projects.vercel.app |  — public response |
| `codology-api` | vercel-latest | 404 | https://codology-145ue1ypf-itmeansbigmountains-projects.vercel.app |  — not found |

## Operator recommendations

1. Treat public HTTP 200 as deployment plumbing, not product completion. Many Vercel apps are static review shells and need MVP implementation passes.
2. Promote these high-leverage projects first: `coding-school-platform`, `Codology`, `social-media-analysis`, `stockNews`, `MusicAI`, `Jupyter.Notebooks`, `local-meeting-transcriber`, `networking`, and `policy-pit-app`.
3. Keep merge-source apps out of separate product lanes: `tweetBetweenTheLines` + `twitter-therapy-app` into `social-media-analysis`; `wutHappened` into `stockNews`; `sleep-dream-app` into `journal-ai`; `music-mood-app` into `MusicAI`.
4. For script/security/private-data projects, deploy public docs/demo shells only; keep actual tools local/private unless explicitly hardened.
