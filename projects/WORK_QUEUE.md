# HeRmEz Project Review + Vercel Deploy Queue

Purpose: review every project, turn viable candidates into live Vercel demos, and keep non-deployable/script folders from stealing cycles.

Last updated: 2026-05-26

## Operating rule

1. Classify project: live app / app scaffold / backend-only / plan-only / script/archive.
2. Run local build or create smallest Vercel-ready MVP from the scope.
3. Deploy to Vercel when credentials are available.
4. Verify anonymous HTTP access.
5. Update `README.md` and `VERCEL_TRIAGE.md` with URL + blocker notes.

## Active now

| Rank | Project | Status | Next action | Blocker |
|---:|---|---|---|---|
| 1 | `card-intel-scanner` | Deployed/public; condition lens + local watchlist added | Mobile camera/OCR review on real cards; next add recorded-video sampling + stabilized AR confidence | none |
| 2 | `3d-react-web` | Deployed/public | Browser visual pass + polish issues | none |
| 3 | `Codology` | Deployed/public | Manual product review + durable leaderboard decision | optional DB only |
| 4 | `stockNews` | Deployed/public | Manual product review + IBM Watson/Durable auth decision | optional credentials/DB |
| 5 | `consumer-advocate-app` | Plan-only | Build a no-login landing/demo analyzer MVP | implementation needed |

## Every project queue

| Project | Class | Current deployment path | Work item |
|---|---|---|---|
| `3d-react-web` | Live frontend | Already on Vercel | Browser review; polish bundle/dependency warnings |
| `CloudAutomation` | Script/archive | Not Vercel as-is | Wrap into dashboard only if productized |
| `Codology` | Live frontend + API | Already on Vercel | Manual review; decide durable leaderboard storage |
| `CombatAtlas` | Backend/API | Needs host decision | Add requirements/prod settings or choose Render/Railway |
| `Jupyter.Notebooks` | Archive/notebooks | Not Vercel as-is | Extract a dashboard if useful |
| `MusicAI` | Flask/integrations | Possible demo | Decide reduced demo vs Spotify/Genius/Watson credentials |
| `RTS-JS-ChatRooms` | Flask + Agora client | Possible with config | Needs Agora config or demo-mode refactor |
| `WebCrawl` | Script/archive | Not Vercel as-is | Wrap as web crawler dashboard if useful |
| `addictive-mobile-games` | Plan-only | Build MVP | Choose first game and ship static demo |
| `api.requests` | Script/archive | Not Vercel as-is | Keep as utility unless productized |
| `bitcoin-bike-startup` | Plan-only | Build MVP | Landing + waitlist/static pricing prototype |
| `cellphone_scripts` | Script/archive | Not Vercel as-is | Keep utility; no deploy priority |
| `coding-school-platform` | Plan-only | Build MVP | Student progress/lesson landing prototype |
| `consumer-advocate-app` | Plan-only | Build MVP | Terms simplifier UX demo; no backend first |
| `cox-elementary-pta` | Django site | Render, not Vercel | Separate maintenance lane |
| `deployment_docs` | Docs | Not app | Keep docs only |
| `docs` | Docs | Not app | Keep docs only |
| `honda-tech-upgrade` | Plan-only | Build MVP | Mileage/maintenance static prototype |
| `journal-ai` | Plan/imported legacy | Build MVP | Local-first journal shell; AI optional later |
| `legacy-src` | Archive source | Not direct deploy | Mine for app code only |
| `local-meeting-transcriber` | Local utility | Not Vercel as-is | Desktop/local-first; deploy only as docs/demo |
| `muscleMadness` | Expo app | Skipped per prior direction | Leave skipped until user reactivates |
| `muscleMadness_API` | Backend | Skipped per prior direction | Leave skipped until user reactivates |
| `music` | Archive | Not Vercel as-is | No deploy priority |
| `music-mood-app` | Plan-only | Build MVP | Mood playlist UX shell; integrations later |
| `networking` | Archive | Not Vercel as-is | No deploy priority |
| `oyama-productions-legal` | Plan-only | Build MVP | Professional legal/production landing page |
| `card-intel-scanner` | Static React/Vite card scanner MVP | Deployed/public | Condition/grading selector and local watchlist shipped; next real-card mobile review + recorded-video AR sampling |
| `policy-pit-app` | Plan/continuation | Needs source inspection | Locate existing policy.pit.app repo/code before rebuild |
| `portfolio-sentiment-subscription-app` | Plan + legacy source | Build MVP | Tie to `stockNews` or separate subscription shell |
| `robinhood-email-reports` | Automation/reporting | Not Vercel as-is | Build reporting dashboard only after data path defined |
| `school` | Archive | Not Vercel as-is | No deploy priority |
| `scraper-project` | Scraper/archive | Not Vercel as-is | Build dashboard if crawler output is valuable |
| `selenium` | Automation/archive | Not Vercel as-is | No deploy priority |
| `sleep-dream-app` | Plan-only | Build MVP | Dream journal + sleep score prototype |
| `social-media-analysis` | Plan-only | Build MVP | Static analytics mock + upload/manual input |
| `stockNews` | Live frontend + API | Already on Vercel | Manual review; optional IBM Watson credentials |
| `store-code-content-studio` | Plan + legacy source | Build MVP | Store/code content workflow dashboard |
| `survey-analytics-website` | Plan-only | Build MVP | Survey upload/results static demo |
| `ticVoter` | Expo app | Skipped per prior direction | Leave skipped until user reactivates |
| `ticVoter_REST.api` | Backend | Skipped per prior direction | Leave skipped until user reactivates |
| `tiktok-clone` | Plan-only | Build MVP | Static feed/editor prototype |
| `tiktok-shop-shopify-commerce` | Plan-only | Build MVP | Commerce landing/admin mock |
| `tournament-wager-app` | Plan-only/high-risk | Build after risk review | Payments/legal risk surface first |
| `tutoring.Repl` | Bot/scripts | Not Vercel as-is | Wrap tutoring UX only if productized |
| `tweetBetweenTheLines` | Django/social app | Possible with credentials | Requirements/prod settings + social API decisions |
| `tweet_video_generator` | Media script | Not Vercel as-is | Productize as generator UI later |
| `twitter-therapy-app` | Plan-only | Build MVP | Local-first text reflection prototype |
| `utilityScripts` | Scripts | Not Vercel as-is | No deploy priority |
| `watsonAI` | Scripts/integration | Not Vercel as-is | Needs IBM credentials/demo shell |
| `wutHappened` | Generation scripts | Not Vercel as-is | Convert into web app before deploy |

## Current operator status

Vercel credentials are available in the execution environment. The next bottleneck is not authentication; it is deciding which deployed demos should be promoted from static review shells into real product MVPs, and which merge/archive folders should stay out of the active build lane.
