# Agentic 1041 Afternoon Swing/Rotation Scan — 2026-07-20

- Timestamp: 2026-07-20T17:32:59Z
- Account: Robinhood Agentic ••••1041 (433711041) only
- Mode: autonomous policy-gated equity management
- Decision: HOLD ALL; NO NEW ORDER; NO ROTATION

## Live broker and kill-switch verification

- MCP connectivity: connected; 50 tools discovered.
- Account identity: 433711041 is active cash account, nickname Agentic, `agentic_allowed=true`. No other account was traded or inspected for sizing.
- Account value: $185.1366; equity value $168.4666; cash and authoritative buying power $16.67.
- Positions: NVDA 0.121165, SOFI 4.477580, JPM 0.195159; all shares shown sellable and no held-for-sale quantities.
- Open-ish equity order states checked individually: new, queued, confirmed, unconfirmed, partially_filled — all empty.
- Today's fill verified: agentic market buy JPM for $66.68, 0.195159 shares at average $341.6699, filled 2026-07-20T13:53:25.4Z; order 6a5e2855-17cf-4546-937b-b6a129da1933. No later fill found.
- Kill switch clear: account value > $10; estimated current position P/L -$3.28 (-1.77% of account), below 5% daily-pause gate; account is 7.43% below original $200 funding proxy, below 10% proxy drawdown gate. Live broker/account/risk state was sufficiently certain.

## Market and sector regime

At ~17:32Z, SPY +0.11% but below SMA10/SMA20 and around SMA50; QQQ +0.69% but below SMA10/20/50; IWM -0.16% and below SMA10/20. This is a narrow risk-on rebound, not a confirmed broad breakout. Semiconductors led (SMH +1.21%) but remained below SMA10/20/50 after a sharp July correction. Financials lagged (XLF -0.30%) while retaining a constructive daily uptrend above SMA10/20/50. Consumer discretionary was weak (XLY -0.71%, below all three averages). Web/news checks corroborated a semiconductor rebound after recent pressure, while today’s crypto-compute leaders were catalyst-driven and very extended.

## Existing positions and plans

### NVDA — HOLD
- Quote $203.785; value ~$24.69; unrealized -$0.31 (-1.23%). Bid/ask $203.78/$203.80.
- Structure: +0.48% today, above SMA20 $202.13 but below SMA10 $204.84/SMA50 $209.91; intraday VWAP $205.65 and low $203.04. SMH relative strength supports the theme, but the stock faded below VWAP.
- Fundamentals: PE ~31.8; six consecutive verified EPS beats; next verified earnings 2026-08-26.
- Plan unchanged: hold while $199–$200 support remains intact; decisive break below $198.50 invalidates. Targets $213.90 then $220. No add below cost.

### SOFI — HOLD / CLOSE WATCH
- Quote $17.3199; value ~$77.55; unrealized -$2.46 (-3.08%). Bid/ask $17.31/$17.32.
- Structure: +0.23% today and above intraday VWAP $17.20 after testing $16.9705; below SMA10 $18.06/SMA20 $17.91 but above SMA50 $17.02. It recovered from the morning low, so immediate exit evidence did not strengthen.
- Fundamentals/catalyst: PE ~39.3; prior quarter met EPS estimate after earlier beats; verified Q2 earnings 2026-07-29 creates near-term event risk.
- Plan unchanged: hold only while $16.90 intraday support and $16.47 swing support hold; exit review below $16.45. Targets $18.50 and $19.70. No averaging down.

### JPM — HOLD
- Quote $339.06; value ~$66.17; unrealized -$0.51 (-0.76%). Bid/ask $339.00/$339.10.
- Structure: -0.60% today and below intraday VWAP $340.70, but still above SMA10 $338.81, SMA20 $335.09 and SMA50 $318.21. XLF was mildly weak intraday but daily sector trend remains constructive.
- Fundamentals: PE ~14.7, dividend yield ~1.72%; 2026-Q2 EPS $6.14 beat $5.59 estimate on 2026-07-14.
- Plan unchanged: hold above $334.50–$335 support; exit review below $334. Targets $351 then $360. No add below entry.

## Broad liquid-universe scan and ranking

Saved broad scans covered 300 daily gainers and 331 upcoming-earnings equities; low-priced/microcap and low-volume names were rejected. Ranked liquid shortlist:

1. **NVDA — 7.8/10:** strongest held combination of liquidity, semiconductor relative strength, earnings quality and clear invalidation, though below VWAP/SMA10; no add below cost.
2. **JPM — 7.5/10:** clean multi-timeframe uptrend, fresh EPS beat, reasonable valuation and clear $334 invalidation; already held.
3. **ACHR — 6.5/10:** +20.95%, 2.7x relative-volume scanner reading, above SMA10/20 and VWAP, but still below SMA50/20-day high, unprofitable (PE negative) and extended ~one full daily range from the open. Wait for a $4.95–$5.10 retest rather than chase.
4. **IREN — 6.2/10:** +20.70%, above VWAP/SMA10 with current news indicating an increased cloud-revenue forecast; however below SMA20/50, ATR ~9.6% of price, PE ~120 and two recent EPS misses. Extended/countertrend entry rejected.
5. **CLSK — 5.9/10:** +14.27%, above VWAP/SMA10/20, and operational news includes 614 June BTC produced plus a long-term data-center lease; still below SMA50 with deeply inconsistent/recently negative EPS. Crypto-beta concentration and gap risk fail clean swing entry.

CIFR (+17.48%) was rejected below SMA20/50 with negative PE and two recent EPS misses. CLS (+3.10%) has six verified EPS beats but is below SMA10/20/50 and reports 2026-07-27; earnings-gap risk and poor trend alignment prevent entry.

## Liquidity, deployment, and action

- Liquid buying power after pending/open orders: $16.67.
- Policy target if a qualifying setup existed: deploy exactly 80% = $13.336; retain 20% = $3.334.
- Existing equity deployment: $168.47, 91.00% of account; cash reserve: $16.67, 9.00% of account.
- New cash deployed this scan: $0.00. Cash retained: $16.67.
- Reason: no fresh candidate offered a non-chasing entry with clear invalidation and at least 1.5:1 reward/risk. Rotating out of recovering SOFI or structurally intact JPM/NVDA into 14%–21% countertrend gaps would increase volatility and constitute churn. The 80% liquid-balance target does not override the no-forced-trade gate.
- Order reviews/placements/cancellations: none. Exact new fills/actions: none.

## Data/source notes

Live account, quotes, OHLCV, fundamentals, earnings history, tradability and scanner results came from Robinhood MCP. Current web/news search was used only for macro/catalyst context and was treated as secondary to broker data. No tool failure compromised broker or risk certainty.
