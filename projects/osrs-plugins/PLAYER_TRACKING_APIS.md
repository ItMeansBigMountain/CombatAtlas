# OSRS Player Tracking APIs for Plugin Detail Panels

This note captures external player-progress services to evaluate for Who's Grinding Panel / SmartHiscoreLookup / RivalRadar detail views.

## Wise Old Man

- Web: https://wiseoldman.net
- API docs: https://docs.wiseoldman.net
- API base: `https://api.wiseoldman.net/v2`
- Useful endpoints:
  - `GET /players/search?username=<partial>&limit=<n>`
  - `POST /players/:username` to update/track a player
  - `GET /players/:username` for player details and latest snapshot
  - `GET /players/:username/gained?period=week` or `startDate/endDate` for gains like the web `/players/Oyama/gained` page
  - `GET /players/:username/snapshots/timeline?metric=overall&period=week` for graph datapoints
  - `GET /players/:username/names` for name changes
  - `GET /players/:username/achievements`, `/records`, `/competitions`, `/groups`
- Strong fit for our detail panel:
  - table of gained metrics: skill/activity, exp, levels, rank, EHP/EHB
  - compact sparkline/timeline for selected metric
  - current week/day/month filters
  - name change and group/competition context
- Caveat: API requests from this environment received HTTP 403 without browser-like headers or possibly due WAF/rate restrictions. In-plugin usage needs respectful User-Agent, rate limiting, opt-in warning/config, and caching.
- Docs explicitly recommend bulk group gains/hiscores when querying many members rather than per-player calls.

## TempleOSRS

- Web: https://templeosrs.com
- API docs: https://templeosrs.com/api_doc.php
- Strong coverage:
  - player info/stats/gains/datapoints/competitions
  - group member stats and group gains
  - competition info/standings
  - collection log and pets
  - EHP/EHB/rates-style competitive tracking
- Strong fit for clans/groups and competitive tracking. Temple is common for clan skill-of-the-week / boss-of-the-week style competitions.
- Caveat: endpoint shapes are older/PHP-style in places; build a small adapter and cache responses.

## Crystal Math Labs

- Web: https://crystalmathlabs.com
- Focus: OSRS XP tracking, records, rank/XP comparisons.
- Useful for cross-checking XP gains and historical records, but API/support may be less clean for embedded plugin detail panels than Wise Old Man/TempleOSRS.

## Official OSRS Hiscores

- Base examples use `https://secure.runescape.com/m=hiscore_oldschool/`
- Strong fit for current snapshot fallback: ranks, levels, XP, boss KC/minigames where listed.
- Limitation: no historical gains unless we store snapshots locally or use a tracker service.

## Detail panel direction

For a clicked social member, prefer:

1. Header: compact name, online/source/world, quick links to WOM/Temple/hiscores.
2. Current grinding guess: highest recent gain from Wise Old Man/Temple weekly/day gains.
3. Mini table: top 3 gained skills/bosses with XP/KC/rank/EHP delta.
4. Mini sparkline: selected metric timeline from WOM snapshots/timeline or Temple datapoints.
5. Footer: last updated, source, and config warning if external APIs are enabled.

Do not call these APIs for every player every tick. Use explicit refresh, caching, per-player click fetches, and bulk endpoints where available.
