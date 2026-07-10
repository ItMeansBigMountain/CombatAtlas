# Who's Grinding Panel: WOM selected-period grinding summaries

Session learning from implementing the detail-card `Grinding` field.

## Product correction

For this plugin, `Grinding` should mean: **what the selected player has been doing during the configured gains period**, not where the plugin discovered them socially.

Do not use source-only text such as `Friends chat • world 486` as the final Grinding value in the selected-player detail card. Social discovery/source data can remain in list rows or filters, but the detail card should focus on tracker/profile data.

## Wise Old Man gained endpoint

Use Wise Old Man's gained API for the selected player and configured period:

```text
https://api.wiseoldman.net/v2/players/{urlEncodedName}/gained?period={day|week|month|year}
```

Period mapping from `GainsPeriod`:

- Day -> `day`
- 7 days -> `week`
- 30 days -> `month`
- 365 days -> `year`

The response contains:

```text
data.skills.<metric>.experience.gained
 data.bosses.<metric>.kills.gained
 data.activities.<metric>.score.gained
```

Summarize **all positive gains** into line-by-line compact sidebar rows, not just a top-N subset. The user specifically corrected that they want to see every stat found with `+` gains so tracking can be audited.

```text
Ranged: +420,000 xp
Slayer: +180,000 xp
Zulrah: +43 kc
Clue Scrolls Hard: +3 score
```

Do not duplicate the gain type by appending `(XP)`, `(KC)`, or `(Score)` after values; the value suffix already says `xp`, `kc`, or `score`, and the section/icon provides the category.

Skip `skills.overall` when listing grinding items; it hides what the player actually trained.

## UX / implementation pattern

- Fetch selected/clicked players asynchronously; avoid blocking the RuneLite sidebar.
- Before reading gained data, call WOM's player create/update endpoint:
  ```text
  POST /v2/players/{urlEncodedName}
  ```
  Then call the gained endpoint. This makes newly discovered social usernames trackable before summaries are read.
- Cache by normalized player name + period.
- Show a loading line while fetching and a graceful fallback such as `Could not load Wise Old Man gains. Use the WOM link below.`
- Add a config toggle/warning when external lookup is enabled because the selected player name is sent to Wise Old Man.
- Keep WOM/TempleOSRS/official hiscore URLs in the card; remove a separate `Sources` line from the selected-player card unless the user asks for it again.
- If later implementing "load everyone on the server / social list" behavior, do it as a throttled queue with explicit pacing and dedupe, not as an eager bulk POST loop every scan. This protects WOM, keeps Plugin Hub review safer, and avoids UI/network spikes.

## Official hiscores fallback

The official hiscores fallback exists to compute period gains by cutting the difference between current official totals and a local baseline snapshot from the configured plugin lookback period.

Current stable fallback in this repo uses the official lite CSV endpoint:

```text
https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={urlEncodedName}
```

Do **not** casually swap this path to the JSON endpoint in a final/passive cleanup if WOM or player finding regresses. If researching JSON (`index_lite.json`) for newer metrics such as Sailing/new bosses, do it as a deliberate branch/tested change: verify WOM lookup still works for known players like `oyama`, verify fallback parsing against live official hiscores, and keep WOM as the primary source.

The baseline/lookback period is selected in plugin settings (`GainsPeriod.days()`: Day/7/30/365). For period gains, save a current local snapshot and compare it only against a local baseline snapshot at or before the configured lookback. Do not compare against a too-recent baseline and present it as a full 7/30/365-day gain; show the baseline-needed message instead.

## Search/rescan UX lessons

- The logged-in profile row should be an editable search field, autofilled with the current RuneLite username but rewritable in-place; pressing Enter/search loads that player's grinding card even if they are not visible in social sources.
- Rescan must feel like it refreshes real data, not merely updates a status message. Clear stale gained-summary cache on refresh and reload WOM/current fallback data for the selected/search player.
- If the user says they cannot find players they previously could find, first restore the known-good WOM flow before extending fallback parsing.

## Tests to add

- Unit-test the gained JSON parser with skills, bosses, and activities.
- Verify names are URL encoded consistently with the links.
- Verify zero-gain periods produce a concise no-gains message.
