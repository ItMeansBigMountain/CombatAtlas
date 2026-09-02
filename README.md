# CombatAtlas — Martial Arts Drill Database

CombatAtlas is now a Vercel-ready React/Vite app with a bundled local martial arts drill atlas. The Vite and Expo clients intentionally ship the same catalog and media modules; `npm test` fails if either client drifts from the other.

An Expo source shell is available in `mobile/`. Web, iOS, and Android JavaScript exports are verified locally, but there are no signed/installable native builds yet. iPhone testing is supported through Expo Go; Android is export-only until an EAS build is published. It preserves the same 22-art catalog and 15 published drill guides, plus consent-first test ads and a receipt-verifying remove-ads boundary. See `mobile/README.md` for the exact support boundary and verification commands.

CI/CD, environment separation, release, and rollback procedures are documented in `RELEASE.md`. The canonical Vercel alias is `https://combatatlas-flame.vercel.app`; its current deployment-protection blocker is recorded there rather than hidden.

## Current shipped state

- 22 martial arts profiles across striking, grappling, weapons, traditional practice, self-defense, hybrid MMA, and movement arts.
- Minimal customer-facing homepage: universal search bar plus a clean martial arts grid.
- 15 individually named, art-specific drill guides are searchable and published with short instructions, coaching cues, difficulty, contact level, and YouTube demonstration search links.
- Search finds both martial arts and drills from one field.
- Each martial art and drill resolves to a visual illustration, so the product no longer depends on broken external image providers.
- Developer/source panels were removed from the public webpage.

## Why the database is bundled first

No single free public API appears to provide “every martial art drill.” The bundle retains 882 draft/generated source records for offline review, but customer search and art pages intentionally publish only the 15 individually curated guides. Draft templates must not be counted or presented as verified art-specific instruction.

## Optional future data/API enrichers

- Wikipedia MediaWiki category members for martial arts technique summaries — no key, CC BY-SA attribution required.
- Wikidata aliases/entity IDs — no key.
- Wikimedia Commons images/media — no key, license attribution required.
- Kaggle Grappling Techniques — free Kaggle username/key required.
- `ubershmekel/bjjdata` GitHub repo — no key, MIT clip/tag metadata.

## Commands

```bash
npm install
npm test
npm run build
npm run dev
npm run import:wikipedia
```

`npm run import:wikipedia` fetches no-key Wikipedia/MediaWiki technique records into `imports/wikipedia-techniques.json` for review/attribution before merging into the bundled seed database.

## Legacy backend

The original Django REST backend remains under `combatAtlas_Backend/` as archival legacy source. It is not the data source for either shipped client and its older relational schema is not API-compatible with the bundled catalog. The canonical product data is `src/data/combatData.js` plus `src/data/themeMedia.js`, mirrored under `mobile/src/data/` and guarded by `npm run validate:sync`. Do not treat Django records as synchronized production content unless a future migration introduces an explicit canonical import/export contract.
