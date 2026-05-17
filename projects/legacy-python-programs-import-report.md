# Legacy python-programs Import Report

- **Date:** 2026-05-03
- **Source inspected read-only:** `C:\Users\faree\Desktop\python-programs`
- **Destination root:** `C:\Users\faree\Desktop\OpEnCLAw`
- **Rule:** Original `python-programs` files were not modified.
- **Safety exclusions:** `.git`, `.env`, credential/token/key-like files, `.pem`, pickle tokens, local SQLite DBs, caches, generated binaries/logs.

## Imported mappings

### `Financial.Market.ML` -> `portfolio-sentiment-subscription-app/legacy-src/financial-market-ml`

- **Files copied:** 92
- **Sensitive/generated/unreadable files skipped:** 4
- **Why it maps:** Existing market ML notebooks/code are a strong base for portfolio/news sentiment and market analysis.

### `Hero/news-webcrawler-app` -> `portfolio-sentiment-subscription-app/legacy-src/news-webcrawler-app`

- **Files copied:** 8
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing news crawler/newsletter code can feed sentiment/news-report features.

### `Hero/news-webcrawler-app` -> `scraper-project/legacy-src/news-webcrawler-app`

- **Files copied:** 8
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing crawler structure is directly useful for the scraper project.

### `programs/webCrawl` -> `scraper-project/legacy-src/web-crawl`

- **Files copied:** 8
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing spider/link-map and finviz scraping code.

### `programs/redditScraper` -> `scraper-project/legacy-src/reddit-scraper`

- **Files copied:** 5
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing Reddit/Twitter trend scraping scripts.

### `programs/SoundDoe` -> `music-mood-app/legacy-src/sounddoe`

- **Files copied:** 24
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing music/playlist analysis app and templates.

### `programs/clutter/CodersSchool` -> `coding-school-platform/legacy-src/coders-school`

- **Files copied:** 112
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing APIs, tutorials, projects, and marketing notes for coding school material.

### `programs/JUPYTER/Tutoring` -> `coding-school-platform/legacy-src/jupyter-tutoring`

- **Files copied:** 3
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing tutoring notebooks and notes.

### `programs/clutter/VideoGames` -> `addictive-mobile-games/legacy-src/video-games`

- **Files copied:** 9
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing starter game scripts/assets.

### `AI/Self_Playing_Game` -> `addictive-mobile-games/legacy-src/self-playing-game`

- **Files copied:** 3
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing game AI experiment.

### `programs/TweetBetweenTheLines` -> `twitter-therapy-app/legacy-src/tweet-between-the-lines`

- **Files copied:** 26
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing tweet analysis/mood scripts and Django tweetDeleter subproject.

### `programs/TweetBetweenTheLines` -> `social-media-analysis/legacy-src/tweet-between-the-lines`

- **Files copied:** 26
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing social text analysis scripts.

### `programs/stonks` -> `robinhood-email-reports/legacy-src/stonks`

- **Files copied:** 2
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing Robinhood/daytrade scripts.

### `programs/clutter/robinMail_UNF` -> `robinhood-email-reports/legacy-src/robin-mail-unf`

- **Files copied:** 19
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing Robinhood email reporting prototype.

### `programs/Persistent-GPT-api` -> `journal-ai/legacy-src/persistent-gpt-api`

- **Files copied:** 24
- **Sensitive/generated/unreadable files skipped:** 3
- **Why it maps:** Existing persistent GPT/Django API may be reusable for journal AI storage/API patterns.

### `programs/Generative-AI/hugging-face-demo` -> `store-code-content-studio/legacy-src/hugging-face-demo`

- **Files copied:** 17
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing AI demo scripts can be converted into tutorial content.

### `AI/hugging-face-demo` -> `store-code-content-studio/legacy-src/ai-hugging-face-demo`

- **Files copied:** 18
- **Sensitive/generated/unreadable files skipped:** 1
- **Why it maps:** Existing Hugging Face scripts and notes for tutorial content.

### `programs/video-generation-api` -> `store-code-content-studio/legacy-src/video-generation-api`

- **Files copied:** 4
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing video generation API scripts may help content automation.

### `programs/Generative-AI/API-Scripts-Video-Gen` -> `store-code-content-studio/legacy-src/generative-video-api-scripts`

- **Files copied:** 5
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing video generation scripts for content workflow.

### `programs/networking/Samad` -> `oyama-productions-legal/legacy-src/networking-security-learning-reference`

- **Files copied:** 11
- **Sensitive/generated/unreadable files skipped:** 0
- **Why it maps:** Existing networking/security learning scripts; reference only, not legal work.

## Skipped item notes

- `C:\Users\faree\Desktop\python-programs\Financial.Market.ML\MLTrading\.DS_Store`
- `C:\Users\faree\Desktop\python-programs\Financial.Market.ML\MLTrading\CODE\.DS_Store`
- `C:\Users\faree\Desktop\python-programs\Financial.Market.ML\MLTrading\CODE\1_Unsupervised\.DS_Store`
- `C:\Users\faree\Desktop\python-programs\Financial.Market.ML\MLTrading\CODE\2_Supervised\.DS_Store`
- `C:\Users\faree\Desktop\python-programs\Hero\news-webcrawler-app\src\services\...`
- `C:\Users\faree\Desktop\python-programs\Hero\news-webcrawler-app\src\services\...`
- `C:\Users\faree\Desktop\python-programs\programs\SoundDoe\oyama.pem`
- `C:\Users\faree\Desktop\python-programs\programs\TweetBetweenTheLines\tweetDeleter\db.sqlite3`
- `C:\Users\faree\Desktop\python-programs\programs\TweetBetweenTheLines\tweetDeleter\db.sqlite3`
- `C:\Users\faree\Desktop\python-programs\programs\Persistent-GPT-api\.env`
- `C:\Users\faree\Desktop\python-programs\programs\Persistent-GPT-api\db.sqlite3`
- `C:\Users\faree\Desktop\python-programs\programs\Persistent-GPT-api\core\templates\display_token.html`
- `C:\Users\faree\Desktop\python-programs\AI\hugging-face-demo\image-to-text\.env`

## Notable source areas not copied yet

- `NOTES/security` was intentionally not copied because it contains credential/key-like filenames.
- Discord bot folders were not copied yet because they contain bot/security/auth artifacts and need a separate secret-safe review.
- Web automation bots were not copied yet because some appear platform/login-bot related and should be reviewed before reuse.
- Large local LLM/audiocraft/vendor folders were not copied yet to avoid dragging heavy dependencies into the new project tree.
