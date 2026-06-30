---
name: software-project-delivery
description: "Use when delivering software projects end-to-end: portfolio inventory, app scaffolding, domain-specific product builds, debugging, QA, docs, repo hygiene, deployment handoff, and verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, project-delivery, portfolio, django, scanners, runelite, debugging, qa, deployment]
    related_skills: [test-driven-development, software-quality-workflows, github-repo-management, github-pr-workflow, codebase-inspection]
---

# Software Project Delivery

## Overview

This umbrella covers building, debugging, organizing, and shipping software projects as working artifacts. Use it when the user's request spans product direction, repo/workspace hygiene, implementation, testing, deployment, or handoff. It also preserves detailed playbooks for several recurring product classes: client-editable Django sites, collectible card scanner apps, OSRS/RuneLite plugins, browser-based QA, and Node inspector debugging.

The default standard is: inspect first, implement the smallest useful slice, verify with real commands or browser checks, document operational handoff, then commit/push when requested.

## When to Use

- Inventorying, consolidating, retiring, or creating repos in a project portfolio.
- Turning a product brief or static mockup into a runnable app.
- Building domain-specific apps where prior experiential notes exist: Django admin-backed client sites, card scanner/price-intelligence apps, or OSRS RuneLite plugins.
- Debugging Node/TypeScript/React/Ink behavior with real breakpoints instead of guesswork.
- Running exploratory browser QA and producing evidence-backed bug reports.
- Updating trackers, README files, product direction docs, deployment guides, or client handoff docs.

## Universal Delivery Workflow

1. **Inspect before changing.** Read project files, trackers, README/direction docs, git status, and relevant branches or child repos.
2. **Classify the job.** Is this a portfolio decision, new scaffold, feature slice, bugfix, QA pass, deployment, or handoff?
3. **Write or update source-of-truth docs.** Use `PRODUCT_DIRECTION.md`, `MERGE_INTO_*.md`, `DEVELOPMENT_PLAN.md`, `DEVELOPER_CHEATSHEET.md`, trackers, or client guides where appropriate.
4. **Implement a vertical slice.** Prefer a small working feature with tests over broad unverified scaffolding.
5. **Verify with real execution.** Run tests/builds, start servers, fetch endpoints, inspect browser console, or attach a debugger as needed.
6. **Protect credentials and nested repos.** Never print `.env` values; keep standalone child repos ignored/submodule-managed if nested under a parent workspace.
7. **Commit/push when requested.** Do not claim code is pullable until `git push` has succeeded.

## Portfolio and Roadmapping

For this user's project portfolio, first load `references/user-project-portfolio-operating-model.md`; it captures the retire/set-aside handoff pattern, app-domain classifications, and Vercel end-user review preference.

For workspaces with many related projects:

- Update the same artifacts consistently: project-local docs, `PROJECT_REVIEW_SHEET.md`, CSV trackers, workspace README/indexes, aggregate update logs, and `.gitignore` for nested repos.
- When projects overlap, choose a primary target app and add merge notes to sources.
- When a project is only a plan/static review shell, do not run installs or redeploys; recommend restoring source or scaffolding the documented MVP first.
- For product-parity research, record public sources and translate competitor concepts into original names.
- For this user's project portfolio statuses and durable buckets (finished/set aside, ship/operate, incubate, upcoming OSRS lane, archive/freeze), see `references/user-project-portfolio-status-2026-06-29.md`.

## Domain Playbooks

### Client-editable Django sites

Use Django admin as the first CMS for community, nonprofit, PTA, small-business, or client-owned content sites.

- Model recurring content: newsletters, events, announcements/flyers, volunteer opportunities, resources, membership, sponsors, fundraising, and site settings.
- Prefer Stripe Payment Links before custom checkout.
- Deploy to a Python host such as Render/Railway/Fly/PythonAnywhere; GitHub Pages is static-only.
- Write client admin and deployment docs, including admin URL, content publishing workflow, env vars, database/static files, and custom domain steps.
- Verify tests, migrations, public pages, `/admin/`, and uploaded-media behavior in local or staging.

### Collectible card scanner and price-intelligence apps

Treat lookup as the baseline and video/AR overlay as the product direction.

- Start with OCR or manual search fallback, then normalize multi-source price rows.
- Preserve condition/grade assumptions (`raw-nm`, `raw-lp-mp`, `graded-8/9/10`, etc.) and save them with watchlist entries.
- For video, sample frames and stabilize predictions before rendering overlays; do not OCR every frame blindly.
- Show source, recency, confidence, and marketplace spread instead of one opaque price.

### OSRS / RuneLite plugins

For OSRS plugins, each child plugin should be its own Gradle/RuneLite repo under the user's portfolio container.

- Use Java 11 and verified boilerplate; run `./gradlew clean test assemble --no-daemon`.
- Keep Old School RuneScape sources separate from RuneScape 3; use OSRS Wiki and RuneLite item IDs.
- RuneLite side panels must fit narrow UI constraints; test long names and result states for overflow.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.

### Node inspect debugging

When `console.log` is not enough:

- Start with `node inspect` or `node --inspect-brk`; use PTY/background process handling for interactive stepping.
- Use `sb(...)`, `cont`, `bt`, `repl`, and `exec` to inspect locals and call stacks.
- For scripted CDP, install `chrome-remote-interface` in a throwaway path and drive breakpoints/scope capture programmatically.
- Prefer `--inspect-brk` when first-breakpoint timing matters; bind inspector to `127.0.0.1` unless isolated.

### Exploratory web QA / dogfood

For QA passes:

1. Build a scope/sitemap.
2. Navigate pages with browser tools.
3. Check console after every navigation and significant interaction.
4. Capture screenshot evidence for every issue.
5. Classify by severity/category and produce a structured report.

## Support Package Index

Archived source packages absorbed into this umbrella are preserved under `references/absorbed/<old-skill-name>/` when available:

- `client-editable-django-sites/` — full Django CMS/site playbook, Render deployment references, and admin templates.
- `collectible-card-scanner-apps/` — scanner, OCR, condition-lens, watchlist, and AR-overlay notes.
- `dogfood/` — browser QA workflow, issue taxonomy, and report template.
- `node-inspect-debugger/` — Node inspector and CDP debugging recipes.
- `osrs-plugins/` — RuneLite plugin portfolio, scaffolding, API, UI, and plugin-hub references.
- `project-portfolio-roadmapping/` — workspace inventory, merge/retire, tracker, and source-of-truth documentation patterns.

## Common Pitfalls

1. Summarizing without writing durable project artifacts when the user asked to organize or steer a portfolio.
2. Calling a static shell a working app because a public URL returns HTTP 200.
3. Claiming deployment or push success without verifying the remote or endpoint.
4. Ignoring support files when consolidating a project-specific skill into this umbrella.
5. Printing secret values while inspecting env files.
6. Using generic web-app advice when a domain playbook has concrete constraints and verification commands.

## Verification Checklist

- [ ] Existing project state, docs, trackers, and git status inspected.
- [ ] Domain-specific subsection and absorbed references checked when relevant.
- [ ] Code/docs changed in the right repo or workspace boundary.
- [ ] Tests/builds/browser checks/debugger evidence run as appropriate.
- [ ] Credentials redacted and nested repo hygiene preserved.
- [ ] Final response names changed files, commands run, and remaining blockers.
