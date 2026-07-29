# Robinhood Agentic OPEN Swing Scan — 2026-07-28

Timestamp: 2026-07-28 13:36–13:40 UTC / 09:36–09:40 ET
Account: Robinhood Agentic 433711041 / ending 1041 only
Mode: autonomous policy ACTIVE; long fractional equities only
Decision: HOLD JPM and SLB; NO NEW TRADE, EXIT, ORDER REVIEW, OR CANCELLATION.

## Live broker state and kill switches

- Account verified active, cash, individual, `agentic_allowed=true`.
- Final portfolio: $185.72 total, $143.43 equity, $42.29 cash and buying power. No pending deposits or non-equity exposure.
- Positions: JPM 0.195159 shares at $341.67 average; SLB 1.443558 shares at $50.67 average. All shares available to sell.
- All open-ish order states were checked independently: `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled`; all returned zero. Pending-order notional is $0.
- No orders or fills today. Latest prior fill remains the 2026-07-27 NVDA exit: 0.121165 shares sold at $198.0666.
- Kill switches clear: account value is above $10; decline from the conservative $200 funding/high-water proxy is 7.14%, below the 10% pause; change from the prior power-hour $186.1075 snapshot is -0.21%, below the 5% daily pause. Live broker, quote, position, and risk state were available.

## Market regime

- Final live: SPY $737.76 (-0.18%), QQQ $672.45 (-1.42%), IWM $292.11 (-0.27%). QQQ opened below its prior 20-day low and remained far below SMA10/20/50 ($700.74/$710.49/$717.64): technology/AI risk-off regime.
- Sector flow at the opening scan: XLV +2.21%, XLP +2.93%, XLC +1.47%, XLY +0.87%, XLF +0.38%; XLK -2.41% and SMH -3.80%. Capital rotated toward defensive healthcare/staples and away from chips/technology.
- Current reporting attributes the global technology rout to renewed concern over AI capital/funding intensity and Chinese semiconductor competition. The Fed decision is due July 29, with reporting indicating a non-trivial chance of a hike/tightening bias. This materially raises gap and duration risk.
- Oil had dropped sharply after a pause in US-Iran strikes; XLE was approximately flat at the scan. This is a headwind to SLB even though the position retains post-earnings relative strength.
- Mega-cap earnings concentration is high this week (MSFT/META, then AAPL/AMZN), so opening-gap tech entries were rejected.

## Position management

### JPM — HOLD

- Live $355.39; market value $69.36; unrealized +$2.68 (+4.02%).
- Technical: above rising SMA10/20/50 ($346.57/$340.25/$323.48), with a new 52-week high of $359.25 this morning and XLF still positive. Opening fade from $359.25 and light early volume argue against adding.
- Fundamental context remains constructive after strong banking/trading results and moderate ~14.7x trailing P/E, but Fed repricing is near-term event risk.
- Binding reassessment/exit level: $346. Do not widen. Marked risk: $1.83.
- Targets: $365 / $375. Marked rewards: $1.88 / $3.83. Hold; no chase.

### SLB — HOLD, close monitoring

- Live $51.33; market value $74.10; unrealized +$0.95 (+1.30%).
- Technical: above SMA10/20 and near SMA50 ($48.10/$47.30/$51.40); $53.20 is nearby resistance. The opening low was $51.195 and the position remains above its thesis floor.
- Fundamental context: Q2 beat and management's stronger second-half free-cash-flow outlook support the thesis; Q1 revenue/net income were weaker sequentially, and lower oil/geopolitical premium is the principal risk.
- Binding reassessment/exit level: $50.00. Do not widen or average down. Marked risk: $1.92.
- Targets: $54.80 / $57.00. Marked rewards: $5.01 / $8.18. Hold.

Aggregate marked open risk is $3.75, within the ~$6 soft target.

## Broad scan and ranked candidates

The scan covered benchmarks/sectors, mega-cap and sector leaders, current earnings, Robinhood Daily Movers, and liquid earnings names beyond stale watchlists. Daily Movers was dominated by ADRs, low-quality, or high-volatility names and was not treated as a mandate.

1. **VZ — 7.8/10, defensive post-earnings breakout; WAIT FOR RETEST.** Live $48.52 (+2.54%), above SMA10/20/50 ($44.19/$43.35/$45.46) and above prior $47.55 resistance; telecom/defensive flow aligns. Approximate trigger $47.55–$47.90 retest hold, stop $46.50, targets $50.50/$51.70. Current gap is extended, so no chase.
2. **INCY — 7.6/10, earnings breakout; WAIT.** Live $120.87 (+1.68%), after touching a 52-week high of $122.98. Q2 revenue reportedly grew 38% and guidance rose, but part of growth reflected a one-time CMS benefit. Trigger: hold $118.5–$119.5 then reclaim $122.50; stop $115.50; targets $128/$133. Opening spread and failure from the high make immediate R:R inferior.
3. **JPM — 7.5/10, existing breakout leader; HOLD, NO ADD.** Trigger for a future add would be a $352–$354 retest hold and reclaim of $359.25; stop $346; targets $365/$375. Existing position already captures the setup.
4. **ITRI — 7.2/10, earnings gap; WAIT FOR CALL/RETEST.** Live $100.92 (+19.03%), 52-week high $102.20, with early volume already ~67% of average daily volume. The earnings call was scheduled for 10:00 ET and the gap is too extended. Trigger only after guidance confirmation and a $94–$96 retest hold; stop $91; targets $105/$112.
5. **DINO — 6.9/10, refining relative strength; WAIT.** Live $91.50 (+0.79%), strong trend above SMA10/20/50 ($88.36/$81.67/$74.23), but near $94.22 resistance and exposed to volatile oil/geopolitics. Trigger $88.5–$90 retest hold or confirmed close above $94.25; stop $86.5; targets $99/$104.

Rejected: GLW (-16%) and UPS (-6.5%) were earnings breakdowns; CNC (-6%) missed the technical test despite an EPS beat; GOOGL remained below SMA10/20/50; semiconductors were in an active breakdown. SHW/PII rose on earnings but were opening-gap extensions without a confirmed retest.

## Allocation and actions

- Equity exposure: $143.43 / 77.23% of account value.
- Cash: $42.29 / 22.77%.
- Liquid buying power after pending orders: $42.29.
- Mechanical liquid-balance target: deploy $33.832 (80%), reserve $8.458 (20%).
- Actual new deployment: $0; full $42.29 retained.
- Rationale: whole-account allocation is already close to 80/20, the QQQ/semiconductor breakdown and imminent Fed/mega-cap catalysts raise regime risk, and all best unowned candidates were opening gaps without policy-quality retests. Forcing $33.83 into an extended gap would violate the no-force/no-churn gate.
- No order review was performed because no immediate setup qualified. No order was placed, cancelled, or sold; no fill occurred.

## Tool/action record

- Robinhood MCP returned required account, portfolio, positions, order/fill history, all five open-ish states, live quotes, daily/intraday OHLCV, fundamentals, financials, tradability, earnings calendar, and Daily Movers.
- One non-critical price-book batch failed because 8 symbols exceeded the 4-symbol tool maximum. Quotes already supplied live bid/ask and spreads; no order was contemplated. The failure is journaled.
- MCP session shutdown repeatedly returned HTTP 400 after successful responses; this did not prevent retrieval, and final broker state was refreshed successfully. No broker uncertainty remained for the no-action decision.
