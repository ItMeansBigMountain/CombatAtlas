# Stock News Backend Ideas → Agentic Trading Cron Addendum

Created: 2026-06-29

The standalone `stockNews` / `stock_news_backend` app is retired, but its useful product idea should be absorbed into Agentic Robinhood cron/reporting.

## Incorporate into Robinhood cron scans

For each scheduled Agentic Robinhood scan, include:

1. **Portfolio dashboard snapshot**
   - Account value
   - Cash / buying power
   - Current positions
   - Current quote and approximate P/L vs average cost
   - Open orders across open-ish states

2. **News/catalyst layer**
   - Position-specific news/catalysts
   - Broad market context: SPY/QQQ/index trend
   - Sector or theme context when relevant
   - Email-derived Robinhood confirmations/account notices when useful

3. **Candidate scoring layer**
   - Technical structure
   - Relative strength
   - Volume/liquidity
   - Catalyst quality
   - Risk/reward and invalidation clarity

4. **Execution gate**
   - Equities only by default
   - Respect autonomous-policy sizing/risk rules
   - No trade when setup is unclear
   - Journal every review/execution/management action

## Retired source project
Original idea source: `/opt/data/HeRmEz/projects/stockNews/PROJECT_HANDOFF_CONTEXT.md`.
