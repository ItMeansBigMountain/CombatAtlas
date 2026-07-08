# Social Video Performance Learnings

Last updated: `2026-07-08T07:44:22.374752+00:00`

## Metrics status

- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.
- This preserves private/unlisted visibility and prevents mixing channel accounts.

## faceless-youtube-channel

- Uploads logged: 370 total; 359 public/metric-eligible.
- Median public views in latest snapshot: 3.0.
- Current winners to study:
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 108 views / 0 likes / 0 comments — Anthropic Fable shutdown , GLM-5.2 , OpenRouter Fusion — https://youtu.be/hjwDcBryTQ8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 108 views / 0 likes / 0 comments — Anthropic Fable shutdown , GLM-5.2 , OpenRouter Fusion — https://youtu.be/hjwDcBryTQ8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 93 views / 0 likes / 0 comments — Devin Fusion , DeepSeek DSpark , economy of tokens — https://youtu.be/ZiFPfJuMoTo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
- Hook/title words showing up in better performers: https, cash, sosaioyama, venmo, will, people, tools, output, more, linktr, sosai, oyama.

## viral-clip-radar

- Uploads logged: 71 total; 56 public/metric-eligible.
- Median public views in latest snapshot: 35.0.
- Current winners to study:
  - 1336 views / 19 likes / 0 comments — Alex Hormozi: Whoever You Blame Is Who You Give Power To — https://youtu.be/8vdPqKeijgw — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1234 views / 10 likes / 0 comments — Alex Hormozi: If the Truth Isn't Compelling, Fix That — https://youtu.be/BZ03CWhpuSk — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1155 views / 10 likes / 0 comments — Luke Belmar: the part people will replay — https://youtu.be/NfjW1diW8NM — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1036 views / 18 likes / 1 comments — Two types of procrastination and how activation changes behavior #Shorts — https://youtu.be/XJ4QzlHq2TE — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1087 views / 7 likes / 0 comments — GG33 #Shorts — https://youtu.be/sew5nLYII0A — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
- Hook/title words showing up in better performers: source, radar, https, transformative, additions, vertical, captions, hook, context, attribution, original, youtube.

## Operating rule for future cron runs

- Before generating the next video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.
