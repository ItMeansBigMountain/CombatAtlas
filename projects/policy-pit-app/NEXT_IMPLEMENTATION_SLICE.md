# Policy.pit.app - Current State and Next Implementation Slice

- **Created:** 2026-05-03
- **Runner:** Heartbeat
- **Project path:** `C:\Users\faree\Desktop\OpEnCLAw\policy-pit-app`

## Inspection result

The project directory currently contains only scaffold files:

- `.env`
- `.env.example`
- `.gitignore`
- `PROJECT.md`
- `README.md`

No application source code, package manifest, git repository, backend, frontend, or database schema was found in the project directory.

A bounded Desktop search for policy/pit-related directories found only this scaffold as the relevant project location. If older source exists elsewhere, Affan needs to point to that repo/path before code continuation can happen.

## Current blocker

Existing Policy.pit.app code location is not present under:

```text
C:\Users\faree\Desktop\OpEnCLAw\policy-pit-app
```

This blocks true continuation of prior implementation work.

## Smallest safe next implementation slice

If no existing repo is provided, start with a fresh MVP skeleton rather than guessing old architecture.

### Recommended slice: static policy search MVP

Build a minimal local web app that can:

1. Load policy documents from local sample data.
2. Display a search box.
3. Return matching policy snippets by keyword.
4. Show source title, category, and short excerpt.
5. Keep all config env-driven.

### Why this slice

- It is useful without accounts, secrets, scraping, or external APIs.
- It creates the core product loop: policy corpus -> user query -> ranked answer/snippet.
- It can later evolve into RAG, uploads, citations, subscription access, or admin tools.

## Suggested stack

Use one boring stack first:

- **Frontend:** Next.js + TypeScript
- **Styling:** plain CSS or Tailwind later
- **Data:** local JSON file first
- **Search:** in-memory keyword scoring first
- **Future:** embeddings/RAG only after local search works

## Proposed files for first code pass

```text
package.json
src/app/page.tsx
src/app/globals.css
src/lib/policies.ts
src/data/sample-policies.json
.env.example
README.md
```

## Required env variables

For the first local-only MVP:

```text
APP_ENV=development
NEXT_PUBLIC_APP_NAME=Policy.pit.app
POLICY_DATA_SOURCE=local
```

Future optional variables, not needed for first slice:

```text
OPENAI_API_KEY=
DATABASE_URL=
AUTH_SECRET=
STRIPE_SECRET_KEY=
```

## Validation for first implementation slice

Once code is created:

```powershell
npm install
npm run dev
```

Then verify:

- Local page loads.
- Search input filters sample policy results.
- No secrets are committed.
- `.env.example` contains only variable names/placeholders.

## Decision needed

Before implementation, choose one:

1. **Continue existing repo:** provide the real Policy.pit.app source path.
2. **Start fresh MVP:** create the Next.js local-search skeleton in this scaffold directory.

Recommendation: if the old repo is not immediately available, start fresh with the local-search MVP. Boring first loop, then sharpen it.
