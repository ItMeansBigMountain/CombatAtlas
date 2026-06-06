# Kanban Project Review PBIs

Generated: 2026-06-06T01:58:47Z

Purpose: durable PBIs for reviewing every project in `/opt/data/HeRmEz/projects`, testing unfinished work, attempting Vercel deployment where appropriate, browser smoke-testing live UI, and routing fixes through subagents until done.

## Operating rules

- Use Kanban as source of truth; each project gets one review/deploy/smoke-test PBI.
- Do not expose or commit credentials/secrets.
- For deployable apps: inspect source, run local tests/build, deploy/redeploy on Vercel, verify anonymous HTTP, then click through the UI in browser.
- For plan-only folders: create an honest minimal Vercel review shell only when it is useful and label it clearly as an MVP/review shell.
- For backend/API candidates: verify health/API routes and decide whether Vercel serverless is appropriate; otherwise block with exact hosting/env requirement.
- Every PBI should finish with tracker updates: README URL table, WORK_QUEUE.md, VERCEL_TRIAGE.md, and project-local notes if needed.
- If smoke testing finds bugs, create child fix PBIs and keep working until the app is shippable or blocked by a real external credential/legal decision.

## Seeded PBIs

1. **3d-react-web** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md — deployable package markers: 1
2. **addictive-mobile-games** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
3. **algos** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
4. **api.requests** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
5. **az204** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
6. **card-intel-scanner** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md — deployable package markers: 1
7. **cellphone_scripts** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
8. **CloudAutomation** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
9. **coding-school-platform** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
10. **Codology** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md, PRODUCT_DIRECTION.md — deployable package markers: 3
11. **CombatAtlas** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md — deployable package markers: 1
12. **consumer-advocate-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
13. **cox-elementary-pta** — backend/API or script candidate — assignee seed: `default` — markers: requirements.txt, manage.py, README.md — deployable package markers: 0
14. **deployment_docs** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
15. **docs** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
16. **faceless-youtube-channel** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md — deployable package markers: 1
17. **honda-tech-upgrade** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
18. **journal-ai** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
19. **Jupyter.Notebooks** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
20. **legacy-src** — Vercel/frontend candidate — assignee seed: `default` — markers: none — deployable package markers: 6
21. **local-meeting-transcriber** — plan-only/product candidate — assignee seed: `researcher` — markers: PRODUCT_DIRECTION.md — deployable package markers: 0
22. **muscleMadness** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json — deployable package markers: 1
23. **muscleMadness_API** — backend/API or script candidate — assignee seed: `default` — markers: manage.py — deployable package markers: 0
24. **music** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
25. **music-mood-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
26. **MusicAI** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, requirements.txt, README.md, PRODUCT_DIRECTION.md — deployable package markers: 1
27. **networking** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
28. **osrs-plugins** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
29. **osrs-plugins-beers** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
30. **osrs-plugins-boilerplate** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
31. **oyama-productions-legal** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
32. **plugin-hub** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
33. **policy-pit-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
34. **portfolio-sentiment-subscription-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
35. **robinhood-daily-portfolio-report** — backend/API or script candidate — assignee seed: `default` — markers: pyproject.toml, README.md — deployable package markers: 0
36. **robinhood-email-reports** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
37. **RTS-JS-ChatRooms** — backend/API or script candidate — assignee seed: `default` — markers: requirements.txt, README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
38. **school** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
39. **scraper-project** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
40. **selenium** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
41. **sleep-dream-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
42. **social-media-analysis** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
43. **stockNews** — Vercel/frontend candidate — assignee seed: `default` — markers: PRODUCT_DIRECTION.md — deployable package markers: 1
44. **store-code-content-studio** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
45. **survey-analytics-website** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
46. **ticVoter** — Vercel/frontend candidate — assignee seed: `default` — markers: package.json, vercel.json, README.md — deployable package markers: 1
47. **ticVoter_REST.api** — backend/API or script candidate — assignee seed: `default` — markers: requirements.txt, manage.py — deployable package markers: 0
48. **tiktok-clone** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
49. **tiktok-shop-shopify-commerce** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
50. **tournament-wager-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
51. **tutoring.Repl** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
52. **tweet_video_generator** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
53. **tweetBetweenTheLines** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
54. **twitter-therapy-app** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
55. **utilityScripts** — script/archive/classification needed — assignee seed: `researcher` — markers: none — deployable package markers: 0
56. **viral-clip-radar** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0
57. **watsonAI** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
58. **WebCrawl** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md — deployable package markers: 0
59. **wutHappened** — backend/API or script candidate — assignee seed: `default` — markers: requirements.txt, PRODUCT_DIRECTION.md — deployable package markers: 0
60. **youtube-high-ticket-leverage** — plan-only/product candidate — assignee seed: `researcher` — markers: README.md, PRODUCT_DIRECTION.md — deployable package markers: 0

## Kanban seed status

Updated: 2026-06-06T02:05:29Z

- Project PBIs seeded: 60
- Recovery controller: `t_d328547f` (running, assignee `default`) — `Orchestrate HeRmEz project sweep batches (no-skill recovery controller)`
- Dispatcher nudge cron: `6265cf005534` every 10 minutes, local/silent delivery, script `/opt/data/scripts/kanban_dispatch_hermez_sweep.sh`.
- Dispatch log: `/opt/data/HeRmEz/projects/KANBAN_SWEEP_DISPATCH.log`.

### PBI task IDs

- `t_fb7d38a6` — **3d-react-web** — todo — `default`
- `t_5ffd0b4e` — **addictive-mobile-games** — todo — `default`
- `t_bcb3f38b` — **algos** — todo — `default`
- `t_cb2a4f56` — **api.requests** — todo — `default`
- `t_a1be0e97` — **az204** — todo — `default`
- `t_e8f1b4dc` — **card-intel-scanner** — todo — `default`
- `t_c8931927` — **cellphone_scripts** — todo — `default`
- `t_4a190fd2` — **CloudAutomation** — todo — `default`
- `t_903498ae` — **coding-school-platform** — todo — `default`
- `t_6942e669` — **Codology** — triage — `default`
- `t_de2213f1` — **CombatAtlas** — triage — `default`
- `t_d1b5f465` — **consumer-advocate-app** — triage — `researcher`
- `t_a69f234b` — **cox-elementary-pta** — triage — `default`
- `t_a1cb039b` — **deployment_docs** — triage — `researcher`
- `t_20581a08` — **docs** — triage — `researcher`
- `t_a629c96f` — **faceless-youtube-channel** — triage — `default`
- `t_5fa1deba` — **honda-tech-upgrade** — triage — `researcher`
- `t_187eae4f` — **journal-ai** — triage — `researcher`
- `t_39a4a6c0` — **Jupyter.Notebooks** — triage — `researcher`
- `t_952d692f` — **legacy-src** — triage — `default`
- `t_410eef4c` — **local-meeting-transcriber** — triage — `researcher`
- `t_2b9d825b` — **muscleMadness** — triage — `default`
- `t_637bd506` — **muscleMadness_API** — triage — `default`
- `t_59869bc2` — **music** — triage — `researcher`
- `t_e6da1cc0` — **music-mood-app** — triage — `researcher`
- `t_625538a3` — **MusicAI** — triage — `default`
- `t_6f9d3ccc` — **networking** — triage — `researcher`
- `t_d381978a` — **osrs-plugins** — triage — `researcher`
- `t_4f3516b2` — **osrs-plugins-beers** — triage — `researcher`
- `t_f98f9efb` — **osrs-plugins-boilerplate** — triage — `researcher`
- `t_7083d7d5` — **oyama-productions-legal** — triage — `researcher`
- `t_eb1a4a5c` — **plugin-hub** — triage — `researcher`
- `t_af027fe6` — **policy-pit-app** — triage — `researcher`
- `t_18aabe58` — **portfolio-sentiment-subscription-app** — triage — `researcher`
- `t_4ee645ca` — **robinhood-daily-portfolio-report** — triage — `default`
- `t_86ed43bd` — **robinhood-email-reports** — triage — `researcher`
- `t_431c21dd` — **RTS-JS-ChatRooms** — triage — `default`
- `t_ad6af343` — **school** — triage — `researcher`
- `t_24c32146` — **scraper-project** — triage — `researcher`
- `t_61c18329` — **selenium** — triage — `researcher`
- `t_88de66e5` — **sleep-dream-app** — triage — `researcher`
- `t_0981feee` — **social-media-analysis** — triage — `researcher`
- `t_1df4ed1c` — **stockNews** — triage — `default`
- `t_c82084c7` — **store-code-content-studio** — triage — `researcher`
- `t_626a1a97` — **survey-analytics-website** — triage — `researcher`
- `t_1f2e480b` — **ticVoter** — triage — `default`
- `t_b89baa68` — **ticVoter_REST.api** — triage — `default`
- `t_887ea690` — **tiktok-clone** — triage — `researcher`
- `t_8c19d45d` — **tiktok-shop-shopify-commerce** — triage — `researcher`
- `t_90b47bec` — **tournament-wager-app** — triage — `researcher`
- `t_bf625e0c` — **tutoring.Repl** — triage — `researcher`
- `t_48694b08` — **tweet_video_generator** — triage — `researcher`
- `t_6efc3dec` — **tweetBetweenTheLines** — triage — `researcher`
- `t_c3123ee1` — **twitter-therapy-app** — triage — `researcher`
- `t_76b45244` — **utilityScripts** — triage — `researcher`
- `t_23ae6bd0` — **viral-clip-radar** — triage — `researcher`
- `t_a7bcc5eb` — **watsonAI** — triage — `researcher`
- `t_cf3e50b0` — **WebCrawl** — triage — `researcher`
- `t_495fdc0f` — **wutHappened** — triage — `default`
- `t_4629da33` — **youtube-high-ticket-leverage** — triage — `researcher`
