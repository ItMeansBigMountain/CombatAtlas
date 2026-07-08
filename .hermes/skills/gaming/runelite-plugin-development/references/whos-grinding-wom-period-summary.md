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

Summarize top positive gains into compact sidebar lines, e.g.:

```text
Ranged: +420,000 xp (XP)
Slayer: +180,000 xp (XP)
Zulrah: +43 kc (KC)
Clue Scrolls Hard: +3 score (Score)
```

Skip `skills.overall` when choosing top grinding items; it hides what the player actually trained.

## UX / implementation pattern

- Fetch only for the selected/clicked player, not every visible social member.
- Cache by normalized player name + period.
- Load asynchronously (e.g. `SwingWorker`) so the RuneLite sidebar does not block.
- Show a loading line while fetching and a graceful fallback such as `Could not load Wise Old Man gains. Use the WOM link below.`
- Add a config toggle/warning when external lookup is enabled because the selected player name is sent to Wise Old Man.
- Keep WOM/TempleOSRS/official hiscore URLs in the card; remove a separate `Sources` line from the selected-player card unless the user asks for it again.

## Tests to add

- Unit-test the gained JSON parser with skills, bosses, and activities.
- Verify names are URL encoded consistently with the links.
- Verify zero-gain periods produce a concise no-gains message.
