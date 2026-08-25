# Deterministic archive and metric formulas

Runtime AI is not used by archive detection, parsing, normalization, coverage, confidence, entitlements, or metrics. Formula versions are immutable; behavior changes require a new version.

## Archive coverage (`archive-coverage@1`)

- `file_completeness = parsed_files / discovered_files`
- `confidence_score = round(schema_certainty × file_completeness, 2)`
- Confidence level: high when score ≥ 0.85; medium when score ≥ 0.60; low otherwise.
- Schema certainty constants: Spotify structured JSON 1.00; Mastodon export 0.90; X representative archive 0.80; decoded ATProto records 0.80.
- Unknown files are quarantined and lower file completeness. Unsupported schemas and archives that promote zero records abstain rather than return a result.

## Metric confidence

`score = min(1, min(events / 20, 0.50) + min(supporting_events / 10, 0.30) + min(sources / 4, 0.20))`, rounded to two decimals.

Level is insufficient when fewer than three events exist or supporting events are zero; otherwise high at score ≥ 0.80, medium at score ≥ 0.50, and low below 0.50.

## Metric cards (`metric-formula@1:<card-id>`)

- Interests: `count(label) = number of events containing at least one configured interest term for label`.
- Topics: `count(token) = number of events containing token at least once after NFKC tokenization and stop-word removal`.
- Communities: `count(name) = number of events whose community, channel, or subreddit metadata equals name`.
- Language style: `average_tokens_per_event = total_tokens / imported_events`; `unique_tokens = cardinality(all normalized tokens)`.
- Sentiment: an event is positive when matched positive terms exceed matched negative terms, negative when negative exceeds positive, and neutral on a tie or unsupported locale.
- Attention rhythm: `hourly_utc[h] = count(events where UTC hour = h)`; `weekday_utc[d] = count(events where UTC weekday = d)`.
- Media affinity: `count(name) = number of events whose creator, artist, channel, or mediaTitle metadata equals name`.
- Stated versus observed: stated is any post/message/import-note matching a label; observed is any view/listen/search/reaction matching it.
- Change over time: `midpoint = (earliest_timestamp + latest_timestamp) / 2`; early includes timestamps at or before midpoint, recent includes timestamps after midpoint.

All counts describe only the selected imported slice. They do not establish identity, intent, beliefs, causation, diagnosis, or complete platform history.

## Entitlements

Import quota is charged only after a recognized parser promotes at least one record. Free allows 2 successful imports per rolling 30 days, 262,144,000 compressed bytes, and 1 active account. Premium and Premium + AI allow 20 imports, 2,147,483,648 compressed bytes, and 10 active accounts. Rejected, malicious, unsupported, duplicate-only, or canceled uploads do not consume import quota.
