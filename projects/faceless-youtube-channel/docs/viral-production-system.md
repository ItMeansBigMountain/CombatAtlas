# Faceless Channel Viral Production System

Use the shared playbook at `/opt/data/HeRmEz/projects/_ops/social-growth/VIRAL_GROWTH_PLAYBOOK.md` as the source of truth.

## Current operating cadence

- **1 Short/day minimum** during a 30-day sprint.
- Test upload windows in Central Time: **2–4 PM** and **8–10 PM** for YouTube Shorts.
- If also posting TikTok: **7–9 PM weekdays** first; then test **7–9 AM Tue/Thu/Fri**.
- If also posting Instagram Reels: **11 AM–1 PM** and **7–9 PM**.
- Long-form, when ready: publish Thu/Fri afternoon or evening, then create 3–7 shorts from it.

## Faceless visual system

The channel should look like a serious discipline dashboard, not generic AI stock footage.

### Scene types

1. **Dopamine meter** — red/orange consumption bar drains; cyan/green discipline bar fills.
2. **Identity split-screen** — left side “old loop,” right side “new standard.”
3. **System checklist** — 3–5 hard rules with checkmarks appearing on beat.
4. **Career receipts** — terminal logs, cloud diagrams, job-search board, shipped-project counter.
5. **Fatherless systems map** — chaos → rules → receipts → confidence flowchart.
6. **Prayer/gym/code triangle** — faith/body/work pillars as a recurring motif.
7. **Temptation strike-through** — food/weed/scroll icons crossed out, replaced by one action.
8. **Timeline compression** — “Day 1 → Day 30 → 6 months” progress lanes.

### Style tokens

- Background: `#071018` / `#020617` dark navy-black.
- Cards: `#111827` with slate borders.
- Discipline/system: cyan `#38BDF8`.
- Receipts/proof: green `#22C55E`.
- Temptation/friction: orange `#F97316`, red `#EF4444`.
- Reward/win: yellow `#FACC15`.
- Typography: bold all-caps hooks, short line lengths, captions always burned in.

## Script structure for Shorts

```text
0–2s: painful hook
2–8s: name the hidden mechanism
8–20s: show the system/receipt
20–35s: one actionable rule
35–45s: challenge/comment prompt
```

## Automation rules

- `scripts/run_graphic_video.py --upload` already uploads private through the shared uploader and removes the per-video workspace after upload unless `--keep-workspace` is passed.
- Keep local workspaces when upload is not requested so renders can be reviewed.
- Do not delete source metadata, upload logs, or strategy docs.
- Add new visual primitives to `graphic_filters()` rather than adding expensive stock/video dependencies first.

## Clip titles to test first

- `AI Did Not Make You Lazy — It Exposed You`
- `Fatherless Men Need Systems, Not Motivation`
- `Dopamine Is Quietly Killing Your Comeback`
- `No Degree, No Excuse: Build Receipts`
- `Before You Open TikTok, Write One Standard`
