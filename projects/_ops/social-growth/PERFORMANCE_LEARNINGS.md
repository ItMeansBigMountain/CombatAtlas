# Social Video Performance Learnings

Last updated: `2026-07-06T01:05:25.677833+00:00`

## Metrics status

- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.
- This preserves private/unlisted visibility and prevents mixing channel accounts.

## faceless-youtube-channel

- Uploads logged: 326 total; 315 public/metric-eligible.
- Median public views in latest snapshot: 3.0.
- Current winners to study:
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 107 views / 0 likes / 0 comments — Anthropic Fable shutdown , GLM-5.2 , OpenRouter Fusion — https://youtu.be/hjwDcBryTQ8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 107 views / 0 likes / 0 comments — Anthropic Fable shutdown , GLM-5.2 , OpenRouter Fusion — https://youtu.be/hjwDcBryTQ8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 93 views / 0 likes / 0 comments — Devin Fusion , DeepSeek DSpark , economy of tokens — https://youtu.be/ZiFPfJuMoTo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
- Hook/title words showing up in better performers: https, cash, sosaioyama, venmo, will, people, tools, output, more, linktr, sosai, oyama.

## viral-clip-radar

- Uploads logged: 45 total; 30 public/metric-eligible.
- Median public views in latest snapshot: 98.0.
- Current winners to study:
  - 1036 views / 18 likes / 1 comments — Two types of procrastination and how activation changes behavior #Shorts — https://youtu.be/XJ4QzlHq2TE — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 1048 views / 7 likes / 0 comments — GG33 #Shorts — https://youtu.be/sew5nLYII0A — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 944 views / 26 likes / 0 comments — The viral moment is not the landing. It is proof under pressure. #Shorts — https://youtu.be/JBX3lRhKhy4 — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 919 views / 24 likes / 0 comments — The viral moment is not the landing. It is proof under pressure. #Shorts — https://youtu.be/ParX8IBet5I — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
  - 835 views / 10 likes / 0 comments — One bad day is normal. Letting it become your identity is the trap. #Shorts — https://youtu.be/7EhcyS1U4d8 — metrics account: Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) via /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
- Hook/title words showing up in better performers: source, radar, clip, https, transformative, additions, vertical, captions, hook, context, attribution, youtube.

## Operating rule for future cron runs

- Before generating the next video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.
