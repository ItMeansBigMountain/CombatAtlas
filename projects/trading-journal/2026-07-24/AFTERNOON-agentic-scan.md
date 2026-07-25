# AFTERNOON Agentic Swing / Rotation Scan — 2026-07-24

- Scan time: 17:31–17:34 UTC / 13:31–13:34 ET
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only
- Decision: **HOLD NVDA, JPM, AND SLB; TIGHTEN JPM WRITTEN INVALIDATION; NO NEW ENTRY OR ROTATION.**

## Verified live broker state / kill switches

- `get_accounts` verified account 433711041 as active cash account, nickname Agentic, `agentic_allowed=true`. No other account was operated.
- Final refresh: total value **$187.6780**, equity **$169.3880**, cash and authoritative buying power **$18.29**, pending deposits $0.
- Positions, all fully sellable: NVDA 0.121165 @ $206.33; JPM 0.195159 @ $341.67; SLB 1.443558 @ $50.67.
- Explicit open-ish order checks were empty for `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled`; therefore liquid buying power after pending orders is $18.29.
- Today's verified fill before this scan: **SLB buy 1.443558 shares @ $50.6734**, $73.15 dollar order, filled 13:41:00.854 UTC, order `6a636b6c-033b-4aed-85d2-4f3c020b40c9`.
- Kill switches clear: value >$10; versus yesterday's $184.6596 power-hour snapshot the account is up about 1.64%; versus the conservative $200 funding proxy drawdown is about 6.16%, below the 10% pause. Live broker/account/risk state was certain.

## Market / sector regime

At 17:31 UTC the tape was sharply bifurcated. SPY $741.69 was about +0.47% versus the broker previous close, while QQQ $689.72 was -0.32% and semiconductor ETF SMH $570.00 was -1.75%. Industrials XLI (+0.69%), financials XLF (+0.56%), healthcare XLV (+1.96%), energy XLE (+0.82%), and utilities XLU (+0.65%) led; growth/consumer risk was weak. The completed-bar calculations showed SPY slightly below SMA10/20/50, QQQ below all three, and SMH about 4.7% below SMA20. The Fed decision and a heavy tech-earnings week are approaching while elevated oil/geopolitical risk keeps inflation and headline risk high. This favors selective relative-strength holdings, not broad growth chasing.

## Position management

### SLB — HOLD; no add to the earnings gap

- Live $52.0601, bid/ask $52.06/$52.07; +10.25% versus prior close and about +2.74% versus the $50.6734 fill. Position value about $75.15; unrealized gain about $2.00.
- Today's range $49.755–$52.23; volume 18.16M versus 10.94M two-week average. Prior completed SMA10/20/50 $47.21/$46.82/$51.54, ATR14 $1.13, prior 20-day high $48.73. The earnings gap reclaimed the 50-day average and prior range on confirmed volume, but the live price is already roughly 4.3 ATR above the prior close and near the session high.
- Verified Q2 EPS **$0.55 vs $0.52 estimate**. Q1 revenue was $8.721B, net income $752M, margin 8.62%; valuation PE ~20.64 and dividend yield ~2.46%. Energy-sector strength and oil/geopolitical risk support the swing, while oil reversal, post-earnings gap failure, and still-lower margins versus 2025 are risks.
- **Written stop/invalidation $49.50; targets $54 / $57; expected hold days to weeks.** Planned loss from fill to stop ~$1.69; reward to targets ~$4.80/$9.13; R:R ~2.85/5.41. No averaging down and no stop widening.

### JPM — HOLD; tighten risk after target-1 breakout

- Live $352.26, bid/ask $352.21/$352.31; position value about $68.74; unrealized gain about $2.07 (+3.10%). Price broke the prior $351.24 target/resistance on relative strength, above SMA10/20/50 ($342.73/$337.99/$321.39).
- Latest verified EPS $6.14 vs $5.59 estimate; banking earnings remain constructive. Risks are a failed breakout, rate volatility, macro shock, expenses, and credit normalization.
- **Management change: raise written stop from $337 to $345** (never widened), preserving room below the breakout while protecting capital. New targets **$360 / $365**; no add into extension. Because $345 is above average cost, planned loss risk is $0 and about $0.65 of open profit is protected if executed near the level during a scheduled scan.

### NVDA — HOLD; no add against weak semiconductor flow

- Live $210.37, bid/ask $210.37/$210.38; position value about $25.49; unrealized gain about $0.49 (+1.96%). Above SMA10/20, near SMA50, but SMH and QQQ lagged and $214.39 remains resistance.
- Fundamental thesis remains exceptional AI/data-center growth and margins (latest available quarter revenue $81.615B; verified EPS $1.87 vs $1.76). Next verified earnings 2026-08-26 PM. Risks: valuation, hyperscaler capex concentration, export/geopolitical exposure, and weak sector flow.
- **Stop/invalidation $198; targets $214 / $220.** Planned risk ~$1.01. No add or stop widening.

Aggregate planned loss risk to written stops is approximately **$2.70**, below the ~$6 policy target.

## Ranked broad-universe candidates

1. **SLB 8.2/10 — best held setup, not a fresh chase.** Confirmed earnings beat, 1.66x two-week volume, energy leadership, clean $49.50 invalidation; live entry is extended.
2. **JPM 7.9/10 — breakout hold.** Strong Q2 EPS and relative strength; already owned and above the first target, so tightening risk beats adding.
3. **AAPL 7.5/10 — watch only.** $332.65, +2.1%, above rising SMA10/20/50 and within 0.7% of the 20-day high, but only 0.63 relative volume and earnings on July 31 make a new tiny position unattractive.
4. **XOM 7.3/10 — watch pullback.** Strong energy trend, $156.76 and near the 20-day high on 1.36 relative volume, but about 9.9% above SMA20 and earnings July 31; extended.
5. **RTX 7.2/10 / LMT 7.0/10 — catalyst leaders, no chase.** +9.5% and +13.0% on strong beat-and-raise/record-backlog news and >2x relative volume, but both are event gaps roughly 9%–12% above SMA20 with poor same-day entry geometry.

Rejected/avoided: weak structures in TSLA, HIMS, HOOD, RKLB, GOOGL, ORCL, and broad semiconductors; no averaging down or falling-knife rotation. The live scanner and a 50+ symbol liquid universe were narrowed through quotes/tradability before OHLCV analysis.

## Allocation / exact actions

- Liquid buying power after pending/open orders: **$18.29**.
- Exact policy target if a clean setup qualified: **$14.632 deployable (80%)** and **$3.658 reserve (20%)**.
- Existing equity deployed: **$169.388 / 90.25%** of account value; cash: $18.29 / 9.75%. Existing exposure counts separately under policy.
- **New cash deployed this scan: $0.00. Final reserve buying power: $18.29.** A $14.63 fourth position was not forced because the leaders were extended earnings/event gaps and laggards lacked valid structure. Adding to SLB at +10% on the day would chase rather than improve risk-adjusted exposure.
- Order reviews/placements/cancellations this scan: **none**. Exact fills this scan: **none**. Management action: written JPM stop raised to $345; SLB plan documented; NVDA unchanged.

## Tool/source record and failure

Robinhood MCP supplied account, portfolio, positions, fills, all five open-ish states, live quotes, tradability, broad daily OHLCV, fundamentals, earnings, financials, and live scanner results. Web news was secondary context. `get_equity_price_book` failed once because the locally inferred `symbol` parameter did not match the current schema; no order depended on that call, and live NBBO from `get_equity_quotes` was available. The failed call is journaled here. No broker order/review tool failed, and no trade was placed under uncertainty.
