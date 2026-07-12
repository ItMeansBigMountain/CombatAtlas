# OSRS Plugin Cleanup Plan

## Current decisions

- `BisLoadouts` is the canonical boss/PvM gear recommendation plugin and is in PR review pending.
- Keep `WhosGrindingPanel` / `WhosGrindingClanPanel` as the standalone social grinding plugin.
- Keep `IceBarrageTimer` as the PvP freeze/teleblock timing utility.
- Keep `CompetitionOverlay` as the remaining competition surface for now.
- Keep `_templates/osrs-plugins-boilerplate` as the RuneLite starter template/reference, not an active plugin product.
- Scrap/remove `PersonalProgressTimeline`, `RivalRadar`, and `SmartHiscoreLookup`; the user no longer wants those project ideas.

## Active parent submodules after cleanup

- `projects/osrs-plugins/pr-review-pending/BisLoadouts` -> `bis-loadouts-osrs`
- `projects/osrs-plugins/pr-review-pending/WhosGrindingClanPanel` -> `whos-grinding-clan-panel-osrs`
- `projects/osrs-plugins/in-progress/IceBarrageTimer` -> `ice-barrage-timer-osrs`
- `projects/osrs-plugins/in-progress/CompetitionOverlay` -> `competition-overlay-osrs`
- `projects/osrs-plugins/_templates/osrs-plugins-boilerplate` -> `osrs-plugins-boilerplate-osrs`
- `projects/plugin-hub` -> `plugin-hub`

## Removed from parent submodules

- GroupIronProgressBoard
- AccountLegacyCard
- NameChangeWatcher
- SkillNemesis
- SkillRaceCreator
- BossRaceCreator
- BossKCRivalLookup
- BossStreaks
- SkillStreaks
- PersonalProgressTimeline
- RivalRadar
- SmartHiscoreLookup
- osrs-plugins-boilerplate from the top-level active plugin folder; it lives under `_templates/` instead

## Remote cleanup completed

Do not delete or archive additional GitHub repositories without explicit final confirmation.

Deleted unused OSRS remotes:

- `group-iron-progress-board-osrs`
- `account-legacy-card-osrs`
- `name-change-watcher-osrs`
- `skill-nemesis-osrs`
- `skill-race-creator-osrs`
- `skill-streaks-osrs`
- `boss-race-creator-osrs`
- `boss-k-c-rival-lookup-osrs`
- `boss-streaks-osrs`
- `clan-grind-heatmap-osrs`
- `breach-check-osrs`
- `personal-progress-timeline-osrs`
- `rival-radar-osrs`
- `smart-hiscore-lookup-osrs`

Remaining OSRS/plugin-related remotes after cleanup should be:

- `bis-loadouts-osrs`
- `competition-overlay-osrs`
- `ice-barrage-timer-osrs`
- `osrs-plugins-boilerplate-osrs`
- `plugin-hub`
- `whos-grinding-clan-panel-osrs`

## Git/submodule cleanup rules

- For removed plugin submodules, use `git submodule deinit -f <path>` then `git rm -f <path>` in the parent repo and remove the `.gitmodules` section.
- Remove stale `.git/modules/<path>` directories after submodule removal.
- Do not force-push parent HeRmEz; rebase or merge remote changes safely.
- Preserve unrelated dirty work from automation/video/trading projects.
- Stage exact OSRS paths only from `/opt/data/HeRmEz`; do not use broad `git add .` in the HeRmEz parent workspace.

## Concrete next implementation order

1. Keep polishing/submitting `BisLoadouts` from PR review pending.
2. Keep `WhosGrindingClanPanel` as the other main RuneLite plugin lane.
3. Only revisit `IceBarrageTimer` or `CompetitionOverlay` if the user asks.
4. Fix `projects/viral-clip-radar` submodule mapping separately from OSRS work.
