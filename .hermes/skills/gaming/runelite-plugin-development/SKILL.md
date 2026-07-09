---
name: runelite-plugin-development
description: Develop, debug, consolidate, and publish RuneLite/OSRS plugins in the user's HeRmEz workspace.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, windows]
metadata:
  hermes:
    tags: [RuneLite, OSRS, Java, Gradle, plugins, GitHub, submodules]
    related_skills: [github-repo-management, software-quality-workflows]
---

# RuneLite / OSRS Plugin Development

Use this when working on the user's OSRS/RuneLite plugin portfolio: fixing plugin UI/API bugs, adding panels/configs, merging overlapping plugin ideas, cleaning project directories, or pushing plugin/submodule updates through the HeRmEz control repo.

## Workspace and repository model

- Canonical control workspace: `/opt/data/HeRmEz`.
- Active plugin workspace: `/opt/data/HeRmEz/projects/osrs-plugins`.
- HeRmEz is a global control repo and is backed up/pushed by cron; keep it clean and up to date after child plugin changes.
- Use `GITHUB_ACCESS_TOKEN` for authenticated GitHub operations when `gh` is unavailable.
- Many plugin folders are standalone Git repos under the parent workspace. Treat them as child repos/submodules, not ordinary parent-tracked source folders.

## Active workflow

1. Load `github-repo-management` before GitHub/submodule/repo cleanup work.
2. Inspect the specific plugin child repo status before editing:
   ```bash
   git -C /opt/data/HeRmEz/projects/osrs-plugins/<Plugin> status --short --branch
   git -C /opt/data/HeRmEz/projects/osrs-plugins/<Plugin> remote -v
   ```
3. For Java/RuneLite work, prefer the Java 11 toolchain already used in this workspace:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew clean test assemble --no-daemon --console=plain
   ```
   For locally launching `WhosGrindingClanPanel` on Windows, the verified task is:
   ```bat
   .\gradlew.bat run
   ```
   Do not tell the user to use `runClient` for this repo unless the Gradle task list confirms it exists.
   For Windows/local launch of these plugin repos, use:
   ```bat
   .\gradlew.bat runClient --args="--developer-mode --debug"
   ```
   Do not recommend `gradlew.bat run --no-daemon` as the primary local launch command; the user confirmed `runClient --args="--developer-mode --debug"` is the working command.
   4. Commit and push the child repo first, verify remote/local match, then update the parent/submodule pointer in `/opt/data/HeRmEz` if needed.
5. After child pushes, update parent documentation/cleanup plans and push HeRmEz so a fresh clone plus submodule update reproduces the workspace.
6. Give Windows pull instructions when reporting completion:
   ```bat
   cd C:\Users\faree\Desktop\HeRmEz
   git pull origin main
   git submodule sync --recursive
   git submodule update --init --recursive
   ```

## RuneLite API/debugging approach

- Do not guess RuneLite social/player APIs. Inspect cached RuneLite jars and existing plugin source when behavior is unclear.
- Use `javap` against cached `runelite-api` jars to confirm methods before wiring code.
- Social/friends/clan APIs can differ by RuneLite version. If a clan/friends-chat source returns empty, verify the exact `Client`, friends chat manager, clan channel, and container APIs exposed by the installed jar.
- Keep plugin side panels within RuneLite's narrow default panel width. Avoid wide tabs, long labels, and horizontally expanding controls.

## UI preferences for this user's OSRS plugins

- Panels should fit the default RuneLite side panel width.
- Do not guess side-panel widths. Derive a safe content width from `PluginPanel.PANEL_WIDTH`, `SCROLLBAR_WIDTH`, and `BORDER_OFFSET`, then add a unit test for the budget. See `references/runelite-side-panel-dimensions.md`.
- Start panels empty; do not fake players or sample clan data.
- Prefer compact controls: dropdowns, icon buttons, short labels, and fixed dimensions for top rows.
- If a control is not visible in screenshots, treat it as a real UI bug and constrain width/height rather than explaining it away.
- Add at-a-glance icons/symbols for player activity, then put detailed tracker information behind a click/details interaction.
- For social activity panels, keep Friends List, Friends Chat, and Clan Chat distinct when the game exposes each as a real source; do not remove Clan Chat just because a plugin is no longer clan-only.
- Member rows should be dense and readable in RuneLite's narrow sidebar: compact height, minimal padding, no trailing text/buttons, and “currently grinding” summaries over status-only rows. If a screenshot shows text/buttons running off-screen, treat it as urgent: remove optional row controls, reduce left/right padding before shrinking text, and force wrapping inside the measured sidebar width.
- For Who's Grinding-style panels, prefer inline expandable/collapsible player rows: clicking a row expands the grinding card directly under that player, clicking again collapses it. Avoid a separate bottom details card when it wastes vertical space or makes the selected row/card visually disconnected.
- Clicked-player details should become an in-panel detail/card view, not a basic `JOptionPane` text dump. If the user decides not to share profile-source details, remove WOM/Temple/hiscore URL rows and any “Data links” section from the UI; keep only the grinding summary.
- Add configurable gains windows for player tracking views when relevant: Day, 7 days, 30 days, and 365 days.
- In Who's Grinding Panel detail cards, treat `Grinding` as selected-period activity from tracker data (top WOM XP/KC/score gains for the configured period), not as a social-source/location summary.
- Keep social source details out of the selected-player detail card when WOM/TempleOSRS/hiscore profile links already provide context; preserve source filtering/list-row context separately.
- For social tracker plugins, preserve all three user-visible social source lanes when applicable: Friends List, Friends Chat, and Clan Chat. Do not remove Clan Chat merely because the plugin is no longer clan-only.
- A clicked social/profile row should become an in-panel selected-player detail/card view, not a basic `JOptionPane` modal. Show what the player is likely grinding using cached tracker data when available.
- Use Wise Old Man/TempleOSRS-style gained tables and mini timelines as the model for progress detail UX: top gained skills/bosses, XP/KC/rank/EHP deltas, selected period, and last-updated labels.
- For Who's Grinding / social player detail cards, do **not** spend sidebar space on a separate `Sources` field when WOM/TempleOSRS/hiscore profile URLs are already shown; the links provide enough external-source context.
- Be precise about `Grinding`: until WOM/TempleOSRS XP/KC enrichment is actually wired, the field is only a local social-scan activity summary (source/world/offline). Do not present it as real inferred training. The target meaning is recent gained data such as likely skill/boss, XP/KC gained, rank/level deltas, and selected period.
- If the user says blocks are too big / text too small / panel trails off, immediately remove low-value visualizations (especially heatmaps), increase readable row/detail text around 10f, and move detail into a slim vertical card inside the panel rather than a modal.
- When the user says a RuneLite side-panel block is too wide/big or wasting space, do not merely restyle it. Remove or replace the underlying UI section, config entries, model classes, and tests if the feature is no longer wanted; then grep the active source for the removed feature name before claiming it is gone.
- For Who's Grinding-style player details, prefer a compact vertical in-panel selected-player card over modals: readable ~10f text, narrow wrapped rows, source/world/status/current-grind summary, selected gains period, and shareable external links such as Wise Old Man gained, TempleOSRS, and official hiscores.

## Current consolidation direction

See `references/osrs-plugin-portfolio-cleanup.md` for the current user-approved consolidation map.
See `references/osrs-consolidation-implementation-notes.md` for session-tested implementation notes, pure-service module patterns, RuneLite API probes, and child/parent push verification snippets.
See `references/runelite-side-panel-dimensions.md` for the RuneLite side-panel width budget, WhosGrindingPanel dimensions helper pattern, and Windows submodule handoff pitfall.
See `references/whos-grinding-panel-social-detail-pattern.md` for the current Who's Grinding Panel source model, profile detail UX, gains-period config, and WOM/TempleOSRS integration direction.
See `references/whos-grinding-wom-period-summary.md` for the Wise Old Man gained API pattern used to populate the selected-player `Grinding` section from the configured period.
See `references/runelite-social-progress-detail-panels.md` for corrected social-source handling (Friends List/Friends Chat/Clan Chat), side-panel profile-detail UX, and WOM/TempleOSRS progress API notes.
See `references/whos-grinding-detail-card-lessons.md` for latest user-reviewed sidebar detail-card rules: no heatmap, no separate Sources line when profile URLs are present, precise `Grinding` semantics, and compact vertical fields.

High-level rules:

- Finish **Who's Grinding Panel** bugs before executing repo cleanup.
- Merge account/name/hiscore identity features into the account intelligence lane.
- Keep major standalone utilities where the user identified unique value.
- Consolidate overlapping race/streak/rival/nemesis plugins into a smaller number of coherent repos.
- Clean project dirs and submodules only after code-level bugs are verified and pushed.

## Pitfalls

- Do not claim GitHub access is unavailable just because `gh` is missing; use `GITHUB_ACCESS_TOKEN` and the GitHub API fallback.
- When pushing with `GITHUB_ACCESS_TOKEN`, avoid nested single-quoted shell/Python URL construction; use a simple double-quoted/f-string token URL and verify `ls-remote` SHA equals local `HEAD` after every child and parent push.
- Do not `git add` nested plugin worktrees directly into the HeRmEz parent unless intentionally updating submodule gitlinks or backup artifacts.
- Do not leave child repo changes unpushed while updating only the parent repo.
- Do not preserve obsolete names like `WhosGrindingClanPanel` in user-facing display text when the direction is **Who's Grinding Panel**; internal package paths may change later as a deliberate migration.
- Do not interpret "remove broken clan source" as "remove Clan Chat forever." The durable product correction is: keep Clan Chat as a real source/panel, alongside Friends List and Friends Chat, but do not make the whole plugin clan-only. In current RuneLite, clan channel classes live under `net.runelite.api.clan.*`.
- Do not use `JOptionPane` as the final profile detail interaction for social/progress plugins. It is acceptable only as a temporary scaffold; replace it with an in-panel detail view before calling the UI polished.
- When adding external player tracking sources (Wise Old Man, TempleOSRS, Crystal Math Labs, official hiscores), avoid polling every visible member every tick. Use click-to-fetch, explicit refresh, caching, and bulk endpoints where available; add Plugin Hub-compliant warnings for any third-party data sent.
- When the user reports `fatal: No url found for submodule path ... in .gitmodules`, do not repeat broad `git submodule update --init --recursive` advice. Either fix the missing `.gitmodules` mapping or give a path-scoped OSRS submodule update for the plugin being worked on.
- Do not consolidate repos before first producing and reviewing a cleanup plan; these plugins represent different product lanes.
