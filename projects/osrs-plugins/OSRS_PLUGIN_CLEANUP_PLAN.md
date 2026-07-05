# OSRS Plugin Cleanup Plan

## Current decisions

- Remove `GroupIronProgressBoard`; user does not want ironman/GIM-focused plugins.
- Keep `RivalRadar` as the canonical repo for race/streak/rival/competition consolidation.
- Make `SmartHiscoreLookup` the canonical account/player intel repo.
- Keep `WhosGrindingPanel` standalone. It should implement similar account-detail functionality locally rather than depending on SmartHiscoreLookup.

## Keep standalone

- WhosGrindingPanel
- SmartHiscoreLookup / Account Intel
- RivalRadar
- BossReadinessScore
- IceBarrageTimer
- PersonalProgressTimeline
- CompetitionOverlay

## Remove/archive

- GroupIronProgressBoard

## Merge into SmartHiscoreLookup

- AccountLegacyCard
- NameChangeWatcher

Merged feature target:

- local account card
- player lookup panel
- hiscore links
- previous/current name detection
- external tracker enrichment from OSRS APIs

## Merge into RivalRadar

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
