# Post-Morning Agentic Market Scan

Session learning: after the user's normal morning operator report, they want a separate Agentic portfolio scan focused on the Robinhood sandbox account.

## Timing

- Run after the morning report, not inside the main morning report.
- Current scheduled example: weekdays around `13:50 UTC` / about `8:50 AM Central`.

## Required scan contents

1. **Agentic portfolio update**
   - Account value
   - Buying power/cash
   - Positions
   - Open orders
   - Recent order/fill status when relevant

2. **Market scan**
   - SPY, QQQ, IWM or relevant broad benchmarks
   - Bullish/bearish/neutral one-line read
   - Key thing to watch today

3. **Candidate discovery beyond stale watchlists**
   - Do not rely primarily on user watchlists when they are stale.
   - Use news, source emails/newsletters, Robinhood curated lists/daily movers, web search, live quotes, tradability, and OHLCV.

4. **Technical analysis**
   - Trend vs recent moving averages when available
   - Support/resistance/invalidation
   - Volume/ATR or volatility context when available
   - Setup type and quality

5. **Fundamental/catalyst analysis**
   - What changed
   - Why it matters
   - What would disconfirm the thesis

6. **Tool/system upgrade notes**
   - Data gaps found during scan
   - Better scanners/scripts to build
   - MCP/tool improvements
   - Watchlist refresh suggestions

7. **Journal update**
   - Write `/opt/data/HeRmEz/projects/trading-journal/YYYY-MM-DD/post-morning-market-scan.md`.

## Safety

- Only use the Agentic account ending `1041` / account number `433711041`.
- Do not trade other accounts.
- Do not trade options by default.
- Stop all trading consideration if account value is below `$10`, broker state is uncertain, or risk cannot be calculated.
- If no clean setup exists, say no trade instead of forcing one.

## Output style

Concise Discord bullets. No Markdown tables unless the user specifically asks.

Recommended sections:

- Decision
- Agentic Portfolio
- Market Read
- Top Candidates
- Best Setup
- Risk / Invalidation
- Tool Upgrades
- Journal
