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
- For screenshot-driven RuneLite UI polish, preserve the user's approved alignment even while changing font size. If the user says the smaller text alignment is better but the bigger font is preferred, keep the smaller-text left edge/section width and only increase font/line height.

## UI preferences for this user's OSRS plugins

- Panels should fit the default RuneLite side panel width.
- Keep domain workflows (posting fights, accepting records, private setup) inside role-aware panel pages; RuneLite config should contain durable preferences, not operational forms. Pin production service endpoints in code rather than exposing URL overrides.
- For multi-page sidebars, preserve the active top-level tab and secondary filter while drilling into details; Back should pop only the nested view. Read-only members may see cards without receiving leader click/accept actions.
- When leaders create records from a listing tab, place a compact role-gated `+` action in that tab’s header and route it into the existing setup form. Do not make record creation discoverable only through a separate setup tab.
- Treat `ClanSettings` as late-loading RuneLite state: login-time `0/0` or missing rank must self-correct on primary clan changes plus a change-detected short game-tick poll. Use `ClanSettings.findMember`, `titleForRank`, and `getMembers().size()` for primary-clan rank title and roster denominator; ignore guest events and use `ClanChannel` only as a temporary/online-presence fallback.
- Snapshot clan/player data on `ClientThread`, run HTTP/JSON work off-thread, and mutate Swing only on the EDT. Return network completions through `ClientThread` before posting chat or taking a fresh client snapshot.
- Delay count/next-event login messages until live board refresh completes, and use explicit RuneLite color tags for legibility.
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
- If WOM cannot find useful stats for a player, first preserve the working WOM-first path: `GET /v2/players/{name}/gained?period=...` is primary. Only then try `POST /v2/players/{name}` to start/update and retry gained data. Do not assume POST always works; WOM may block create/update from the plugin/runtime environment. If POST/update fails for a player not on WOM, show a clear card message telling the user to open Wise Old Man, track/update the player there, then refresh here. If the player is on WOM but has no positive gains, suggest trying a longer period (30/365 days) or checking again after XP/KC changes. In the narrow card, wrap fallbacks at roughly three words per line using `<br>` so they do not become long unreadable sentences.
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
See `references/plugin-hub-upstream-pr-validation.md` for the verified end-to-end upstream submission loop: one marker per PR, immutable SHA pinning, official packager monitoring, bundled Gson compatibility, CI log-driven fixes, and the difference between a real failure and the expected maintainer-review gate.
See `references/plugin-hub-production-hardening.md` for the post-submission production pass: inspect issue comments/reviews/check runs, remove every user-accessible development mode, address maintainer-prohibited patterns, update the existing marker PR, and verify exact parent gitlink SHAs.
See `references/osrs-consolidation-implementation-notes.md` for session-tested implementation notes, pure-service module patterns, RuneLite API probes, and child/parent push verification snippets.
See `references/runelite-side-panel-dimensions.md` for the RuneLite side-panel width budget, WhosGrindingPanel dimensions helper pattern, and Windows submodule handoff pitfall.
See `references/whos-grinding-panel-social-detail-pattern.md` for the current Who's Grinding Panel source model, profile detail UX, gains-period config, and WOM/TempleOSRS integration direction.
See `references/whos-grinding-wom-period-summary.md` for the Wise Old Man gained API pattern used to populate the selected-player `Grinding` section from the configured period.
See `references/whos-grinding-wom-regression-recovery.md` for the recovery playbook when WOM stats stop rendering and the panel falls through to official-hiscores baseline messages; includes the known-good checkpoint, WOM smoke test, and command-only console preference.
See `references/runelite-social-progress-detail-panels.md` for corrected social-source handling (Friends List/Friends Chat/Clan Chat), side-panel profile-detail UX, and WOM/TempleOSRS progress API notes.
See `references/whos-grinding-wom-detail-ui.md` for the latest wrap-up lessons: compact expandable rows, content-sized grinding cards, WOM start/update fallback, grouped skills/bosses/activities, and visual verification expectations.
See `references/whos-grinding-card-legibility-polish.md` for latest screenshot-reviewed card rules: line-by-line stats, bold gained values, safe inline symbols, tiny right padding, and three-words-per-line no-data fallback.
See `references/whos-grinding-compact-gained-lines.md` for gained-summary formatting history.
See `references/whos-grinding-final-sidebar-standards.md` for the latest user-approved final sidebar standards: approved width, line-by-line stat rows, bold gained values, no-data wrapping, and visual verification checklist.
See `references/whos-grinding-card-line-layout.md` for the latest user-reviewed card layout rule: every player-card item line-by-line, 12f/11f text, left alignment, tiny right padding, no giant HTML blobs, and no-stats fallback behavior.
See `references/whos-grinding-card-alignment-and-no-stats.md` for the latest card-alignment fix: avoid giant HTML blobs, use per-row left-aligned labels, and handle no-WOM-stats cases with start/update + retry messaging.
See `references/whos-grinding-wom-grinding-summary.md` for the current Who's Grinding Panel wrap-up target: compact expandable rows, grinding-only card UX, WOM gained API sections, start-tracking fallback, and Windows `gradlew.bat run` command.
See `references/whos-grinding-wom-rollback-and-no-wom.md` for the rollback/no-WOM lessons: known-good WOM commit, suffix removal, live `oyama` WOM probe, and explicit not-on-WOM message when POST update is blocked.
See `references/whos-grinding-card-final-polish.md` for final screenshot-driven card polish rules: every stat line-by-line, readable fonts, tight left edge, slight right padding, inline category markers, no-stats fallback, and live `oyama`-style visual verification.
See `references/boss-readiness-item-data-and-ui.md` for BIS Loadouts item-source and gear logic: research OSRS/GearScape data before filters, keep GearScape combat stats plus OSRS Wiki validation, allow main-game minigame rewards, exclude DMM/BH/seasonal rows, split 1H/2H weapon cycles, match ranged ammo compatibility, order boss defenses weakest-to-strongest, curate missing current items, and center the sidebar UI.
See `references/bis-loadouts-pr-review-and-repo-cleanup.md` for BIS Loadouts PR-ready docs, lifecycle move commands, Windows submodule handoff, and OSRS GitHub repo cleanup verification.
See `references/bis-loadouts-readme-screenshots.md` when adding or regenerating BIS Loadouts README screenshots; visually inspect assets and prefer clear explanatory images over cramped/cutoff raw sidebar captures.
See `references/clan-war-board-rank-gated-planning.md` for the CompetitionOverlay pivot into Clan War Board: rank-gated leader/member views, clan rank API probes, config-backed war setup, and Plugin Hub-safe boundaries.
See `references/clan-war-board-azure-service.md` for the service-backed Clan War Board direction: no local/share-code storage, service-owned `infra/` inside `services/clan-war-board-service`, Azure free-tier stack, static leaderboard API, WOM group import boundaries, and attacker-aware security model.
See `references/clan-war-board-high-traffic-fight-analytics.md` for the expanded Clan War Board product model: leader availability/applications, member plugin heartbeats, live fight telemetry, third-party interference metrics, read-only website boundary, layered anti-abuse stance, and narrow vertical RuneLite panel UX.
See `references/clan-war-board-service-integration-and-site-ux.md` for the latest Clan War Board service/plugin/site integration rules: required online sync, live WOM data only, OSRS Wiki imagery, direct challenges, leaderboard/winner scoring model, home-page match terms, dark burned-Wilderness/stone-castle theme, and Static Web Apps routing verification.
See `references/clan-war-board-live-service-and-plugin-sync.md` for the latest live Clan War Board service lessons: production website copy/pages, match terms at home bottom, Wise Old Man + OSRS Wiki real data, Static Web Apps managed API routing, required plugin sync with no disable toggle, and Java API smoke verification.
See `references/clan-war-board-real-time-zero-state.md` for the Clan War Board stale-data audit checklist: plugin-only clan source, valid zero registered clans, rendered-site counters, RuneLite panel wording, no fake/default fight fixtures, and live API/browser/Java smoke verification.
See `references/clan-war-board-pvp-tracking-research.md` for PvP telemetry research from PvP Performance Tracker, PvP Leaderboard, PvP-Hub, WOM/Temple/hiscores/wiki sources, recommended Clan War Board event model, scoring/confidence policy, privacy boundaries, and static snapshot scaling.
See `references/clan-war-board-telemetry-privacy-and-batching.md` for the current Clan War Board telemetry implementation rules: required sync, member public-player privacy defaulting off, public world policy, low-lag batched event uploads, live `/api/plugin/events/batch` contract, and the next Cosmos persistence slice.
See `references/clan-war-board-cosmos-registration.md` for the durable registration pattern: persistent UUIDv4 installation identity, real-clan-only upserts, private-by-default member records, development-role isolation, Cosmos production gating, and live deployment verification.
See `references/clan-war-board-secure-match-workflow.md` for canonical fight terms, deterministic terms hashing, mutual acceptance/reconfirmation, server-authority limitations, and fight-scoped telemetry gates.
See `references/runelite-role-aware-board-workflow.md` for durable panel-vs-config placement, three-tab/nested-back navigation, member read-only gating, ClanSettings roster counts, ClientThread/EDT boundaries, refreshed colored login messages, sanitized public fight projections, and unrelated-overlay stack-trace triage.
See `references/clan-war-board-azure-infra.md` for the user's preferred online service direction: no local/share-code-only storage, keep Azure infra under `projects/osrs-plugins/infra/`, and use a near-free Static Web Apps + Functions + Cosmos DB Free Tier architecture while keeping Plugin Hub repo clean.
See `references/osrs-slang-acronyms.md` for OSRS slang/acronym labels to use in narrow RuneLite UI, especially boss/raid/activity labels such as CoX, ToB, ToA, CG, KQ, KBD, LMS, BH, SW, etc.
See `references/runelite-plugin-hub-lifecycle-and-hiscore-fallback.md` for the current OSRS plugin lifecycle folder model, RuneLite Plugin Hub PR submission checklist, and WOM -> official hiscores local snapshot fallback pattern.
See `references/whos-grinding-self-row-and-acronyms.md` for the latest final-shipping lesson: pinned current-player row, concise distinct WOM error/no-gain states, and acronym verification.
See `references/whos-grinding-compact-card-rendering.md` for the latest card-rendering pitfalls: content-sized Swing cards, no blank expanded-card height, `oyama` WOM visual verification, and boss KC one-per-line formatting.
See `references/whos-grinding-detail-card-lessons.md` for latest user-reviewed sidebar detail-card rules: no heatmap, no separate Sources line when profile URLs are present, precise `Grinding` semantics, and compact vertical fields.

High-level rules:

- Current OSRS active lanes are BIS Loadouts, Who's Grinding/WhosGrindingClanPanel, Clan War Board/CompetitionOverlay, the boilerplate template, and plugin-hub.
- Treat Plugin Hub submission as a production sprint: PR-ready plugins must expose no developer, debug, mock, pretend-role, test-mode, experimental-endpoint, or development-comparison option. Remove the underlying branch/config/docs/tests, not just the label. Inspect issue comments, formal reviews, and check runs because actionable maintainer feedback may appear only in PR issue comments.
- PersonalProgressTimeline, RivalRadar, SmartHiscoreLookup, and IceBarrageTimer were scrapped and their GitHub repos/submodules deleted after explicit user direction.
- Before polishing or submitting any Plugin Hub candidate, screen its core feature against RuneLite's current `Rejected-or-Rolled-Back-Features` policy and Jagex third-party-client guidelines. A standalone build passing does not make a policy-rejected concept viable; do not submit opponent freeze/barrage timers.
- Do not revive deleted OSRS plugin ideas unless the user explicitly asks.
- Clean project dirs and submodules only after code-level bugs are verified and pushed.

- For Clan War Board specifically: do not repopulate `/clans` or the public directory from Wise Old Man/public clan directories. Clans should appear only after plugin registration/telemetry/leader registration. External sources may enrich an already-registered clan, but must not promote clans that are not using the plugin.
- Clan War Board production builds must expose no development role preview, pretend-leader/member mode, configurable service endpoint, debug authority path, or experimental network toggle. Delete the config items, enum/branches, docs, and tests—not merely the labels. Render leader controls only when both the live RuneLite clan rank and a server-issued `leader:write` capability agree. Keep the production HTTPS endpoint pinned in code.
- Clan War Board online sync is required; do not reintroduce a disable toggle. Player-level public website visibility remains opt-in/private by default, while fight worlds are public.
- For Clan War Board status or user-experience explanations, the user prefers very small, short bullets unless they ask for deep detail.

## Pitfalls

- Do not call a Plugin Hub candidate ready based only on its standalone Gradle build. Open the real upstream marker PR and treat the official `build` check as authoritative because `build=standard` compiles against RuneLite's bundled dependencies. If upstream fails, fix the standalone plugin, push a new immutable SHA, update the existing marker, and wait for the rerun. A red `RuneLite Plugin Hub Checks` result titled **Requires maintainer review** is the expected human-review gate, not a build defect; `Changes are needed` is actionable. See `references/plugin-hub-upstream-pr-validation.md`.
- For Clan War Board, treat “0 registered plugin clans” as a correct real-time state until actual plugin registrations exist. Audit API JSON, rendered website counters, browser view, RuneLite panel wording, plugin defaults, and tests before saying stale/fake clan data is gone. Remove fake defaults and fixture names from user-facing code; external directories can enrich already-registered plugin clans but must not populate/promote clans by themselves.
- Do not claim GitHub access is unavailable just because `gh` is missing; use `GITHUB_ACCESS_TOKEN` and the GitHub API fallback.
- When pushing with `GITHUB_ACCESS_TOKEN`, avoid nested single-quoted shell/Python URL construction; use a simple double-quoted/f-string token URL and verify `ls-remote` SHA equals local `HEAD` after every child and parent push.
- Do not `git add` nested plugin worktrees directly into the HeRmEz parent unless intentionally updating submodule gitlinks or backup artifacts.
- Do not leave child repo changes unpushed while updating only the parent repo.
- Do not preserve obsolete names like `WhosGrindingClanPanel` in user-facing display text when the direction is **Who's Grinding Panel**; internal package paths may change later as a deliberate migration.
- Do not interpret "remove broken clan source" as "remove Clan Chat forever." The durable product correction is: keep Clan Chat as a real source/panel, alongside Friends List and Friends Chat, but do not make the whole plugin clan-only. In current RuneLite, clan channel classes live under `net.runelite.api.clan.*`.
- Do not use `JOptionPane` as the final profile detail interaction for social/progress plugins. It is acceptable only as a temporary scaffold; replace it with an in-panel detail view before calling the UI polished.
- When adding external player tracking sources (Wise Old Man, TempleOSRS, Crystal Math Labs, official hiscores), avoid polling every visible member every tick. Use click-to-fetch, explicit refresh, caching, and bulk endpoints where available; add Plugin Hub-compliant warnings for any third-party data sent. For WOM, if a selected player is not tracked yet, POST `/v2/players/{name}` to start/update tracking, then retry the gained endpoint. For official OSRS hiscores fallback, remember that official hiscores provide current totals only; calculate period gains by saving local snapshots and comparing against an older snapshot, and show a clear baseline-needed message if no older snapshot exists.
- Do not let official hiscores fallback mask or replace working WOM stats. If a screenshot shows `Official hiscores baseline saved` for a player that should have WOM gains (known smoke-test player: `oyama`), stop feature work and restore the last known WOM-working baseline before re-adding fallback/search. Re-add search UI and fallback as separate verified changes, with a live WOM smoke test after each.
- When the user asks for just the RuneLite run command, especially “only see errors on the console,” return only the command block and no explanatory prose. Use `.\gradlew.bat run --no-daemon --console=plain --quiet 1>NUL` from the plugin directory.
- When the user reports RuneLite sidebar spacing from screenshots, treat it as a blocking UI bug. Build success is insufficient: inspect or generate a visual sidebar-width render with representative live data (e.g. `oyama` WOM gains) and verify no cutoff/trailing text, no large left margin, no blank card height, line-by-line stat rows, readable text, and small right padding. Send the render when the user asks to see it.
- When the user reports `fatal: No url found for submodule path ... in .gitmodules`, do not repeat broad `git submodule update --init --recursive` advice. Either fix the missing `.gitmodules` mapping or give a path-scoped OSRS submodule update for the plugin being worked on.
- If the user says WOM/player lookup regressed or they cannot find players they previously could find, stop extending fallback/search features and restore the known-good WOM-first flow before doing anything else. For Who's Grinding Panel, use `references/whos-grinding-wom-rollback-and-no-wom.md`; the known-good rollback point from this session was `a0e2162 feat: add player header and OSRS acronym labels`. Verify with a live WOM gained probe for `oyama` using the plugin User-Agent, run `./gradlew clean test assemble --no-daemon --console=plain`, then apply only small safe UI fixes.
- Do not consolidate repos before first producing and reviewing a cleanup plan; these plugins represent different product lanes.
