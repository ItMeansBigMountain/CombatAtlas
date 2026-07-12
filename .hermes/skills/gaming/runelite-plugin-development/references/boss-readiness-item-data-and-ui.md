# BIS Loadouts item-data, gear logic, and sidebar lessons

Use when working on `/opt/data/HeRmEz/projects/osrs-plugins/in-progress/BisLoadouts` (formerly BossReadinessScore). The GitHub repo is `ItMeansBigMountain/bis-loadouts-osrs`.

## Data-source stance

Do **not** scrap GearScape just because a few recommendations are stale/noisy. The user says the plugin is mostly accurate because GearScape has practical live equipment/weapon/boss combat stats that older BiS-style sources do not keep current.

Preferred runtime source stack:

1. **GearScape** monster/equipment/weapon endpoints for machine-readable combat stats, `two_handed`, subcategory, and ranged `ammunition` compatibility IDs.
2. **OSRS Wiki** as the always-updated canonical item/name/main-game source. Use wiki mapping/category/page data as reliability and freshness validation around GearScape, not as a replacement for combat-stat shape.
3. **Local curated fallback items/ammo** for current main-game gear that live APIs may lag on or omit.

Before changing filters or item logic, run a quick research scan against OSRS Wiki mapping + GearScape equipment/weapon data and inspect actual names/ids that would pass. Do not implement filters from memory.

## Main-game vs excluded items

The user wants **main-game** recommendations. Exclude seasonal/PvP-mode-only rows that leak from GearScape, including patterns found in research scans:

- `(dmm)`, `deadman`, `deadman's`
- `(bh)`, `bounty hunter`
- `vesta's`, `statius's`, `morrigan's`, `zuriel's`
- `fractured archive`, `dogsword`, `thunder khopesh`
- temporary Gauntlet variants: `corrupted`, `attuned`, `perfected`, `(basic)`, etc.
- Leagues/seasonal cosmetics: `leagues`, `trailblazer`, `shattered relics`, `raging echoes`, `relic hunter`, broad `seasonal`/`competitive` terms.

Do **not** block main-game minigame rewards just because they are minigame-sourced. Allowed examples:

- Castle Wars/LMS halos (`saradomin halo`, `zamorak halo`, etc.)
- `swift blade`
- other current main-game rewards if they are real wearable OSRS gear.

Avoid broad substring filters like `gauntlet`: `confliction gauntlets` are real current OSRS gear and should be allowed. Use explicit temporary-item patterns instead.

## Known current item corrections

- `confliction gauntlets` are real current OSRS gear, item id `31106`; they should be recommended over tormented bracelet when offensive magic stats make them stronger. They require 90 Hitpoints in-game, but current `GearItem` requirement modeling may not include HP requirements yet — note this until HP requirements are modeled.
- `aranea boots` are real current OSRS tribrid boots, item id `29806`; no requirements; offensive stats include +5 magic, +6 ranged, +4 melee strength. Add/keep them as local curated fallback if live sources lag.

## Recommendation logic expectations

- Gear recommendations should be **max-DPS / offensive-stat first**, respecting boss style weakness, player stats, budget, weapon compatibility, and main-game filters. Defensive/readiness messaging is secondary.
- Alternatives for each slot must be ordered strongest-to-weakest. The left/default item is the strongest; right arrow moves to weaker alternatives.
- Do not mix 1H and 2H weapons in one cycling list. Maintain separate weapon alternative sets:
  - 2H weapon set
  - 1H weapon set
- The panel should let the user switch/cycle those sets. If a 1H weapon is displayed, recommend/cycle a compatible shield/offhand. If a 2H weapon is displayed, suppress/disable shield display but keep shield alternatives internally so they reappear when switching back to 1H.
- Use GearScape `two_handed` boolean when available. Fall back to known-name/subcategory heuristics only when the live boolean is missing.

## Ranged ammo compatibility — critical pitfall

The user explicitly complained when cycling ranged weapons did not update ammo and again when no ammo was recommended. Treat this as a blocking regression.

Authoritative OSRS Wiki ammunition rules:

- bows use arrows
- crossbows use bolts
- ballistae use javelins
- toxic blowpipe uses darts
- salamanders use herb tar
- crystal/self-contained ranged weapons use charges, not conventional ammo

Use GearScape weapon `ammunition` IDs when available and filter the displayed ammo slot to compatible ammo only:

- `twisted bow`, `dark bow`, `venator bow`, `scorching bow` → arrow IDs
- `rune crossbow`, `zaryte crossbow` → bolt IDs
- `toxic blowpipe` → dart IDs
- `bow of faerdhinen`, `crystal bow`, `webweaver bow`, `craw's bow` → self-contained/charge behavior; do not force generic arrows.

Implementation pitfall: do **not** permanently replace/remove the full ammo alternatives list with only the currently selected weapon's compatible ammo. Keep the full ammo pool internally so switching bow → crossbow → blowpipe can recalculate arrows → bolts → darts. Only the displayed/selected ammo should be filtered for the currently displayed weapon.

Also avoid relying only on GearScape live ammo rows. Add local curated ammo fallbacks from OSRS Wiki so recommendations never go blank when live data omits ammo:

- arrows: `dragon arrow`, `amethyst arrow`, `rune arrow`
- bolts: `dragon bolts`, `ruby dragon bolts (e)`, `diamond dragon bolts (e)`, `runite bolts`, `amethyst broad bolts`
- darts: `dragon dart`, `amethyst dart`, `rune dart`

Test requirements for future changes:

- Bow accepts arrows and rejects bolts.
- Crossbow accepts bolts and rejects arrows.
- Blowpipe accepts darts and rejects arrows.
- Self-contained bowfa/crystal-style weapons reject generic arrows.
- Ranged recommendations include arrow, bolt, and dart alternatives in the internal ammo pool so UI cycling can recalculate ammo by weapon type.

## Boss weakness / defence display

The user wants selected boss defenses shown below the gear icon grid **in order from weakest to strongest**, but not as a dense one-line stat dump. OSRS players understand this better as an attack-style guide: low defence means the boss is weak to that style; high defence means avoid that style.

Preferred format is a light, larger, vertical bullet block that can use sidebar height freely:

```text
Boss attack style guide
• Weakest / best: Ranged def 45
• Good: Stab def 75
• Okay: Slash def 150
• Strong: Crush def 150
• Strongest / avoid: Magic def 150
```

Avoid paragraph-looking text under the gear grid. If all defenses are zero/missing from the source, show a single bullet such as `• Unknown from this data source`.

## UI preference

For Boss Readiness, center the panel controls and status text inside RuneLite's narrow sidebar: boss selector, style buttons, Analyze button, headings, summary lines, muted notes, and equipment grid.

For explanatory text under gear recommendations, make it lighter/brighter than the previous muted gray, slightly bigger, and multi-line/bulleted. The user is comfortable using more vertical space; prioritize legibility over compactness.

Alignment lesson from screenshot review: text above the recommendation icons should align from the same left edge as the icon grid begins. For text below the recommendation icons, the user preferred the smaller-text version's alignment but the larger font size. Preserve the grid-aligned left edge/section width and increase only the font/line height. Section the below-grid text consistently using the same font/alignment for `Gear controls`, `Boss attack style guide`, and `DPS per style` (renamed from `Other styles`).

Boss search UX: do not use `None` as visible placeholder/search text or as a dropdown option because it interferes with searching. A blank boss search field means “no boss selected / best gear by stats”; if old UI state sends `None`, treat it as blank internally.

Keep explanatory text concise; the gear grid should answer: “what is the strongest legal main-game gear for my stats/budget against this boss?”