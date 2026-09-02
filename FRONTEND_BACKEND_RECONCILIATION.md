# Frontend/backend reconciliation

Verified: 2026-09-02T07:42:16Z

## Result

No tracked frontend/backend discrepancy requires a code change.

The shipped Vite web client and Expo client intentionally use a bundled offline catalog rather than the Django REST API. Their canonical catalog and theme-media modules are byte-identical:

- `src/data/combatData.js` ↔ `mobile/src/data/combatData.js`
- `src/data/themeMedia.js` ↔ `mobile/src/data/themeMedia.js`

The legacy Django project under `combatAtlas_Backend/` remains internally healthy, but its relational API schema is not compatible with the bundled client schema. It is archival and is not imported by either shipped client. Connecting it directly would introduce drift rather than reconcile the current product. A future backend migration needs an explicit versioned API/import-export contract before either client switches data sources.

## Issues found

1. The Vite production bundle is about 2.25 MB before gzip and emits Vite's chunk-size warning. This does not break the build; most of the weight is the bundled offline catalog. It should be handled as a performance optimization, not as a frontend/backend mismatch.
2. `submodule-health-report.md` was already untracked before this reconciliation. It documents repository mapping health and was not modified by this task.
3. There are no signed native iOS/Android builds. Expo web export works; installable native delivery remains outside this reconciliation scope.

## Verification

From the repository root:

- `npm test` — passed catalog, customer-experience, and Vite/Expo mirror checks.
- `npm run lint` — passed syntax/JSON checks for 33 files.
- `npm run build` — passed Vite production build, with the non-blocking chunk-size warning noted above.
- `cmp -s src/data/combatData.js mobile/src/data/combatData.js` — identical.
- `cmp -s src/data/themeMedia.js mobile/src/data/themeMedia.js` — identical.

From `mobile/`:

- `npm test` — 6/6 passed.
- `npx expo export --platform web --output-dir /tmp/combatatlas-mobile-web-verify` — exported successfully.

From `combatAtlas_Backend/combatAtlas_Backend/`:

- `../.venv/bin/python manage.py check` — no issues.
- `../.venv/bin/python manage.py test` — 3/3 passed.

Git alignment:

- Local `HEAD`, fetched `origin/main`, live `refs/heads/main`, and the HeRmEz
  parent gitlink were identical when this verification began. Exact commit
  hashes are intentionally omitted because committing this report advances the
  branch and parent pointer.
