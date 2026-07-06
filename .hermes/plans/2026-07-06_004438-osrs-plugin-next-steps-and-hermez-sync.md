# OSRS Plugin Next Steps and HeRmEz Sync Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Stabilize `WhosGrindingPanel`, then consolidate the OSRS plugin workspace into a smaller set of canonical repos while keeping `/opt/data/HeRmEz` pullable with correct submodule pointers.

**Architecture:** Treat each active OSRS plugin as an independent child repo/submodule, with the parent `HeRmEz` repo holding only stable submodule pointers, workspace docs, and cleanup plans. Child repo changes must be built, committed, pushed, and verified before updating the parent submodule pointer. Use `GITHUB_ACCESS_TOKEN` for authenticated GitHub operations.

**Tech Stack:** Java 11, Gradle, RuneLite plugin API, Git submodules, GitHub HTTPS remotes.

---

## Current Verified State

Verified on 2026-07-06:

- Parent repo: `/opt/data/HeRmEz`
- GitHub auth source: `GITHUB_ACCESS_TOKEN`
- Active local OSRS child worktrees are clean and match their remote branch heads:
  - `BossReadinessScore` → `2314946` OK
  - `CompetitionOverlay` → `a5f65a7` OK
  - `IceBarrageTimer` → `0a52bcb` OK
  - `PersonalProgressTimeline` → `eda0d9f` OK
  - `RivalRadar` → `cd05284` OK
  - `SmartHiscoreLookup` → `07c56d3` OK
  - `WhosGrindingClanPanel` → `3d38a31` OK
- Parent `.gitmodules` includes those 7 active OSRS submodules plus `_templates/osrs-plugins-boilerplate`.
- Parent repo currently has unrelated dirty/untracked files from other automation/trading/video work. Do **not** stage those during OSRS cleanup.
- Parent `git submodule status --recursive` currently reports a mapping problem for `projects/viral-clip-radar`; this is unrelated to OSRS but should be cleaned separately because it affects recursive submodule commands.

---

## Target Canonical Plugin Set

Keep these as active top-level OSRS workspace projects:

1. `WhosGrindingClanPanel` / product name: **Who's Grinding Panel**
2. `SmartHiscoreLookup` / product direction: account/player intelligence
3. `RivalRadar` / product direction: rival, race, streak, nemesis consolidation
4. `BossReadinessScore` / product direction: best-in-slot/current gear readiness tab
5. `IceBarrageTimer` / product direction: target freeze/barrage timer
6. `PersonalProgressTimeline` / product direction: player progression timeline
7. `CompetitionOverlay` / product direction: larger future competition idea
8. `_templates/osrs-plugins-boilerplate` / template only, not an active plugin product

Already removed from default parent checkout per `projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md`:

- `GroupIronProgressBoard`
- `AccountLegacyCard`
- `NameChangeWatcher`
- `SkillNemesis`
- `SkillRaceCreator`
- `BossRaceCreator`
- `BossKCRivalLookup`
- `BossStreaks`
- `SkillStreaks`
- top-level `osrs-plugins-boilerplate` outside `_templates/`

---

## Phase 1: Stabilize Who's Grinding Panel

### Task 1: Confirm WhosGrindingPanel current source state

**Objective:** Establish exact current code before modifying behavior.

**Files:**
- Inspect: `projects/osrs-plugins/WhosGrindingClanPanel/src/main/java/com/itmeansbigmountain/whosgrindingclanpanel/WhosGrindingClanPanelPlugin.java`
- Inspect: `projects/osrs-plugins/WhosGrindingClanPanel/src/main/java/com/itmeansbigmountain/whosgrindingclanpanel/WhosGrindingClanPanelPanel.java`
- Inspect: `projects/osrs-plugins/WhosGrindingClanPanel/src/main/java/com/itmeansbigmountain/whosgrindingclanpanel/WhosGrindingClanPanelConfig.java`
- Inspect: `projects/osrs-plugins/WhosGrindingClanPanel/src/main/java/com/itmeansbigmountain/whosgrindingclanpanel/SocialTrackingService.java`

**Steps:**

1. Run:
   ```bash
   cd /opt/data/HeRmEz/projects/osrs-plugins/WhosGrindingClanPanel
   git status --short --branch
   git log -5 --oneline
   ```
2. Verify clean working tree before edits.
3. Read current scanner methods and UI rendering methods.
4. Note whether `showOfflineFriends()` already exists and where it is used.

**Expected:** clean tree at current `main` head.

---

### Task 2: Remove clan-specific source from the panel UI

**Objective:** Make the product a general friends/player activity panel, not clan-first.

**Files:**
- Modify: `WhosGrindingClanPanelPlugin.java`
- Modify: `WhosGrindingClanPanelPanel.java`
- Modify: `SocialSourceFilter.java` or equivalent source enum
- Modify: `README.md`
- Modify: `plugin.json`
- Modify: `runelite-plugin.properties`

**Steps:**

1. Remove or hide `Clan Chat` from the source dropdown.
2. Keep `Friends List` and `Friends Chat` sources.
3. Keep the code extensible so clan support can return later, but do not show broken clan source in the UI.
4. Rename all user-facing labels from `Who's Grinding Clan Panel` to `Who's Grinding Panel`.
5. Update metadata tags to prioritize `friends`, `activity`, `grind`, `skills`, `xp`.

**Verification:**

```bash
cd /opt/data/HeRmEz/projects/osrs-plugins/WhosGrindingClanPanel
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

Expected: `BUILD SUCCESSFUL`.

---

### Task 3: Make offline friends a clear boolean option

**Objective:** Add or verify a config checkbox that controls whether offline friends render.

**Files:**
- Modify: `WhosGrindingClanPanelConfig.java`
- Modify: `WhosGrindingClanPanelPlugin.java`
- Modify: `README.md`

**Implementation details:**

- Add/verify config item:
  ```java
  @ConfigItem(
      keyName = "showOfflineFriends",
      name = "Show offline friends",
      description = "Show offline friends in the friends list source. Disable to show only online friends."
  )
  default boolean showOfflineFriends()
  {
      return false;
  }
  ```
- In the friends-list scanner, include a friend only when:
  ```java
  config.showOfflineFriends() || friend.getWorld() > 0
  ```

**Verification:** build passes and README documents the behavior.

---

### Task 4: Add at-a-glance activity icons

**Objective:** Show quick visual status per player without needing to click into detail.

**Files:**
- Modify: `WhosGrindingClanPanelPanel.java`
- Modify/create if needed: player row model or renderer helpers

**Suggested icon vocabulary:**

- `🟢` online / visible world
- `⚫` offline
- `⚔` combat/bossing clue if available later
- `⛏` skilling/activity clue if available later
- `?` unknown activity

**YAGNI scope for first pass:**

- Do not build full activity inference yet.
- Show online/offline/world state reliably.
- Add a placeholder `activitySummary` field or helper so future XP/tracker enrichment can plug in.

**Verification:** build passes; panel row width remains within RuneLite sidebar width.

---

### Task 5: Add click-to-detail scaffold

**Objective:** Clicking a player row opens a detail section with tracker-style information.

**Files:**
- Modify: `WhosGrindingClanPanelPanel.java`
- Modify/create: detail panel helper if needed
- Reference but do not depend on: `SmartHiscoreLookup` account/player detail patterns

**First-pass detail content:**

- Display name
- Source: Friends List or Friends Chat
- Online/offline
- World number if known
- Last seen timestamp in this panel session
- Placeholder for tracker enrichment: hiscore lookup, name history, recent activity

**Verification:** build passes; clicking a row updates detail area without creating a plugin dependency.

---

### Task 6: Commit and push WhosGrindingPanel child repo

**Objective:** Push tested code before touching the parent submodule pointer.

**Commands:**

```bash
cd /opt/data/HeRmEz/projects/osrs-plugins/WhosGrindingClanPanel
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
git status --short
git add README.md plugin.json runelite-plugin.properties src/main/java/com/itmeansbigmountain/whosgrindingclanpanel
git commit -m "feat: focus whos grinding panel on friends activity"
git push "https://x-access-token:${GITHUB_ACCESS_TOKEN}@github.com/ItMeansBigMountain/whos-grinding-clan-panel-osrs.git" main
remote_sha=$(git ls-remote "https://x-access-token:${GITHUB_ACCESS_TOKEN}@github.com/ItMeansBigMountain/whos-grinding-clan-panel-osrs.git" refs/heads/main | cut -f1)
local_sha=$(git rev-parse HEAD)
test "$remote_sha" = "$local_sha"
```

**Expected:** remote and local SHA match.

---

## Phase 2: Analyze and Clean Canonical Repos

### Task 7: Build inventory of active OSRS plugins

**Objective:** Capture current purpose, status, and consolidation target for each active repo.

**Files:**
- Modify: `projects/osrs-plugins/README.md`
- Modify: `projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md`

**Steps:**

1. For each active child repo, inspect:
   - `README.md`
   - `plugin.json`
   - `runelite-plugin.properties`
   - main plugin class
   - config class
2. Summarize:
   - current features
   - missing features
   - consolidation target
   - keep/merge/archive decision

**Active repos:**

```text
WhosGrindingClanPanel
SmartHiscoreLookup
RivalRadar
BossReadinessScore
IceBarrageTimer
PersonalProgressTimeline
CompetitionOverlay
```

---

### Task 8: Define SmartHiscoreLookup as account-intel canonical repo

**Objective:** Merge conceptual features from AccountLegacyCard and NameChangeWatcher into SmartHiscoreLookup direction.

**Files:**
- Modify: `projects/osrs-plugins/SmartHiscoreLookup/README.md`
- Possibly modify: SmartHiscoreLookup source files in later implementation

**Feature targets:**

- Player lookup
- Hiscore links / hiscore data
- Account legacy/profile card
- Name-change watcher capability
- Tracker/detail panel patterns reusable by WhosGrindingPanel without a hard dependency

**Verification:** build SmartHiscoreLookup after any code change.

---

### Task 9: Define RivalRadar as rival/race/streak canonical repo

**Objective:** Merge conceptual features from SkillNemesis, SkillRaceCreator, BossRaceCreator, BossKCRivalLookup, BossStreaks, and SkillStreaks into RivalRadar direction.

**Files:**
- Modify: `projects/osrs-plugins/RivalRadar/README.md`
- Possibly modify: RivalRadar source files in later implementation

**Feature targets:**

- Rival comparison
- Skill races
- Boss races
- Skill streaks
- Boss streaks
- Nemesis/weakness analysis
- Competition-ready views

**Verification:** build RivalRadar after any code change.

---

### Task 10: Preserve standalone plugin directions

**Objective:** Keep valuable standalone plugins focused and documented.

**Repos:**

- `BossReadinessScore`: best-in-slot/current gear readiness tab
- `IceBarrageTimer`: target barrage/freeze timing
- `PersonalProgressTimeline`: personal progress visualization
- `CompetitionOverlay`: future big competition overlay idea

**Steps:**

1. Ensure each README has a concise product direction.
2. Ensure each builds.
3. Avoid merging these into RivalRadar unless user explicitly changes direction.

---

## Phase 3: Parent HeRmEz Repo/Submodule Sync

### Task 11: Update parent submodule pointer after child changes

**Objective:** Make `/opt/data/HeRmEz` pullable with the latest child repo commit.

**Commands:**

```bash
cd /opt/data/HeRmEz
git status --short --branch
git add projects/osrs-plugins/WhosGrindingClanPanel projects/osrs-plugins/README.md projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md .hermes/plans/2026-07-06_004438-osrs-plugin-next-steps-and-hermez-sync.md
git diff --cached --stat
git commit -m "chore: update osrs plugin cleanup plan and submodules"
git push "https://x-access-token:${GITHUB_ACCESS_TOKEN}@github.com/ItMeansBigMountain/HeRmEz.git" main
remote_sha=$(git ls-remote "https://x-access-token:${GITHUB_ACCESS_TOKEN}@github.com/ItMeansBigMountain/HeRmEz.git" refs/heads/main | cut -f1)
local_sha=$(git rev-parse HEAD)
test "$remote_sha" = "$local_sha"
```

**Important:** Do not stage unrelated files currently present in parent status, including trading/video/temp scripts unless explicitly requested.

---

### Task 12: Clean unrelated broken submodule mapping separately

**Objective:** Fix recursive submodule command failure caused by `projects/viral-clip-radar` having submodule-like state without a `.gitmodules` mapping.

**Current symptom:**

```text
fatal: no submodule mapping found in .gitmodules for path 'projects/viral-clip-radar'
```

**Decision needed before action:**

- Option A: make `projects/viral-clip-radar` a real submodule by adding a `.gitmodules` entry and pushing its child repo first.
- Option B: remove it from parent git index and keep it as ignored local worktree.
- Option C: convert it into a regular tracked folder after removing nested git internals, only if secrets/runtime artifacts are sanitized.

**Recommendation:** Option B unless the user wants it cloned by default with HeRmEz.

---

## Phase 4: User Pull Instructions After Sync

After the parent is pushed and verified, user can run on Windows:

```bat
cd C:\Users\faree\Desktop
git clone https://github.com/ItMeansBigMountain/HeRmEz.git HeRmEz
cd HeRmEz
git submodule sync --recursive
git submodule update --init --recursive
```

For an existing checkout:

```bat
cd C:\Users\faree\Desktop\HeRmEz
git pull origin main
git submodule sync --recursive
git submodule update --init --recursive
```

Then run a plugin locally, for example:

```bat
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\WhosGrindingClanPanel
git switch main
git pull origin main
.\gradlew.bat run --no-daemon
```

---

## Risks / Notes

- Parent repo has unrelated dirty/untracked files. Stage exact paths only.
- Child repos are submodules: child changes must be pushed before parent pointer updates.
- `WhosGrindingClanPanel` repo name can remain as-is remotely for now even if product name becomes `Who's Grinding Panel`; renaming the remote should be a later deliberate step.
- Avoid cross-plugin runtime dependencies; duplicate small UI/detail patterns where needed until a shared library is justified.
- Use Java 11 for RuneLite plugin builds via `/opt/data/jdks/current-java11`.
