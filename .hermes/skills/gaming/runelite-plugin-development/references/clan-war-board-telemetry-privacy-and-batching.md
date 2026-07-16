# Clan War Board telemetry privacy and batching

Use this when continuing Clan War Board RuneLite plugin/service work after the PvP tracking research and first telemetry slice.

## Durable product decisions

- Online sync is required for Clan War Board; do not reintroduce an `Enable Online Sync` disable option.
- Members must have a setting controlling whether their player-level performance appears publicly on the website.
  - Current plugin setting: `Show My Player Stats Publicly`.
  - Default must be `false`.
  - Clan-level telemetry can still sync while the member's public website identity is hidden.
- Fight worlds are intentionally public. The user wants world visibility to help revive Wilderness activity.
- Private-by-default data should focus on member/player identity and leader notes/rally details, not the world.
- If public tracking creates problems, the operational plan is to ship an update rather than over-block public world visibility up front.

## Anti-lag telemetry pattern

The user explicitly warned that wars may have ~200 visible players per client and API calls can explode exponentially. Do **not** poll or upload every visible player every tick/frame.

Preferred MVP plugin pattern:

1. Track only local-player-observable events first.
2. Queue events locally in memory.
3. Flush small batches on a timer or important terminal events.
4. Never send one HTTP request per visible player, per hitsplat, or per frame.
5. Use backend aggregation/merge to combine multiple clients' points of view.

Current constants from the first implementation:

- Max batch size: `50` events.
- Minimum flush interval: `10s`.
- Heartbeat interval: `100` game ticks.
- Death/kill-candidate events may flush immediately.

Current plugin classes:

- `ClanWarBoardTelemetryEvent`
- `ClanWarBoardTelemetryBuffer`
- `ClanWarBoardApiClient.submitTelemetry(...)`

Current event types:

- `heartbeat`
- `damage_dealt`
- `damage_taken`
- `death`
- `kill_candidate`

Current service endpoint:

```text
POST /api/plugin/events/batch
```

Response policy currently includes:

```json
{
  "worldIsPublic": true,
  "playerWebsiteTrackingDefaultsPrivate": true,
  "recommendedClientFlushSeconds": 10,
  "recommendedMaxEventsPerBatch": 50
}
```

## Current limitation / next slice

The live endpoint validates and accepts batches, but the first slice does not persist them into Cosmos yet. The next vertical slice should add persistence/materialization:

- wire service managed API to Cosmos settings/dependency,
- persist raw telemetry batches/events,
- aggregate fight summaries,
- calculate winner/confidence,
- update public leaderboard snapshots,
- apply member public-player privacy during public materialization.

## Verification pattern

For plugin work:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

For service work:

```bash
python3 -m unittest discover -s tests -v
```

Live endpoint smoke shape:

```bash
curl -fsS -X POST 'https://salmon-dune-01c80c60f.7.azurestaticapps.net/api/plugin/events/batch' \
  -H 'Content-Type: application/json' \
  --data '{"events":[{"type":"heartbeat","playerName":"private","clanName":"TRAPISTAN","world":330,"tick":1,"timestamp":123,"playerPublic":false}]}'
```

Expected: `ok: true`, `accepted >= 1`, `worldIsPublic: true`, `playerWebsiteTrackingDefaultsPrivate: true`.
