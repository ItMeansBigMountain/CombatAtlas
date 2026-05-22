---
name: vercel-app-deployments
description: "Triage, deploy, and manually verify Vercel apps from existing project folders."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Vercel, deployment, frontend, preview, manual-testing]
    related_skills: [github-repo-management]
---

# Vercel App Deployments

Use this skill when auditing existing app folders for Vercel, redeploying Vercel projects, building a deployment URL tracker, or diagnosing why Vercel preview/production URLs are not manually testable.

## Principles

- Treat Vercel URLs as part of a manual testing workflow: record production URL, preview URL, alias/friendly URL, status, and notes in the workspace README.
- Never print or commit Vercel tokens, bypass tokens, environment values, or project secrets.
- Verify both deployment creation and anonymous/manual browser accessibility. A deployment can exist but still return `401 Unauthorized` due to deployment protection.
- Classify projects before deploying: frontend app, backend/API, monorepo, project plan/spec, or script/archive.

## Access check

Check for token/CLI without exposing secrets:

```bash
python - <<'PY'
import os
for n in ['VERCEL_TOKEN','VERCEL_API_TOKEN','VERCEL_ORG_ID','VERCEL_PROJECT_ID']:
    print(f'{n}=' + ('set' if os.getenv(n) else 'missing'))
PY
if command -v vercel >/dev/null 2>&1; then vercel --version; else echo 'vercel cli missing; use npx vercel'; fi
```

If the CLI is unavailable, use `npx vercel` or the REST API with the token from `VERCEL_TOKEN`/`VERCEL_API_TOKEN`.

Before a deploy, verify the token in the exact execution context that will run `npx vercel` (same terminal/session/workdir), because higher-level wrappers or different tool backends may have different environment injection. If neither `VERCEL_TOKEN` nor `VERCEL_API_TOKEN` is present there, stop after local build/preview verification and report the deploy-auth blocker without exposing secrets.

## Inventory existing Vercel projects via API

```bash
python - <<'PY'
import os, json, urllib.request
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
assert TOKEN, 'Missing Vercel token'
req=urllib.request.Request('https://api.vercel.com/v9/projects?limit=100', headers={'Authorization':'Bearer '+TOKEN})
data=json.load(urllib.request.urlopen(req, timeout=30))
for p in data.get('projects', []):
    latest=p.get('latestDeployments') or []
    print(p.get('name'), p.get('framework'), latest[0].get('url','') if latest else '')
PY
```

## Local project triage

For each candidate folder:

1. Look for `package.json`, `vercel.json`, lockfiles, framework configs, and sub-apps.
2. Read scripts and key dependencies:

```bash
node -e "let p=require('./package.json'); console.log(p.scripts||{}); console.log({...p.dependencies,...p.devDependencies})"
```

3. Run the least destructive local build/check available:
   - Create React App: `npm run build`
   - Vite: `npm run build`
   - Next.js: `npm run build`
   - Angular: `npm ci && npm run build`
   - Expo web: inspect Expo version; old SDKs often need dependency/export fixes before Vercel.
4. Note missing env vars from `.env.example`/templates by key name only, not value.
5. Decide whether backend/API components belong on Vercel serverless or a service better suited for long-running apps/databases (Render/Railway/Fly/etc.).
6. If a folder is only a README/SCOPE/PROJECT plan but the user asks to begin work across projects, do not leave it as inert triage. Pick the highest-leverage low-risk plan-only app and build the smallest Vercel-ready MVP from the stated scope, favoring static/local-first implementations that avoid credentials, payments, official trademarked assets, and databases until manual review proves value.

## Workspace deploy queue for many projects

When the user asks to review every project or create a work queue, create/update a durable queue document in the workspace (for this user's project workspace, `/opt/data/HeRmEz/projects/WORK_QUEUE.md`) with:

- an "Active now" ranked section,
- every project classified as live app, app scaffold, backend/API candidate, plan-only app, or script/archive,
- the current deployment path,
- the next work item,
- explicit blockers.

Keep `/opt/data/HeRmEz/projects/README.md` as the public URL tracker and `/opt/data/HeRmEz/projects/VERCEL_TRIAGE.md` as the detailed evidence log. The work queue is the operator view for choosing what to build next; the README is the review URL table.

## Deployment protection / 401 pattern

If a Vercel URL returns `401 Unauthorized` in anonymous checks, do **not** assume deployment failed. It usually means deployment protection/authentication is enabled or the public alias is not configured as expected.

Ask/resolve one of:

- disable deployment protection for manual testing,
- provide the intended public alias/domain,
- provide the approved Vercel deployment-bypass mechanism.

When the user approves disabling protection, patch each project with `ssoProtection: null` via the Vercel API, then re-test anonymously:

```bash
python - <<'PY'
import os,json,urllib.request
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
assert TOKEN, 'Missing Vercel token'
headers={'Authorization':'Bearer '+TOKEN,'Content-Type':'application/json'}
projects=json.load(urllib.request.urlopen(urllib.request.Request('https://api.vercel.com/v9/projects?limit=100',headers=headers),timeout=30)).get('projects',[])
for p in projects:
    name=p['name']
    req=urllib.request.Request(
        f'https://api.vercel.com/v9/projects/{name}',
        data=json.dumps({'ssoProtection': None}).encode(),
        headers=headers,
        method='PATCH',
    )
    detail=json.load(urllib.request.urlopen(req,timeout=30))
    print(name, 'ssoProtection=', detail.get('ssoProtection'))
PY
```

A Bearer Vercel API token is not necessarily enough to bypass deployment protection on the public app URL; verify with an anonymous request after changing settings.

## Free/SQLite backend defaults

For legacy projects, prefer the lowest-friction deploy path before asking for paid infrastructure:

- Frontend-only apps: Vercel static/site deployment, no database.
- Demo APIs: SQLite or bundled JSON/sample data.
- Prototype games/quizzes that only use accounts for high scores: remove login friction first; collect a display name after the game and post anonymous leaderboard rows. Add durable score storage later only if leaderboard persistence matters.
- Django/Flask apps with durable writes: SQLite on a host with persistent disk (Render/Railway/Fly/etc.) unless there is a reason to use serverless.
- Vercel serverless backends: avoid relying on local SQLite for durable writes; use read-only seed data or a free hosted DB.
- Firebase/Supabase: use only when the app needs hosted auth/realtime or already depends on it.

## HeRmEz legacy-project triage reference

For this user's imported legacy project workspace, see `references/hermez-vercel-triage.md` for the classification pattern, common user inputs, and README/triage-doc approach. See `references/hermez-imported-project-redeploys.md` for working redeploy patterns discovered while continuing the imported projects: linked Vercel redeploys, Express API subdirectory routing, Sequelize/MySQL serverless fixes, nested Expo web exports, anonymous HTTP verification, and tracker updates. See `references/hermez-static-mvp-reframe-and-card-intel.md` for the pattern of reframing a plan-only/legacy folder into a static Vite MVP, renaming misleading project folders, deploying with token fallback, disabling protection on newly-created projects, and verifying a Pokémon card price-scanner MVP. See `references/vercel-protection-and-free-data.md` for the exact Vercel `ssoProtection` API patch and free SQLite/sample-data planning pattern. See `references/oauth-and-third-party-credentials.md` for safely handling Spotify/Genius/Watson/Agora/Imgflip-style credentials, redirect URLs, and redacted status docs during deployment setup.

## Plan-only app reframes

When a project folder is mostly README/SCOPE/PROJECT scaffolding and the user changes the product direction, treat the latest user direction as the source of truth rather than preserving the imported legacy concept. If the old folder name is misleading and no deployed external integration depends on it yet, rename the folder and update project-local docs plus workspace trackers from the new path. Prefer a static Vercel-ready MVP using public/no-key APIs and browser-only logic before adding accounts, databases, or paid API keys. See `references/plan-only-app-reframes.md` for the detailed reframe workflow and pitfalls.

## URL tracker

Create/update a workspace README table like:

```markdown
| Project | Status | Vercel production / preview URL | Alias / friendly URL | Manual testing notes |
|---|---|---|---|---|
| my-app | Deployed / needs manual review | https://...vercel.app | https://my-app.vercel.app | Login works; mobile nav needs polish |
```

When the user explicitly deprioritizes or skips projects during triage, immediately mark those rows as `Skipped for now` (including paired API/backend rows), add a short note such as `User said to skip <project> for now`, and update the triage doc's recommended next order so future sessions do not keep resurfacing the skipped projects.

## Pitfalls

- Do not deploy every legacy folder blindly; many are specs/scripts, not apps.
- When the user changes a project direction, update/replace stale README/SCOPE/PROJECT/tracker text immediately and rename the folder if the old name will mislead future work.
- Do not commit `.vercel/`, `.env`, `node_modules`, build outputs, local DBs, or generated credentials.
- Do not expose Vercel tokens or protection bypass tokens in chat, commits, docs, or logs.
- Do not report a URL as manually testable until it returns a public 200/expected response or the user has a protection bypass path.
- For nested legacy apps, run the build/export/deploy command from the actual deployable subdirectory and verify `.vercel/project.json` there points at the intended Vercel project; parent and child folders can be linked to different projects.
- For Vercel serverless Express APIs, a successful deployment can still 404 if `vercel.json` does not route requests to the exported API app. Add explicit `builds`/`routes` for `api/index.js` when needed and then verify a known endpoint.
- If login/signup routes time out because a legacy serverless API defaults to localhost MySQL and no `DATABASE_URL`/`MYSQL_URL` exists, do not stop at “needs DB” when the user needs a live demo. Add a clearly documented demo-mode in-memory fallback that preserves the frontend response contract (for example, signup/login both return JWTs), then verify signup → login → private-route remotely. See `references/hermez-imported-project-redeploys.md`.
- For Sequelize/MySQL APIs on Vercel, `mysql2` in `package.json` may not be enough. If logs show “Please install mysql2 package manually,” require `mysql2` and pass `dialectModule: mysql2` in the Sequelize constructor.
- For Expo web apps, prefer `npx expo export --platform web` with `outputDirectory: "dist"`; if `export:web` fails, do not assume the app is undeployable — use the export command that matches the installed Expo SDK/bundler.
- For imported quiz/education apps whose question images are missing, duplicated placeholders, or unavailable in the web export, do not reflexively chase asset paths. If the user wants curriculum review, replace image prompts with deterministic rendered lesson/code cards and add source tests for curriculum coverage; see `references/hermez-imported-project-redeploys.md`.
