# Submodule and Gitlink Mapping Health Report

## Scope

Audited the `projects/CombatAtlas` mapping and the complete gitlink/`.gitmodules`
relationship in the local `/opt/data/HeRmEz` superproject on 2026-09-02 at
07:42 UTC.

## CombatAtlas result

- Parent gitlink, local `main`, fetched `origin/main`, and the live GitHub
  `refs/heads/main` commit were identical at verification time. Exact hashes
  are intentionally omitted because committing this report advances the branch
  and parent pointer.
- `.gitmodules` URL and local `origin`:
  `https://github.com/ItMeansBigMountain/CombatAtlas.git`
- Nested gitlinks inside CombatAtlas: none

The CombatAtlas gitlink is initialized, correctly mapped, and synchronized.
The report files are tracked; there were no uncommitted differences before this
verification update.

## Superproject-wide findings

The superproject index currently has 27 gitlinks and `.gitmodules` has 11 path
mappings:

- 9 mappings correspond to initialized gitlinks. Their index commits match the
  checked-out submodule commits, and their configured URLs match local origins.
- 18 archive gitlinks have no `.gitmodules` mapping:
  `Generative-AI`, `HTML_REGEX`, `Kubernetes-Docker`, `Multiplayer`,
  `OptaPlanner`, `REST_Templates`, `React.web_userLoginForm`,
  `Spring_Boot_webDev`, `darkSouls-Unity`, `frequencyFinder.Hz`, `pdf-emailer`,
  `penTest`, `robinhood-daily-portfolio-report`,
  `security-research-source-monorepo`, `snake-REACT_NATIVE`, `spring_Oauth`,
  `spring_template`, and `wornly`.
- 2 `.gitmodules` paths (`projects/algos` and
  `projects/cox-elementary-pta`) have no corresponding index gitlink.
- No duplicate `.gitmodules` paths were found.
- A full `git submodule status` exits 128 at the first unmapped archive gitlink
  (`projects/_archive/Generative-AI`).

The parent workspace already contains staged deletions of
`projects/_archive/Financial.Market.ML` and `projects/_archive/Fintech`, plus
unrelated archive working-tree changes. This audit did not alter or overwrite
those pre-existing changes.

## Disposition

No CombatAtlas synchronization change is required. Repairing the historical
archive mappings and stale entries is a separate superproject cleanup decision:
either add authoritative mappings for the 18 archive gitlinks, or remove those
gitlinks from the parent index while preserving the standalone repositories.
That broad parent-repository operation was intentionally not performed from the
CombatAtlas-scoped workspace without explicit ownership of the existing staged
changes.