# Autonomous Maintenance Reset Audit — 2026-08-11

## Executive decision

Do **not** restart the existing project-wide Kanban sweep as-is. It expanded into 420 cards with 105 blocked items and repeated worker protocol failures. Preserve current production workflows, reconcile the board, remove only approved stale/generated artifacts, and relaunch maintenance as small bounded batches with explicit success/failure contracts.

No files were deleted and no processes were stopped during this audit.

## Current operating state

- Disk: 96 GB total, 68 GB used, 29 GB free (71%).
- Memory: 7.8 GiB total, approximately 966 MiB available during audit; no swap.
- Kanban: 420 total — 122 done, 105 blocked, 191 todo, 2 ready.
- Diagnostics: 107 active diagnostics across 105 tasks.
- Two tasks are stranded in `ready` under unavailable/non-dispatching profiles:
  - `t_f8df6c43` — faceless direct hash deep-link, assigned `web-worker`.
  - `t_9736ebad` — journal-ai modernization, assigned `backend-developer`.
- Many workers exited cleanly without calling `kanban_complete` or `kanban_block`; this is the dominant autonomous-maintenance protocol failure.

## Production workflows to preserve

### Daily Stoic → A F

- One email produces one video.
- Upload success requires a verified YouTube video ID and expected channel match.
- Only after verification: trash the source email and delete generated media.
- On failure: preserve source identity, write durable backlog, continue to next item, retry later.
- Current defect: a deterministic 44.30-second render fails the 45-second minimum and may loop forever.
- Current state defect: backlog entries are appended but never explicitly marked resolved.
- Health defect: top-level Gmail discovery/auth errors can exit with code 0 and appear healthy.

### Viral Clip Radar

- Production contract must be enforced **per selected source**, not globally.
- Current run reported success after five uploads spread over multiple sources while four Ryan Holiday clips remained pending.
- Pending clips were not materialized into `UPLOAD_QUEUE`.
- Source acquisition is degraded by YouTube bot checks, HTTP 403/400 responses, and a missing/unused cookie file.
- TateSpeech and Capital Club Community playlist IDs currently return `playlistNotFound`.

## Blocked-item classification

### 1. Systemic/stale Kanban sweep — reconcile, do not blindly retry

- 105 blocked tasks, many approximately 1,500–1,583 hours old according to scheduler timestamps.
- Repeated failure modes:
  - worker exits without terminal Kanban call;
  - dead worker PID;
  - nonexistent/inactive assignee profiles;
  - deployment/smoke-test tasks created for projects that may not be deployable apps;
  - downstream tasks created before classification evidence existed.
- Reset action:
  1. Back up `/opt/data/kanban.db`.
  2. Freeze the old sweep controller `t_d328547f`.
  3. Reconcile cards project by project: complete with evidence, cancel as obsolete, or rewrite with a real blocker.
  4. Reassign only to profiles returned by live profile discovery.
  5. Relaunch at most 2–3 heavy workers concurrently.

### 2. Active production blockers — fix, retain data

- Daily Stoic 44.30-second duration failure for Gmail message `personal-secondary/19f8e38d853bfc0a`.
- Viral Radar download/auth degradation.
- Viral Radar per-source success accounting and missing durable queue entries.
- These are not deletion targets.

### 3. Intentional gates — leave in place

- Who’s Grinding remains in `pr-review-pending`; wait for Plugin Hub merge/visibility.
- Clan War Board remains in progress until manual RuneLite verification, release pinning, manifest/CI, and submission gates are satisfied.
- Keep Ryan Holiday source files `V9sm6z2Ce7g` and `28MUVg0oTGg`; four clips remain pending.

## Deletion candidates — approval required

### Tier A: generated/empty artifacts, low risk

1. 41 zero-byte failed downloads under `viral-clip-radar/SOURCES/`.
2. Generated Terraform cache:
   - `osrs-plugins/services/clan-war-board-service/infra/terraform/.terraform`
   - approximately 251 MB; reproducible.
3. Kanban workspace SDK/build residue:
   - `/opt/data/kanban/workspaces/t_d9fceed6/dotnet` — approximately 578 MB.
   - associated workspace totals approximately 1.1 GB; inspect project copy before removing whole workspace.
4. Stale lock path `viral-clip-radar/STATE/viral_radar_upload.lock` only after proving no process holds the lock. Prefer changing observability so file existence is not interpreted as lock ownership.

### Tier B: misplaced/duplicate/explicitly scrapped

1. `/opt/data/HeRmEz/projects/viral-clip-radar/SECURITY_SOURCE_ARCHIVE` — 5.3–5.4 MB, unrelated and untracked. Delete from this repo or relocate the EvilQR Git bundle if intentional archival history is needed.
2. `/opt/data/HeRmEz/projects/whos-grinding-clan-panel-osrs` — stale duplicate of canonical nested checkout; verify no scripts reference the old path first.
3. Explicitly scrapped OSRS repos:
   - `ice-barrage-timer-osrs`
   - `personal-progress-timeline-osrs`
   - `rival-radar-osrs`
   - `smart-hiscore-lookup-osrs`

### Tier C: review before any deletion

- Failed Daily Stoic workspace `videos/20260811-013736-they-have-been-misled/`; retain until corrected retry succeeds and source email availability is verified.
- July 7 `UPLOAD_QUEUE_HOLD` item; hold queues are protected state.
- Large old project areas requiring owner classification:
  - `_vercel_mvp` — 4.0 GB
  - `_vercel_mvp_safe` — 1.9 GB
  - `_vercel_mvp_fix` — 389 MB
  - `_tmp` — 2.8 GB, recently active
  - `legacy-src` — 1.3 GB
- Analytics directories are large but are retained operational state, not routine cleanup targets.

## Fresh autonomous-maintenance contract

Every autonomous job must implement the same lifecycle:

1. **Identify** — stable source identity and idempotency key.
2. **Preflight** — credentials, expected account/channel, resource headroom, duplicate ledger, lock ownership.
3. **Execute** — bounded concurrency, timeout, checkpoints, deterministic workspace.
4. **Verify** — validate the real external artifact, not only process exit code.
5. **Commit success** — immutable ledger, URL/ID, resolved backlog marker.
6. **Cleanup** — delete only disposable media/build artifacts after verified success.
7. **Commit failure** — nonzero/blocked status, exact error class, source retained, retry count and next retry time.
8. **Continue** — isolate item failure; do not abort the whole batch unless preflight/system health fails.
9. **Reconcile** — daily stale-lock, orphan, queue-vs-ledger, backlog-resolution, and resource review.

## Error policy

- Transient network/auth: exponential backoff with jitter, bounded attempts, then durable backlog.
- Deterministic validation failure: mutate the input or strategy before retry; never rerun identical work indefinitely.
- External success ambiguity: fail closed; do not delete source or media.
- Resource pressure: pause starting new heavy work when available RAM is below a configured threshold; current host has no swap.
- Worker protocol violation: task is blocked automatically with logs; do not retry unchanged.
- Cleanup: manifest/ledger-aware first, age-based second; never delete queues, source emails, credentials, upload ledgers, or active workspaces.

## Completed Daily Stoic batch addendum — 2026-08-11 01:44 UTC

The manually launched batch exited with process code `0` after mixed results:

- Verified public upload: `https://youtu.be/4cbhLX4n2hs`; source email trashed and generated media cleanup recorded.
- Verified public upload: `https://youtu.be/hcUSFZGgeuY`; 46.319 seconds, source email trashed, and `final.mp4` deleted.
- Backlogged duration failure: `personal-secondary/19f8e38d853bfc0a`; 44.30 seconds.
- Backlogged duration failure: `personal-secondary/19f83ed2bee46ea2`; 38.06 seconds.

There are now two durable Daily Stoic backlog files. Both source emails remain retained. The completed process no longer exists. Its zero exit code despite two item failures confirms that cron-level health cannot rely on process exit alone; the wrapper must emit a partial/blocked result or nonzero exit when unresolved items remain.

Current failed workspaces remain deletion-protected until corrected retries succeed. The audit found media still present in `20260811-013736-they-have-been-misled` and `20260811-014215-this-is-how-you-change`.

## Diagram

See `/opt/data/HeRmEz/projects/OPERATIONS_MAINTENANCE_DIAGRAM.svg`.
