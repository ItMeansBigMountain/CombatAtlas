# BIS Loadouts README screenshot assets

Use when the user asks to add, rerun, or recreate README screenshots for the BIS Loadouts RuneLite plugin.

## What happened

Raw screenshot reuse and naive headless Swing rendering produced poor README assets:

- copied Discord screenshots were narrow/cropped and did not clearly explain the plugin flow;
- rendering `BisLoadoutsPanel` directly from a test produced mostly blank light-gray images because Swing components were not realized/laid out like a live RuneLite panel;
- cropping/upscaling the raw Swing output made text/icons visible but caused clipped labels and cut-off panel content.

The successful README assets were clear explanatory images that preserve the plugin's visual language while showing the workflow at high resolution.

## Preferred README screenshot shape

For BIS Loadouts README assets, prefer two clean explanatory screenshots over raw cramped sidebar captures:

1. `docs/assets/bis-loadouts-side-panel.png`
   - boss selection
   - setup style controls
   - Analyze button
   - selected boss setup summary
   - loadout fit / estimated DPS / hit chance
   - recommended equipment grid
   - basic gear cycling / 1H-2H note

2. `docs/assets/bis-loadouts-recommendations.png`
   - gear controls bullets
   - boss attack style guide from weakest to strongest
   - DPS per style bars
   - public data/fallback note

Use readable README-scale dimensions around 700 px wide and a dark RuneLite-like palette. Prioritize clarity over exact pixel-perfect RuneLite capture when the goal is explaining the plugin in GitHub.

## Verification checklist

Before committing screenshot updates:

- open/analyze the generated PNGs and confirm they are not blank;
- confirm text is readable at GitHub README scale;
- confirm no major label is clipped on the right edge;
- confirm the screenshots communicate how to use the plugin, not just what a tiny sidebar looks like;
- run `./gradlew clean test assemble --no-daemon --console=plain` after code/doc asset changes;
- commit/push the child repo first, then update/push the HeRmEz parent submodule pointer.

## Pitfall

Do not claim screenshots are fixed after only generating files. Visually inspect them. A file can be non-empty and still be useless for README review if the UI is blank, cropped, or too small to read.