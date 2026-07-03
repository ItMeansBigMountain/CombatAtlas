# Social Video Performance Learnings

Last updated: `2026-07-03T01:53:03.353093+00:00`

## Metrics status

- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.
- This preserves private/unlisted visibility and prevents mixing channel accounts.

## faceless-youtube-channel

- Uploads logged: 242 total; 233 public/metric-eligible.
- Median public views in latest snapshot: 5.0.
- Current winners to study:
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 203 views / 1 likes / 0 comments — Print On Demand (POD) Management — https://youtu.be/K2nMayJr8Oo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 134 views / 0 likes / 0 comments — Bezos' AI engineer 🤖, SpaceX record IPO 💰, building vertical agents 👨‍💻 — https://youtu.be/g4c5O0DI-ys — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 121 views / 1 likes / 0 comments — The Terror of Knowing What The World Is About — https://youtu.be/b6QcYwU9SPo — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 107 views / 0 likes / 0 comments — Anthropic Fable shutdown , GLM-5.2 , OpenRouter Fusion — https://youtu.be/hjwDcBryTQ8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
- Hook/title words showing up in better performers: https, cash, sosaioyama, venmo, will, people, tools, output, read, into, proof, today.

## viral-clip-radar

- Uploads logged: 34 total; 19 public/metric-eligible.
- Median public views in latest snapshot: 131.
- Current winners to study:
  - 1036 views / 18 likes / 1 comments — Two types of procrastination and how activation changes behavior #Shorts — https://youtu.be/XJ4QzlHq2TE — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 944 views / 26 likes / 0 comments — The viral moment is not the landing. It is proof under pressure. #Shorts — https://youtu.be/JBX3lRhKhy4 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 919 views / 24 likes / 0 comments — The viral moment is not the landing. It is proof under pressure. #Shorts — https://youtu.be/ParX8IBet5I — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 828 views / 10 likes / 0 comments — One bad day is normal. Letting it become your identity is the trap. #Shorts — https://youtu.be/7EhcyS1U4d8 — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
  - 741 views / 16 likes / 2 comments — Most people confuse hard work with the thing that actually scales. #Shorts — https://youtu.be/wjo6nMGAWgk — metrics account: Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) via /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
- Hook/title words showing up in better performers: source, radar, clip, https, transformative, additions, vertical, captions, hook, context, attribution, youtube.

## Operating rule for future cron runs

- Before generating the next video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.
