# Viral Radar Performance Learnings

Last updated: `2026-08-04T01:02:58.572469+00:00`

## Metrics status

- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.
- This preserves private/unlisted visibility and prevents mixing channel accounts.

## viral-clip-radar

- Uploads logged: 402 total; 378 public/metric-eligible.
- Median public views in latest snapshot: 2.
- Current winners to study:
  - 1335 views / 18 likes / 0 comments — Alex Hormozi: Whoever You Blame Is Who You Give Power To — https://youtu.be/8vdPqKeijgw — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1253 views / 10 likes / 0 comments — Alex Hormozi: Download Free Scaling Roadmap — The Desire Gap Nobody Admits — https://youtu.be/lrkae-8_njY — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1234 views / 10 likes / 0 comments — Alex Hormozi: If the Truth Isn't Compelling, Fix That — https://youtu.be/BZ03CWhpuSk — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1157 views / 10 likes / 0 comments — Luke Belmar: the part people will replay — https://youtu.be/NfjW1diW8NM — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1036 views / 18 likes / 1 comments — Two types of procrastination and how activation changes behavior #Shorts — https://youtu.be/XJ4QzlHq2TE — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
- Hook/title words showing up in better performers: source, alex, youtube, radar, hormozi, https, vertical, captions, context, attribution, original, burned.

## Operating rule for future Viral Radar runs

- Before clipping the next influencer video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.
