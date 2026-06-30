# stockNews / stock_news_backend — Retired Context

Status: retired from active app hosting as of 2026-06-29.

## What this project is
A stock/news dashboard/backend idea for aggregating market news, broker/portfolio context, and analysis into a user-facing app.

Useful files:
- `PRODUCT_DIRECTION.md`
- `DEVELOPMENT_PLAN.md`
- `readme.md`
- `stock_news_backend/api/index.py`
- `stock_news_backend/core/views.py`
- `stock_news_backend/analysis.json`
- `stock-news-frontend/src/app/stock.service.ts`
- `stock-news-frontend/src/app/portfolio-dashboard/*`

## Current decision
Retire as a standalone hosted backend because Hermes already runs Robinhood/market/news cron jobs and MCP-backed account inspections. Keep the idea, not the deployed backend.

## Ideas to incorporate into cron/Agentic trading
- Daily market/news briefing tied to actual positions.
- Portfolio dashboard-style summary: account value, positions, P/L, buying power, notable news/catalysts.
- Watchlist/candidate sentiment scoring.
- Explicit separation between source/news signals and trade execution gates.

## If revived later
Revive only as a UI/dashboard over the existing Hermes cron + Robinhood MCP pipeline, not as a separate duplicate backend.
