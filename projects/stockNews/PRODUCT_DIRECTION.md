# stockNews / wutHappened — Unified Portfolio News Intelligence

## Consolidation

`stockNews` and `wutHappened` are the same project.

Use `stockNews` as the active deployed app/codebase because it already has a live frontend/API deployment and portfolio sentiment baseline:

- Frontend: `https://stocknews-sentiment.vercel.app`
- API: `https://stocknews-api.vercel.app`

Use `wutHappened` as the merge source for the stronger product framing and legacy news/script/video generation ideas.

## Product goal

A user loads their real stock portfolio, then gets an understandable daily explanation of news, sentiment, risks, and catalysts that matter to their holdings.

The core user question is:

> “What happened today that matters to my portfolio?”

## Portfolio input methods

Support multiple import paths so the app is not blocked by one brokerage integration:

1. OAuth / vendor integrations where permitted.
2. CSV upload.
3. JSON upload.
4. Manual ticker/share list.
5. Vendor exports from Robinhood, Fidelity, Schwab, E*TRADE, Coinbase, Yahoo Finance, spreadsheets, or future brokerage APIs.

Initial generic schema:

```json
{
  "positions": [
    {
      "symbol": "AAPL",
      "shares": 10,
      "avgCost": 180.25,
      "vendor": "manual"
    }
  ]
}
```

## Core functionality

- User authentication / profile.
- Portfolio CRUD.
- Import/export portfolio.
- Pull latest news by symbols, sectors, and macro topics.
- Rank news by relevance to portfolio exposure.
- Analyze sentiment: bullish, bearish, mixed, neutral.
- Label risk/catalyst types: earnings, regulatory, macro, supply chain, legal, leadership, product launch, analyst rating, sector rotation.
- Explain why each article matters in plain English.
- Show stock-level and portfolio-level sentiment.
- Create a daily report/email: biggest movers, most relevant news, sentiment shifts, and watchlist.
- Optional generated recap script/video using `wutHappened` legacy `ScriptGenerator.py`, `ImageGenerator.py`, and `VideoGenerator.py` ideas.

## MVP screens

- Portfolio import / manual entry.
- Holdings dashboard.
- Today’s portfolio news.
- Article explanation cards.
- Sentiment/risk dashboard.
- Daily report preview/export/email.
- Settings for news sources and report schedule.

## Merge plan

### Keep from `stockNews`

- Existing live frontend/API deployment.
- Portfolio sentiment demo flow.
- Yahoo Finance RSS heuristic sentiment fallback.
- Future Watson NLU integration hook.
- Frontend portfolio UX and API structure.

### Keep from `wutHappened`

- “What happened?” daily explanation framing.
- News aggregation experiments.
- Generated scripts/images/videos as optional report formats.
- Portfolio-aware news relevance idea.

## Safety language

This is market/news explanation software, not financial advice. It should help the user understand news context and portfolio exposure, not tell the user what to buy, sell, or hold.
