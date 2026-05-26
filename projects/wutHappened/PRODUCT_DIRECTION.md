# WutHappened — Portfolio-Aware News Intelligence

## Product direction

`wutHappened` should become a portfolio-aware news intelligence product, similar to stock sentiment analysis but more personal and explanatory.

A user loads their stock portfolio, and the app finds, summarizes, and explains news that may matter to those holdings.

## Relationship to stockNews

- `stockNews` remains the existing stock sentiment demo/API baseline.
- `wutHappened` becomes the more user-facing question: “What happened today that matters to my portfolio?”
- The two can share market/news/sentiment utilities later.

## Portfolio import methods

Support multiple ways to load a portfolio:

1. OAuth/brokerage integrations where allowed.
2. CSV upload.
3. JSON upload.
4. Manual ticker/share list.
5. Vendor export imports from brokerages and finance tools.

Initial schema:

```json
{
  "positions": [
    { "symbol": "AAPL", "shares": 10, "avgCost": 180.25, "vendor": "manual" }
  ]
}
```

## Core features

- Import or enter holdings.
- Pull news for portfolio symbols, sectors, and macro topics.
- Rank articles by relevance to portfolio exposure.
- Summarize why each article may matter.
- Sentiment and risk tags: bullish, bearish, regulatory, earnings, macro, supply chain, leadership, legal.
- Daily digest: biggest movers, important news, what changed, what to watch.
- Optional generated script/video later using legacy `VideoGenerator.py`, `ScriptGenerator.py`, and `ImageGenerator.py` ideas.

## MVP screens

- Portfolio import.
- Holdings review.
- Today’s portfolio news.
- Article explanation cards.
- Sentiment/risk dashboard.
- Daily report export/email.

## Vendor/import strategy

Start with generic CSV/JSON/manual list support. Add brokerage/vendor-specific import mappers later for Robinhood, Fidelity, Schwab, E*TRADE, Coinbase, Yahoo Finance exports, or spreadsheet templates.

## Safety language

This is market/news explanation software, not financial advice. It should explain possible relevance and uncertainty, not tell the user what to buy or sell.
