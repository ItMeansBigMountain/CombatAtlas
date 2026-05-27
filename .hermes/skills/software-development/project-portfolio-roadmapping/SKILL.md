---
name: project-portfolio-roadmapping
description: "Manage a workspace full of related projects: inventory, consolidate overlapping apps, capture product direction, update trackers, and create/retire repos safely."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [project-portfolio, roadmap, consolidation, inventory, trackers, repos, product-direction]
platforms: [linux, macos]
triggers:
  - inventory all projects
  - update project directions
  - merge these apps
  - remove this project
  - create a new repo after reviewing another repo
  - update trackers
  - project portfolio status
related_skills: [codebase-inspection, github-repo-management, writing-plans]
---

# Project Portfolio Roadmapping

Use this skill when the user is steering a workspace containing many apps/repos and asks to inventory, retire, merge, rename, scope, or create projects. The output should leave the workspace more organized, not just summarize opinions.

## Core Workflow

1. **Inspect before changing**
   - Check the relevant project folders, existing tracker docs, README inventories, and git status.
   - If a project references another repo/source, inspect that source before creating a new plan.
   - For imported code exercises or examples, check all branches; do not assume the default branch is complete.
   - For product-parity requests, research public official pages/portals and clearly separate public feature claims from user-provided operational knowledge.

2. **Translate user direction into durable artifacts**
   - Add or update `PRODUCT_DIRECTION.md`, `MERGE_INTO_*.md`, `*_PLAN.md`, or aggregate direction docs in the affected project folders.
   - Capture source-of-truth decisions in committed files, not only in chat.
   - Keep product direction practical: vision, merge/consolidation target, MVP flows, data inputs, safety/privacy boundaries, and next implementation steps.

3. **Handle project retirement deliberately**
   - Remove obsolete folders only when the user clearly asks to remove them.
   - Update all project trackers and URL lists to remove retired projects.
   - Preserve the deletion in git history via `git rm`/`git add -A`; do not leave stale tracker rows.

4. **Handle project consolidation clearly**
   - Pick one primary target app/repo.
   - In source apps, add `MERGE_INTO_<TARGET>.md` describing what to keep and what becomes archive/source material.
   - In the target app, add a richer `PRODUCT_DIRECTION.md` defining the combined product.
   - Update trackers so future inventory summaries show the merge status instead of treating all apps as unrelated active products.

5. **Create new repos only after source review**
   - If the user says “review X and make a new repo,” inspect X first and document what was reused.
   - Scaffold the smallest runnable/tested baseline.
   - Commit locally, create/push the remote, then add the new repo to workspace trackers or `.gitignore` if it is nested and managed separately.

6. **Verify and commit**
   - Run lightweight tests or validation for generated scaffolds.
   - Check `git status --short` before committing.
   - Commit and push when the user asked for repo/workspace updates.
   - Final response should include commit IDs, created/updated files, and concise next steps.

## Tracker Update Pattern

When a project direction changes, update the same set consistently:

- Project-specific direction/merge files.
- `PROJECT_REVIEW_SHEET.md`.
- `PROJECT_REVIEW_SHEET.csv` when present.
- Workspace `README.md` or project index.
- Aggregate direction/update log, if present.
- `.gitignore` for nested standalone repos that should not be swallowed by the parent repo.

## Product Direction File Shape

Use this default structure unless the project needs something else:

```md
# <Project> Direction

## Product vision

## Consolidation / relationship to other projects

## Target users

## Core flows

## Data inputs / integrations

## MVP screens or modules

## Safety, privacy, or compliance boundaries

## First implementation steps
```

## Research-Backed Product Parity Plans

When the user asks to replicate another business/app's customer portal or workflow:

- Use public research only unless the user provides their own operational context.
- Record sources and findings in a project-local research doc before/alongside the implementation plan.
- Translate competitor-branded concepts into original names.
- Build an end-to-end vertical slice instead of a feature dump.
- Include role matrix, schedule/client relationships, data model, reporting surfaces, and admin queues.
- For AI-assisted note extraction, require human review before extracted tags update official progress/history.

## User Preferences Observed

- The user often steers multiple legacy projects by explaining how they should merge or evolve. Convert those instructions into repo docs and tracker updates immediately.
- The user prefers momentum: remove what is no longer needed, document merged directions, scaffold new repos, test, commit, and push.
- Keep summaries concise and operational: what changed, where it was written, commit hash, and next build step.

## Pitfalls

- Don’t leave overlapping projects with ambiguous ownership after the user says they are “the same thing” or “can go together.” Create merge notes.
- Don’t capture only a chat summary; write the source-of-truth files inside the workspace.
- Don’t update Markdown but forget CSV/project trackers.
- Don’t nest a new standalone Git repo inside the parent workspace without adding it to the parent `.gitignore`.
- Don’t turn mental-health-adjacent products into diagnostic claims; use pattern/reflection language and safety boundaries.
- Don’t expose credentials, env values, or token-bearing command output while inspecting legacy projects.

## References

- `references/hermez-portfolio-2026-05.md` — session-specific example of retiring a project, merging apps, importing exercises from all branches, and creating a new standalone portfolio-report repo.
- `references/coding-school-crm-portal-research-2026-05.md` — research-backed product-parity pattern for a coding-school CRM with teacher schedules, AI lesson-note tagging, and parent/student progress dashboards.
- `references/hermez-consolidation-patterns-2026-05.md` — condensed merge/retire/new-repo patterns from the HeRmEz project-direction session, including stockNews+wutHappened and social-media app consolidation.
