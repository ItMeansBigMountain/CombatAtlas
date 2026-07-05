# OSRS Plugin Cleanup Plan

## Current decisions

- Remove `GroupIronProgressBoard`; user does not want ironman/GIM-focused plugins.
- Remove thin/overlapping source repos from the parent HeRmEz workspace once their product direction is captured in the canonical repos.
- Keep `RivalRadar` as the canonical repo for race/streak/rival/competition consolidation.
- Make `SmartHiscoreLookup` the canonical account/player intel repo.
- Keep `WhosGrindingPanel` standalone. It should implement similar account-detail functionality locally rather than depending on SmartHiscoreLookup.

## Active parent submodules after cleanup

- WhosGrindingClanPanel / WhosGrindingPanel
- SmartHiscoreLookup / Account Intel
- RivalRadar
- BossReadinessScore
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

The removed child repositories still exist remotely/history-wise, but they are no longer cloned by default from the HeRmEz parent workspace.

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
