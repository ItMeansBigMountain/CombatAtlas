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
- OSRS plugin repos are organized into lifecycle buckets next to `_templates/`: `in-progress/`, `pr-review-pending/`, and `completed/`. Use `in-progress/` for active work, `pr-review-pending/` for locally complete Plugin Hub candidates, and `completed/` only after official RuneLite Plugin Hub approval/merge.
- HeRmEz is a global control repo and is backed up/pushed by cron; keep it clean and up to date after child plugin changes.
- Use `GITHUB_ACCESS_TOKEN` for authenticated GitHub operations when `gh` is unavailable.
- Many plugin folders are standalone Git repos under the parent workspace. Treat them as child repos/submodules, not ordinary parent-tracked source folders. When moving plugins between lifecycle buckets, use `git mv` in the parent repo, update `.gitmodules`, and verify the plugin still builds from its new path.

## Active workflow

1. Load `github-repo-management` before GitHub/submodule/repo cleanup work.
2. Inspect the specific plugin child repo status before editing:
   ```bash
   git -C /opt/data/HeRmEz/projects/osrs-plugins/<Plugin> status --short --branch
   git -C /opt/data/HeRmEz/projects/osrs-plugins/<Plugin> remote -v
   ```
3. For Java/RuneLite validation, prefer the Java 11 toolchain already used in this workspace:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew clean test assemble --no-daemon --console=plain
   ```
   For locally launching `WhosGrindingClanPanel` on Windows from the plugin directory, the verified command is:
   ```bat
   .\gradlew.bat run --no-daemon --console=plain
   ```
   Do not recommend `runClient` for this repo unless the Gradle task list confirms it exists for the current checkout.
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
- Use Wise Old Man/TempleOSRS-style gained data as the model for progress detail UX, but keep the user's Who's Grinding Panel detail focused on the **Grinding** section only: grouped selected-period skills XP, boss KC, and activity/minigame score gains. Avoid URL/source/debug rows in the card unless the user asks for them.
- For Who's Grinding Panel and future RuneLite sidebar plugins, use the screenshot-approved width standard: align major content to the same left edge as the top dropdown/title block and constrain content to the dropdown/button row width, not the full screenshot/window. Preserve only a tiny right safety pad (~3 px); do not leave a large right blank gutter. Rows/cards should visually match the red-marked width in the user's approved screenshot.
- For Who's Grinding Panel, prefer compact expandable player rows over a separate bottom detail card. Click row to expand/collapse the grinding card inline. The card must be content-sized, use readable font, start near the left edge, include a small right padding (~3px), and contain no blank vertical filler. For Swing `BoxLayout`, do not leave expanded cards with `Short.MAX_VALUE` max height; compute height from the card row labels' preferred heights and set both preferred and max size.
- If a Who's Grinding card still appears pushed right after width/height fixes, do not keep tweaking a single giant HTML label. Split the card into multiple `JLabel` rows, set `Component.LEFT_ALIGNMENT` on the card and every row/control/member component, and keep each row's border/margins at zero. Giant HTML blobs tend to wrap unpredictably, shift right, and create blank vertical space in RuneLite's narrow sidebar.
- In Who's Grinding Panel WOM/official-hiscore summaries, show **all positive gains**, not only the top few. The user wants every stat found with `+` gains visible for auditing tracking correctness. Remove max-line caps for skills, bosses, and activities unless a later UI explicitly adds an expandable/collapsible control.
- Do not render redundant gain labels like `+485,257 xp (XP)`, `+16 kc (KC)`, or `+34 score (Score)`. Use only the value suffix (`xp`, `kc`, `score`) with the existing section heading/icon.
- Before fetching WOM gained data for a selected player, call WOM's player create/update endpoint (`POST /v2/players/{name}`) so newly discovered usernames become trackable, then fetch `gained`. For any future server-wide/social-list preloading, implement a throttled deduped queue rather than an eager bulk loop.
- If WOM cannot find useful stats for a player, start/update WOM tracking with `POST /v2/players/{name}` and retry gained data; if there are still no positive gains, show a concise explanation that WOM tracking was started/updated and suggest trying a longer period (30/365 days) or checking again after XP/KC changes. In the narrow card, wrap this fallback at roughly three words per line using `<br>` so it does not become a long unreadable sentence. Keep API-failure and no-positive-gain messages distinct internally, but make both concise and similarly wrapped so screenshots do not look inconsistent.
- For Who's Grinding Panel, the top logged-in-player row should be an editable player search field autofilled with the current username. The user must be able to type another name directly there and press Enter/search to load that player's WOM grinding card, even if they are not visible in the social-source list.
- Simple inline text markers are acceptable when real RuneLite/OSRS sprite wiring is not yet done: e.g. `▴` for skills/XP, `⚔` for boss KC, `★` for activities/minigames. Prefer these over no visual category cue, but do not spend a large pass on sprite assets unless the user explicitly asks.
- Use common OSRS slang/acronyms to keep narrow WOM cards readable when the label is unambiguous: `CoX`, `ToA`, `ToB`, `HMT`, `CG`, `KQ`, `KBD`, `LMS`, `SW`, etc. Avoid ambiguous acronyms when they confuse the card (e.g. use `Bandos` for General Graardor rather than `GG`).


- Be precise about `Grinding`: until WOM/TempleOSRS XP/KC enrichment is actually wired, the field is only a local social-scan activity summary (source/world/offline). Do not present it as real inferred training. The target meaning is recent gained data such as likely skill/boss, XP/KC gained, rank/level deltas, and selected period.
- If the user says blocks are too big / text too small / panel trails off, immediately remove low-value visualizations (especially heatmaps), increase readable row/detail text around 10f, and move detail into a slim vertical card inside the panel rather than a modal.
- When the user says a RuneLite side-panel block is too wide/big or wasting space, do not merely restyle it. Remove or replace the underlying UI section, config entries, model classes, and tests if the feature is no longer wanted; then grep the active source for the removed feature name before claiming it is gone.
- For Who's Grinding-style player details, prefer a compact vertical in-panel selected-player card over modals: readable ~10f text, narrow wrapped rows, source/world/status/current-grind summary, selected gains period, and shareable external links such as Wise Old Man gained, TempleOSRS, and official hiscores.

## Current consolidation direction

See `references/osrs-plugin-portfolio-cleanup.md` for the current user-approved consolidation map.
See `references/osrs-plugin-lifecycle-and-plugin-hub-pr.md` for OSRS plugin lifecycle bucket rules (`in-progress`, `pr-review-pending`, `completed`), RuneLite Plugin Hub PR manifest requirements, and the current Who's Grinding Panel run command/finalization notes.
See `references/osrs-consolidation-implementation-notes.md` for session-tested implementation notes, pure-service module patterns, RuneLite API probes, and child/parent push verification snippets.
See `references/runelite-side-panel-dimensions.md` for the RuneLite side-panel width budget, WhosGrindingPanel dimensions helper pattern, and Windows submodule handoff pitfall.
See `references/whos-grinding-panel-social-detail-pattern.md` for the current Who's Grinding Panel source model, profile detail UX, gains-period config, and WOM/TempleOSRS integration direction.
See `references/whos-grinding-wom-period-summary.md` for the Wise Old Man gained API pattern used to populate the selected-player `Grinding` section from the configured period.
See `references/runelite-social-progress-detail-panels.md` for corrected social-source handling (Friends List/Friends Chat/Clan Chat), side-panel profile-detail UX, and WOM/TempleOSRS progress API notes.
See `references/whos-grinding-wom-detail-ui.md` for the latest wrap-up lessons: compact expandable rows, content-sized grinding cards, WOM start/update fallback, grouped skills/bosses/activities, and visual verification expectations.
See `references/whos-grinding-card-legibility-polish.md` for latest screenshot-reviewed card rules: line-by-line stats, bold gained values, safe inline symbols, tiny right padding, and three-words-per-line no-data fallback.
See `references/whos-grinding-compact-gained-lines.md` for gained-summary formatting history.
See `references/whos-grinding-final-sidebar-standards.md` for the latest user-approved final sidebar standards: approved width, line-by-line stat rows, bold gained values, no-data wrapping, and visual verification checklist.
See `references/whos-grinding-card-line-layout.md` for the latest user-reviewed card layout rule: every player-card item line-by-line, 12f/11f text, left alignment, tiny right padding, no giant HTML blobs, and no-stats fallback behavior.
See `references/whos-grinding-card-alignment-and-no-stats.md` for the latest card-alignment fix: avoid giant HTML blobs, use per-row left-aligned labels, and handle no-WOM-stats cases with start/update + retry messaging.
See `references/whos-grinding-wom-grinding-summary.md` for the current Who's Grinding Panel wrap-up target: compact expandable rows, grinding-only card UX, WOM gained API sections, start-tracking fallback, and Windows `gradlew.bat run` command.
See `references/whos-grinding-card-final-polish.md` for final screenshot-driven card polish rules: every stat line-by-line, readable fonts, tight left edge, slight right padding, inline category markers, no-stats fallback, and live `oyama`-style visual verification.
See `references/osrs-slang-acronyms.md` for OSRS slang/acronym labels to use in narrow RuneLite UI, especially boss/raid/activity labels such as CoX, ToB, ToA, CG, KQ, KBD, LMS, BH, SW, etc.
See `references/runelite-plugin-hub-lifecycle-and-hiscore-fallback.md` for the current OSRS plugin lifecycle folder model, RuneLite Plugin Hub PR submission checklist, and WOM -> official hiscores local snapshot fallback pattern.
See `references/whos-grinding-self-row-and-acronyms.md` for the latest final-shipping lesson: pinned current-player row, concise distinct WOM error/no-gain states, and acronym verification.
See `references/whos-grinding-compact-card-rendering.md` for the latest card-rendering pitfalls: content-sized Swing cards, no blank expanded-card height, `oyama` WOM visual verification, and boss KC one-per-line formatting.
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
- When adding external player tracking sources (Wise Old Man, TempleOSRS, Crystal Math Labs, official hiscores), avoid polling every visible member every tick. Use click-to-fetch, explicit refresh, caching, and bulk endpoints where available; add Plugin Hub-compliant warnings for any third-party data sent. For WOM, if a selected player is not tracked yet, POST `/v2/players/{name}` to start/update tracking, then retry the gained endpoint. For official OSRS hiscores fallback, remember that official hiscores provide current totals only; calculate period gains by saving local snapshots and comparing against an older snapshot, and show a clear baseline-needed message if no older snapshot exists.
- When the user reports RuneLite sidebar spacing from screenshots, treat it as a blocking UI bug. Build success is insufficient: inspect or generate a visual sidebar-width render with representative live data (e.g. `oyama` WOM gains) and verify no cutoff/trailing text, no large left margin, no blank card height, line-by-line stat rows, readable text, and small right padding. Send the render when the user asks to see it.
- When the user reports `fatal: No url found for submodule path ... in .gitmodules`, do not repeat broad `git submodule update --init --recursive` advice. Either fix the missing `.gitmodules` mapping or give a path-scoped OSRS submodule update for the plugin being worked on.
- Do not consolidate repos before first producing and reviewing a cleanup plan; these plugins represent different product lanes.
