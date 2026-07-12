# OSRS Plugin Cleanup Plan

## Current decisions

- Remove `GroupIronProgressBoard`; user does not want ironman/GIM-focused plugins.
- Remove thin/overlapping source repos from the parent HeRmEz workspace once their product direction is captured in the canonical repos.
- Keep `RivalRadar` as the canonical repo for race/streak/rival/competition consolidation.
- Make `SmartHiscoreLookup` the canonical account/player intel repo.
- Keep `WhosGrindingPanel` standalone. It should implement similar account-detail functionality locally rather than depending on SmartHiscoreLookup.
- `BisLoadouts` is the canonical name/repo for the former boss readiness gear recommendation plugin (`bis-loadouts-osrs`).

## Active parent submodules after cleanup

- WhosGrindingClanPanel / WhosGrindingPanel
- SmartHiscoreLookup / Account Intel
- RivalRadar
- BisLoadouts
- IceBarrageTimer
- PersonalProgressTimeline
- CompetitionOverlay
- `_templates/osrs-plugins-boilerplate` as the RuneLite starter template/reference, not an active plugin product

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
- osrs-plugins-boilerplate from the top-level active plugin folder; it lives under `_templates/` instead

The removed child repositories are no longer cloned by default from the HeRmEz parent workspace. Unused OSRS GitHub remotes listed below were deleted after user confirmation.

## Remote cleanup completed

Do not delete or archive additional GitHub repositories without explicit final confirmation. Current consolidation state:

- Keep active/canonical remotes: `bis-loadouts-osrs`, `whos-grinding-clan-panel-osrs`, `rival-radar-osrs`, `smart-hiscore-lookup-osrs`, `ice-barrage-timer-osrs`, `personal-progress-timeline-osrs`, `competition-overlay-osrs`, `plugin-hub`, and `_templates/osrs-plugins-boilerplate`.
- Deleted unused remotes: `group-iron-progress-board-osrs`, `account-legacy-card-osrs`, `name-change-watcher-osrs`, `skill-nemesis-osrs`, `skill-race-creator-osrs`, `skill-streaks-osrs`, `boss-race-creator-osrs`, `boss-k-c-rival-lookup-osrs`, `boss-streaks-osrs`, `clan-grind-heatmap-osrs`, and `breach-check-osrs`.

## Merge direction: SmartHiscoreLookup

- AccountLegacyCard
- NameChangeWatcher

Merged feature target:

- local account card
- player lookup panel
- hiscore links
- previous/current name detection
- external tracker enrichment from OSRS APIs

## Merge direction: RivalRadar

- SkillNemesis
- SkillRaceCreator
- BossRaceCreator
- BossKCRivalLookup
- BossStreaks
- SkillStreaks

Merged feature target:

- rival comparison
- skill/boss races
- skill/boss streaks
- nemesis/weakness analysis
- competition-ready progress views

## Git/submodule cleanup rules

- Push child repo changes first.
- Then update/remove parent submodule pointers.
- For removed plugin submodules, use `git rm -f <path>` in the parent repo and remove the `.gitmodules` section.
- Do not force-push parent HeRmEz; rebase or merge remote changes safely.
- Preserve unrelated dirty work from automation/video/trading projects.

## Concrete next implementation order

1. **SmartHiscoreLookup account-intel merge**
   - Pull AccountLegacyCard's local account summary/card concept into a tested `PlayerIntelCard` model.
   - Pull NameChangeWatcher's previous/current name observation logic into a tested session service.
   - Add a compact detail UI pattern that WhosGrindingPanel can mirror for clicked player rows.

2. **RivalRadar consolidation merge**
   - Start with non-network local modules: SkillNemesis analyzer, SkillStreaks tracker, BossStreaks parser/tracker.
   - Then add race setup/progress models for skill and boss races.
   - Add hiscore/Wise Old Man rival comparisons last, behind background-safe/cached helpers.

3. **Standalone polish lane**
   - Keep BisLoadouts focused on BIS/best-available boss loadout recommendations.
   - Keep IceBarrageTimer focused on PvP freeze/teleblock timing.
   - Keep PersonalProgressTimeline focused on personal milestones.
   - Keep CompetitionOverlay as the future larger competition surface; do not merge it into RivalRadar until the big idea is specified.

4. **Parent workspace hygiene**
   - Push every child repo before updating parent submodule pointers.
   - Stage exact OSRS paths only from `/opt/data/HeRmEz`.
   - Fix `projects/viral-clip-radar` submodule mapping separately from OSRS work.
