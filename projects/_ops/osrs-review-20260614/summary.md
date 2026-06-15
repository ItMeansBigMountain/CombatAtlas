# OSRS Plugin Review 2026-06-14

Build check: 17/17 passed `./gradlew clean test assemble --no-daemon` with Java 11.

Raw build report: `/opt/data/HeRmEz/projects/_ops/osrs-review-20260614/build-report.jsonl`
Product review: `/opt/data/HeRmEz/projects/_ops/osrs-product-review.json`

## Build failures
- None

## Product maturity
- **AccountLegacyCard** — serious side-panel/API product; features: sidebar, player menu, api/http, hiscore/WOM/Temple, config
- **BossKCRivalLookup** — thin; features: chat, hiscore/WOM/Temple, config
- **BossRaceCreator** — thin; features: chat, config
- **BossReadinessScore** — serious side-panel/API product; features: sidebar, api/http, config
- **BossStreaks** — thin; features: chat, config
- **ClanGrindHeatmap** — usable RuneLite UI/plugin MVP; features: overlay, chat, config
- **CompetitionOverlay** — usable RuneLite UI/plugin MVP; features: overlay, chat, config
- **GroupIronProgressBoard** — thin; features: chat, config
- **IceBarrageTimer** — usable RuneLite UI/plugin MVP; features: overlay, game tick, chat, config
- **NameChangeWatcher** — thin; features: game tick, chat, config
- **PersonalProgressTimeline** — thin; features: chat, config
- **RivalRadar** — usable RuneLite UI/plugin MVP; features: overlay, chat, api/http, hiscore/WOM/Temple, config
- **SkillNemesis** — moderate codebase; features: chat, config
- **SkillRaceCreator** — thin; features: chat, config
- **SkillStreaks** — thin; features: chat, config
- **SmartHiscoreLookup** — thin; features: chat, hiscore/WOM/Temple, config
- **WhosGrindingClanPanel** — thin; features: chat, config

## Recommended completion order
- **Ship first:** AccountLegacyCard, BossReadinessScore, RivalRadar, WhosGrindingClanPanel/ClanGrindHeatmap.
- **Consolidate into RivalRadar:** BossKCRivalLookup, BossRaceCreator, SkillNemesis, SkillRaceCreator.
- **Lightweight publish candidates:** IceBarrageTimer, CompetitionOverlay, BossStreaks, SkillStreaks, NameChangeWatcher, PersonalProgressTimeline.
- **Merge with AccountLegacyCard:** SmartHiscoreLookup unless it has a distinct UX after manual testing.