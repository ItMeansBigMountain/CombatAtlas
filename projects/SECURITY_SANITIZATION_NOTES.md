# Security Sanitization Notes
## 2026-05-03 - Legacy import secret cleanup

Before pushing legacy imports, copied files were scanned for hardcoded API keys, tokens, client secrets, bearer tokens, and passwords. Risky copied files were removed from this repo. Original source directories were not modified. Any exposed keys found in old local source should be considered compromised and rotated if still active.

Removed copied paths:

- `rubber-headphone-adapter/`
### Additional risky tracked source files removed

- `coding-school-platform/legacy-src/coders-school/API/COVID19.py`
- `coding-school-platform/legacy-src/coders-school/API/airQuality.py`
- `coding-school-platform/legacy-src/coders-school/API/ipGeolocation.py`
- `coding-school-platform/legacy-src/coders-school/API/memeGenerator.py`
- `coding-school-platform/legacy-src/coders-school/API/nasaAPI.py`
- `coding-school-platform/legacy-src/coders-school/API/rottenTomatoesAPIT.py`
- `coding-school-platform/legacy-src/coders-school/API/spotifyAPI.py`
- `coding-school-platform/legacy-src/coders-school/API/spotipyLIB.py`
- `coding-school-platform/legacy-src/coders-school/API/vinAPI.py`
- `coding-school-platform/legacy-src/coders-school/projects/twillo.py`
- `coding-school-platform/legacy-src/coders-school/repls/api.requests/meme.py`
- `coding-school-platform/legacy-src/coders-school/repls/api.requests/nasaAPI.py`
- `coding-school-platform/legacy-src/coders-school/repls/api.requests/planetDistance.py`
- `coding-school-platform/legacy-src/coders-school/repls/discordBots/discordIP.py`
- `coding-school-platform/legacy-src/coders-school/repls/discordBots/discordMeme.py`
- `coding-school-platform/legacy-src/coders-school/repls/discordBots/discordTime.py`
- `coding-school-platform/legacy-src/coders-school/repls/discordBots/sayBotDiscord.py`
- `coding-school-platform/legacy-src/coders-school/repls/discordBots/tellJokeDiscord.py`
- `coding-school-platform/legacy-src/coders-school/repls/projects/rottenTomatoes.py`
- `coding-school-platform/legacy-src/coders-school/repls/utility/sendText.py`
- `coding-school-platform/legacy-src/coders-school/tutorials/FlaskTwilio.py`
- `coding-school-platform/legacy-src/coders-school/tutorials/MeMe.py`
- `coding-school-platform/legacy-src/coders-school/tutorials/readEmails.py`
- `coding-school-platform/legacy-src/coders-school/tutorials/sendEmail.py`
- `music-mood-app/legacy-src/sounddoe/WhoDoe.py`
- `music-mood-app/legacy-src/sounddoe/api/musicAI.py`
- `music-mood-app/legacy-src/sounddoe/api/test.py`
- `music-mood-app/legacy-src/sounddoe/api/watson.py`
- `music-mood-app/legacy-src/sounddoe/bpm.py`
- `oyama-productions-legal/legacy-src/networking-security-learning-reference/EOS.py`
- `oyama-productions-legal/legacy-src/networking-security-learning-reference/apis/mist/inventory.py`
- `oyama-productions-legal/legacy-src/networking-security-learning-reference/apis/mist/test.py`
- `oyama-productions-legal/legacy-src/networking-security-learning-reference/routerScan.py`
- `oyama-productions-legal/legacy-src/networking-security-learning-reference/sshTemplate.py`
- `policy-pit-app/.env.example`
- `portfolio-sentiment-subscription-app/.env.example`
- `portfolio-sentiment-subscription-app/legacy-src/news-webcrawler-app/src/services/reddit.py`
- `portfolio-sentiment-subscription-app/src/config.py`
- `robinhood-email-reports/legacy-src/robin-mail-unf/dataMail.py`
- `robinhood-email-reports/legacy-src/robin-mail-unf/robin_stocks/authentication.py`
- `robinhood-email-reports/legacy-src/stonks/robinAPI.py`
- `scraper-project/legacy-src/news-webcrawler-app/src/services/reddit.py`
- `social-media-analysis/legacy-src/tweet-between-the-lines/tweetDeleter/core/views copy.py`
- `social-media-analysis/legacy-src/tweet-between-the-lines/tweetDeleter/core/views.py`
- `social-media-analysis/legacy-src/tweet-between-the-lines/twitter-api-v2-login-manual.py`
- `social-media-analysis/legacy-src/tweet-between-the-lines/twitterTopHashtag.py`
- `store-code-content-studio/legacy-src/generative-video-api-scripts/kling.py`
- `store-code-content-studio/legacy-src/generative-video-api-scripts/runaway.py`
- `store-code-content-studio/legacy-src/generative-video-api-scripts/veo3.py`
- `store-code-content-studio/legacy-src/video-generation-api/kling.py`
- `store-code-content-studio/legacy-src/video-generation-api/runaway.py`
- `store-code-content-studio/legacy-src/video-generation-api/veo3.py`
- `twitter-therapy-app/legacy-src/tweet-between-the-lines/tweetDeleter/core/views copy.py`
- `twitter-therapy-app/legacy-src/tweet-between-the-lines/tweetDeleter/core/views.py`
- `twitter-therapy-app/legacy-src/tweet-between-the-lines/twitter-api-v2-login-manual.py`
- `twitter-therapy-app/legacy-src/tweet-between-the-lines/twitterTopHashtag.py`
