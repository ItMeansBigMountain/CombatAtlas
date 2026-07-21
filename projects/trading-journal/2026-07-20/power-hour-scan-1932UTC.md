# Agentic 1041 Power-Hour Swing Scan — 2026-07-20

- Timestamp: 2026-07-20T19:32:18Z / 15:32 ET
- Account: Robinhood Agentic ••••1041 (433711041) only
- Mode: autonomous policy-gated equity management
- Decision: HOLD NVDA, SOFI, JPM; NO NEW ORDER; NO ROTATION

## Live broker state and kill switches

- MCP connected; account 433711041 verified active cash account, nickname Agentic, `agentic_allowed=true`.
- Total value $183.8066; equity value $167.1366; cash and buying power $16.67.
- Positions fully sellable: NVDA 0.121165, SOFI 4.477580, JPM 0.195159. No shares held for sells.
- Open-ish equity states checked separately: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`; all empty.
- Today's only verified fill: JPM market buy, $66.68 / 0.195159 shares at $341.6699, filled 13:53:25Z, order 6a5e2855-17cf-4546-937b-b6a129da1933.
- Kill switch clear: value above $10. Current unrealized P/L versus average costs approximately -$4.57 (-2.49% of account), below the 5% daily-pause gate. Account is about 8.10% below the original $200 funding proxy, below the 10% drawdown pause proxy. Live broker/account/risk state was sufficiently certain.
- Aggregate risk from current prices to written invalidations is approximately $4.23, within the default ~$6 open-risk target.

## Market/sector regime

- SPY $742.98 (-0.04%), below SMA10 $750.24, SMA20 $744.90 and SMA50 $743.99; below intraday VWAP $745.03.
- QQQ $697.93 (+0.37%), but below SMA10/20/50 ($716.02/$719.70/$718.73) and VWAP $701.00.
- IWM $292.87 (-0.40%), below SMA10/20 and VWAP; breadth/risk appetite weak.
- SMH +0.43% but below daily SMA10/20/50 and intraday VWAP; XLF -0.43% but remains above rising SMA10/20/50. XLK +0.41% but below all key daily averages. Regime is narrow rebound with late-day fading, not a confirmed broad risk-on breakout.

## Overnight positions

### NVDA — HOLD
- Quote $203.03; value ~$24.60; unrealized ~$-0.40. Bid/ask $203.02/$203.04.
- Daily: above SMA20 $202.22, below SMA10 $204.04 and SMA50 $209.79. Intraday range $202.28–$207.74; below VWAP $205.12 on light partial-day relative volume.
- Fundamental/catalyst: PE ~31.8; six consecutive verified EPS beats; next verified earnings 2026-08-26. AI/inference demand remains supportive, while chip-sector correction and concentration risk remain material.
- Plan: hold while $199–$200 support remains intact; exit review on decisive break below $198.50. Targets $213.90 then $220. No add below cost.

### SOFI — HOLD / HIGHEST-RISK WATCH
- Quote $17.095; value ~$76.54; unrealized ~$-3.47. Bid/ask $17.09/$17.10.
- Daily: below SMA10 $18.16 and SMA20 $17.92, just above SMA50 $17.00. Intraday low $16.9705; below VWAP $17.20. Structure weakened late but did not break the $16.90/$16.47 support framework.
- Fundamental/event risk: PE ~39.3; verified Q2 earnings 2026-07-29 before market (EPS estimate $0.11). Q1 revenue growth was strong, but Tech Platform weakness and valuation elevate gap risk.
- Plan: hold only while $16.90 intraday support and $16.47 swing support hold; exit review below $16.45. Targets $18.50 and $19.70. Reassess/likely de-risk before earnings absent a technical recovery. No averaging down.

### JPM — HOLD
- Quote $338.08; value ~$65.98; unrealized ~$-0.70. Bid/ask $338.00/$338.17.
- Daily: near SMA10 $338.15 and above SMA20 $334.71/SMA50 $317.58; intraday low $337.37 and below VWAP $340.07. XLF remains in a constructive daily trend despite today's weakness.
- Fundamental/catalyst: PE ~14.7; Q2 EPS $6.14 beat $5.59 estimate, with record quarterly profit and supportive analyst follow-through. Expense guidance and higher-for-longer macro sensitivity remain risks.
- Plan: hold above $334.50–$335 support; exit review below $334. Targets $351 then $360. No add below entry.

## Candidate/rotation decision

- Broad saved scans covered 297 daily gainers and 331 upcoming-earnings names. Most top gainers were low-cap/low-liquidity and rejected.
- ACHR (+19.1%) held above VWAP and SMA10/20 but remained below SMA50 and was extended; IREN (+18.2%) remained below SMA20/50 with ~10% ATR; CIFR (+17.8%) remained below SMA20/50; CLS (+2.4%) remained below SMA10/20/50 with earnings 7/27. None offered a cleaner non-chasing 1.5:1+ swing entry than existing positions.
- Rotation was rejected: selling structurally intact holdings to chase 18%–19% countertrend gaps would raise volatility and constitute churn. No thesis had reached its written invalidation.

## Liquidity, actions, and orders

- Liquid buying power after pending/open orders: $16.67.
- Policy target if a qualifying setup existed: deploy 80% = $13.336; reserve 20% = $3.334.
- Existing equity deployment: $167.14 (90.93% of account); actual cash reserve $16.67 (9.07%).
- New cash deployed this scan: $0.00. Cash retained: $16.67.
- Order reviews, placements, cancellations: none, because no order was selected. Exact new fills/actions: none.
- Fractional protective stops were not placed; this account's positions require manual invalidation checks during scheduled scans. Stops were not widened.

## Data notes

Live account, orders, fills, quotes, OHLCV, fundamentals, earnings history/calendar and scanner results came from Robinhood MCP. Web search supplied secondary news/catalyst context. MCP calls returned usable data; benign session-termination 400 messages occurred after completed direct calls and did not compromise returned broker state.
