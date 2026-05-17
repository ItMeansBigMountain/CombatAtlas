# First Tiny Mobile Game Concept Selection

- **Project:** Quick Addictive Mobile Games
- **Created:** 2026-05-03
- **Runner:** Heartbeat
- **Goal:** Compare 3 tiny addictive mobile game concepts, select the first one, and note ad monetization/app-store constraints before implementation.

## Existing assets noticed

The project already has imported legacy experiments:

- `legacy-src/video-games/space_invaders_unf/main.py` and related sprites
- `legacy-src/video-games/drawing.py`
- `legacy-src/video-games/pokemon.py`
- `legacy-src/self-playing-game/script.py`

These are useful inspiration, but the first mobile game should be smaller than a full port. Start with one tight loop.

## Comparison table

| Concept | Core loop | Build difficulty | Addiction hook | Monetization fit | Risk | Score |
|---|---|---:|---|---|---|---:|
| **Dodge Dot Rush** | Drag a dot/fighter to dodge falling blocks and collect coins | Low | one-more-run survival + high score | rewarded revive, interstitial every few runs, cosmetic skins | Low | 9/10 |
| **Tap Ninja Timing** | Tap at the exact moment to slice targets / avoid bombs | Low-medium | timing mastery + combo streaks | rewarded continue, skin unlocks, light interstitials | Medium: needs satisfying feel | 8/10 |
| **Tiny Space Defender** | One-thumb horizontal movement + auto-shoot waves | Medium | wave survival + upgrades | rewarded upgrade/continue, interstitial after game over | Medium: more assets/balancing | 7/10 |

## Concept 1: Dodge Dot Rush

### Pitch

A one-thumb survival game where the player drags a glowing dot/ninja/fighter around the screen, dodges falling obstacles, and grabs coins/powerups.

### Why it works

- Very small scope.
- Easy to prototype with circles/rectangles before art.
- Natural mobile controls.
- Session length can be 20-90 seconds.
- High-score loop is easy to understand.

### MVP mechanics

- Player follows finger drag.
- Obstacles fall from top.
- Coins occasionally spawn.
- Score increases with survival time.
- Game over on collision.
- Restart button.
- Local best score.

### Stretch mechanics

- Shield powerup.
- Slow-motion pickup.
- Skins: ninja, spaceship, pixel orb.
- Daily challenge seed.

## Concept 2: Tap Ninja Timing

### Pitch

A reaction game where targets fly across the screen and the player taps at the perfect moment to slice them. Bombs or decoys break the streak.

### Why it works

- Strong short-form content appeal.
- Easy to theme with ninja/Oyama branding.
- Simple to explain in 2 seconds.

### MVP mechanics

- Targets appear with a timing window.
- Tap inside window for points.
- Miss or tap bomb ends streak.
- Combo multiplier.

### Risks

- Needs good animation/sound feedback to feel addictive.
- Timing balance matters.

## Concept 3: Tiny Space Defender

### Pitch

A simplified mobile space shooter inspired by the imported Space Invaders assets, but reduced to one-thumb movement and auto-fire.

### Why it works

- Existing legacy assets can help.
- Familiar arcade loop.
- Upgrade path is obvious.

### MVP mechanics

- Player moves horizontally.
- Auto-shoot bullets.
- Enemies descend.
- Score and lives.
- Game over/restart.

### Risks

- More balancing and collision logic than Dodge Dot Rush.
- More likely to become a mini-engine before the first release.

## Selected first game

# Dodge Dot Rush

## Selection reason

Pick **Dodge Dot Rush** first because it has the smallest implementation surface and the cleanest monetization loop. It can be built with placeholder shapes, tested quickly, and reskinned later into ninja/space/pixel styles.

This is the boring-success choice. Do not start with the more complex shooter until one tiny mobile loop is playable.

## Recommended prototype scope

### Platform

Start with a simple web/mobile prototype first, then package later if worth it.

Good first implementation options:

1. HTML Canvas + JavaScript/TypeScript
2. React Native / Expo after mechanics are proven
3. Godot only if app-store packaging becomes priority

Recommendation: **HTML Canvas first** for fastest local validation.

### Prototype files

```text
index.html
src/game.js
src/styles.css
README.md
```

### Prototype success criteria

- Game launches locally.
- Player can move with mouse/touch drag.
- Obstacles spawn and fall.
- Collision ends game.
- Score increases over time.
- Restart works.
- Best score persists in local storage.

## Ad monetization notes

Use ads only after gameplay is fun. Do not wire ad SDKs in the first prototype.

Future ad placements:

- **Rewarded ad:** continue once after game over.
- **Interstitial:** after every 3-5 completed runs, never during active play.
- **Rewarded ad:** unlock temporary skin or coin bonus.

Avoid:

- Ads before first play.
- Ads during gameplay.
- Too many popups.
- Misleading reward prompts.

## App-store constraints to remember

Manual approval/account steps will be required later:

- Apple Developer account / Google Play Console account.
- App privacy policy URL.
- Accurate age rating.
- Data collection disclosures.
- Ad SDK privacy disclosures.
- COPPA/child-directed content review if marketed to kids.
- No copyrighted/protected assets from Pokemon or other brands.
- No misleading gambling-like reward mechanics.

## Next implementation slice

Create a local HTML Canvas prototype for **Dodge Dot Rush** with placeholder shapes and no ad SDKs.

## Blockers

None for local prototype. App-store publishing, ad SDK setup, developer accounts, and public release require manual approval.
