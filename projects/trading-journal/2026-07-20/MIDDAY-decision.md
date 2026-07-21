# Agentic 1041 Midday Decision — 2026-07-20

- Timestamp: 2026-07-20T16:03:51Z
- Account: Robinhood Agentic ••••1041 (433711041)
- Mode: autonomous policy-gated equity management
- Decision: HOLD ALL; NO NEW ORDER

## Live account and risk gates

- Account value: $185.1004
- Equity value: $168.4304 (90.99% of account)
- Cash / broker buying power: $16.67
- Open-ish equity orders checked: new, queued, confirmed, unconfirmed, partially_filled — all empty
- Today's fill: bought $66.68 JPM, 0.195159 shares at $341.6699 at 13:53:25Z; agentic placement
- Kill switch: clear (account value > $10)
- Estimated current-day position P/L versus costs: about -$3.34 (-1.8% of account), below 5% daily pause threshold. Portfolio high-watermark data was not directly provided; account remains ~7.45% below original ~$200 funding, below the 10% recent-high pause threshold if $200 is used as conservative proxy.
- Broker connectivity/account identity/risk math: verified and certain.

## Holdings

### NVDA — HOLD
- Quantity 0.121165; average $206.33; midday quote $205.90; value ~$24.95; unrealized ~$-0.05 (-0.21%).
- Daily: prior close $202.81; SMA10 $204.84, SMA20 $202.12, SMA50 $209.91; ATR14 $7.35; RSI14 ~58.9; 20-day range $189.80–$213.99.
- Intraday: $204.58–$207.74, VWAP ~$206.04; price near VWAP and +1.52% vs prior close. SMH +1.73% and QQQ +0.97% confirm semiconductor/tech relative strength.
- Fundamental/catalyst: PE ~31.8; six consecutive reported EPS beats in broker earnings history; next verified earnings 2026-08-26. Recent news flow remains supportive of AI-inference opportunity, but retail flow reports show some chip/NVDA outflows.
- Plan: hold while above $199–$200 support; review/exit on decisive break below $198.50. Targets $213.90 then $220. No add below cost (no averaging down).

### SOFI — HOLD / WATCH CLOSELY
- Quantity 4.477580; average $17.87; midday quote $17.205; value ~$77.04; unrealized ~$-2.98 (-3.72%).
- Daily: prior close $17.28; below SMA10 $18.06 and SMA20 $17.91 but above SMA50 $17.02; ATR14 $0.94; RSI14 ~44.9; 20-day low $16.47.
- Intraday: low $16.9705, VWAP ~$17.14, price recovered above VWAP but remains -0.43% vs prior close. Finance ETF XLF is flat, so SOFI is modestly lagging sector.
- Fundamental/catalyst: PE ~39.3; prior quarter met EPS estimate after a sequence of beats; verified earnings 2026-07-29 creates event risk.
- Plan: hold only while $16.90 intraday support/$16.47 swing support holds. Exit review below $16.45; targets $18.50 and $19.70. No averaging down.

### JPM — HOLD
- Quantity 0.195159; average/fill $341.67; midday quote $340.055; value ~$66.36; unrealized ~$-0.32 (-0.47%).
- Daily: prior close $341.10; above SMA10 $338.81, SMA20 $335.09, SMA50 $318.21; RSI14 ~62.3; 20-day high $351.24.
- Intraday: $338.85–$344.26, VWAP ~$340.95; price slightly below VWAP and -0.31% vs prior close. XLF flat after strong recent trend.
- Fundamental/catalyst: PE ~14.7, dividend yield ~1.72%; 2026-Q2 EPS $6.14 beat $5.59 estimate on 2026-07-14.
- Plan: hold while above $334.50–$335 support; review/exit below $334. Targets $351 then $360. No add below entry.

## Broad scan and ranked opportunities

Daily-gainer and upcoming-earnings scans were run beyond watchlists. Liquid shortlist ranking:

1. NVDA (8.0/10) — best combination of liquidity, semiconductor relative strength, earnings quality and clear $199–$200 invalidation; already held and cannot add below cost.
2. JPM (7.6/10) — strong multi-timeframe uptrend and fresh EPS beat; already held, current entry near support, no add below cost.
3. CLS (6.7/10) — +2.95% midday and above VWAP, profitable with repeated EPS beats, but below falling SMA10/20/50 and earnings due 7/27; not clean enough.
4. ACHR (6.1/10) — +19% reversal on 1.75x relative volume, but still below daily SMA10/20/50, unprofitable, and extended from the open; wait for retest rather than chase.
5. IREN (5.8/10) — +18% high-volume bounce, but RSI was oversold and price remains below all key moving averages; high valuation and recent EPS misses make the gap poor swing R:R at midday.

CIFR/CLSK/HUT were rejected: large countertrend crypto-compute bounces, negative/volatile earnings, and extended intraday entries. AMKR was rejected ahead of 7/27 earnings while below key moving averages.

## Liquidity deployment decision

- Liquid buying power after pending orders: $16.67 (no pending orders).
- Policy target if a qualifying fourth setup existed: deploy exactly 80% = $13.336; reserve 20% = $3.334.
- Action: no deployment because no new setup cleared the minimum 1.5:1 R:R and clean-invalidation gate without chasing a large countertrend gap. Existing exposure is already 90.99% of account value, with 9.01% cash.
- No review/place/cancel calls made. This is an intentional no-trade under the policy's “never force trades” and no-averaging-down rules.

## Data/tool notes

- Robinhood MCP connected and account/broker state verified.
- Historical calls initially exceeded the 10-symbol limit, then were retried successfully in two batches.
- `get_financials` rejected the supplied parameter shape; broker fundamentals and earnings-result tools were used instead. This did not make account/risk state uncertain.
