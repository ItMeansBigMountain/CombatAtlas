# Autonomous OPEN Swing-Trading Scan — 2026-07-23

- Window: approximately 13:36–13:38 UTC (09:36–09:38 ET)
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only; no options, shorts, crypto, leverage, averaging down, or other accounts
- Decision: **EXIT SOFI; HOLD NVDA/JPM/UNH; NO NEW ENTRY.** SOFI broke the written $16.90 invalidation. New opening leaders were extended gaps, and authoritative buying power remained only $3.33 after the cash-account sale.

## Live broker state and kill switches

- Account identity was verified through `get_accounts`; only account 433711041 was operated.
- Pre-action account value $185.1878, equity $181.8578, cash $3.33, authoritative buying power $3.33, pending deposits $0.
- Initial positions: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09. All were fully sellable.
- Explicit `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled` queries were empty before action; no July 23 fill existed before this scan.
- Below-$10 kill switch clear. Account value was down about 0.93% from July 22's $186.9347 power-hour snapshot, inside the -5% daily pause. Drawdown versus the conservative $200 funding proxy was about 7.41%, inside the -10% pause. Broker does not expose a direct high-water field.

## Market regime and context

- Opening quotes: SPY $741.02 (-0.85%), QQQ $695.51 (-1.40%), IWM $292.02 (-0.60%). SPY was below SMA10/20/50; QQQ remained below all three and was weakest; IWM was below SMA10/20 but just above SMA50. Regime: risk-off/mixed.
- Sector flow: XLI +1.65%, XLE +1.59%, XLV +0.90% led. XLY -3.29%, XLC -2.39%, SMH -1.13%, XLK -0.65%, and XLF -0.65% lagged. Energy/industrials/healthcare rotation persisted while growth and consumer sectors weakened.
- Current reporting indicated elevated oil/inflation/rate risk. The prior night's large-cap reports created sharp dispersion: GOOGL opened about -5.9% and TSLA about -10.3%; these were falling gaps, not policy-valid longs.

## Position management

| Symbol | Live price | Technical state | Invalidation / targets | Action |
|---|---:|---|---|---|
| SOFI | $16.775 pre-review | Below the written $16.90 trigger, SMA10 $17.83, SMA20 $17.88, and SMA50 $17.10; weakest holding and July 29 event risk remained. | $16.90 breached; targets void | **Exited full position; no averaging down.** |
| NVDA | $209.505 | Above SMA10/20 but near SMA50 $209.68 and below $214.39 resistance; semiconductors weak. | $198; $214/$220 | Hold; no add. |
| JPM | $348.50 | Above rising SMA10/20/50, near $351.24 resistance; relative strength despite weak XLF. | $337; $351.24/$360 | Hold; no add into resistance. |
| UNH | $429.37 | Above SMA10/20/50, but below $461.62 recent high; healthcare relatively strong. | $423; $450/$461.62 | Hold. |

## SOFI order review, execution, and fill

- Thesis failure: sustained live trade below the pre-written $16.90 invalidation, deteriorating trend/relative strength, and upcoming earnings risk.
- Reviewed: sell 4.477580 SOFI, market, GFD, regular hours. Broker `order_checks` was empty.
- Required quote disclosure: **Bid $16.77 × 1600 Q · Ask $16.78 × 1200 Q · Last $16.76 × 1000 Q. Updated 9:37 AM ET.**
- Placed autonomously under active policy. Order ID `6a621912-1a9f-45bb-8ee8-7b5d32b73a1b`.
- Filled 4.477580 shares at average $16.750000 at 13:37:22 UTC; fees $0. Estimated proceeds $74.9995.
- Realized price loss versus $17.87 average cost: approximately $5.0149 (-6.27%), excluding any tax effects. Rules followed: yes; stop was not widened and no averaging down occurred.

## Broad liquid scan and ranked candidates

The Robinhood gainers scanner returned 249 names; microcaps/low-price spikes were rejected. Quotes, daily OHLCV, fundamentals/tradability, earnings records, and sector context were checked for liquid candidates beyond stale watchlists.

1. **RTX — 7.4/10 watch, no chase.** $209.25 (+7.37%), above rising SMA10/20/50 and prior $203.94 20-day high; industrial leadership supports it. Opening gap was ~1.6 ATR above the prior high. Require a retest/hold near $203.90–$205; invalidation $199; targets $214/$220.
2. **TMO — 7.2/10 watch, no chase.** $575.25 (+9.27%), strong trend and healthcare alignment, but >2 ATR above prior $544.45 20-day high. Require a $545–$555 retest/base; invalidation $535; targets $590/$610.
3. **CSX — 7.0/10 watch.** $52.84 (+5.83%), above rising SMA10/20/50 and prior $51.28 high with industrial relative strength. Prefer a $51.20–$51.60 breakout retest; invalidation $49.80; targets $54.50/$56.
4. **CLF — 6.5/10 no chase.** $11.08 (+17.25%) with liquidity and industrial/materials momentum, but still near declining SMA50 $11.25 after a multi-ATR gap. Require a multi-session base above $10.50; invalidation $9.95; targets $11.80/$12.50.
5. **IMAX — 6.3/10 watch.** $42.85 (+9.02%), above SMA10/20/50 but still below recent $45.52 resistance; opening volume/gap entry was extended. Require a $41.00–$42.00 hold; invalidation $39.80; targets $45.50/$48.

NVCR (+27.75%) was rejected as an extended biotech gap with weak opening relative-volume confirmation. GOOGL and TSLA were rejected as falling post-earnings gaps. No setup offered a clean immediate entry with explicit >=1.5:1 reward/risk at the live opening price.

## Post-action state, deployment, and blocker

- Verified final positions: NVDA, JPM, UNH only; SOFI absent.
- Verified all five open-ish order states empty; the SOFI order appears as filled.
- Post-action account value $185.1879; equity $106.8579; cash $78.33.
- Authoritative broker buying power remained **$3.33**, despite the sale proceeds appearing in cash. This is consistent with cash-account settlement restrictions, but the reason was not assumed; buying power was treated as authoritative.
- Liquid BP after pending orders: $3.33. Mechanical 80% amount $2.664; 20% reserve $0.666. No new order was reviewed or placed because the opening candidates were extended and an immaterial ~$2.66 entry would force a trade. Equity deployment after exit was 57.70% of account value; the gap from the deployment target is due to unavailable buying power plus setup quality, not discretionary reserve spending.
- Next checks: reassess whether sale proceeds become buying power; monitor SOFI only for post-exit review, NVDA $198, JPM $337, UNH $423, and candidate retests listed above.

## Tool/source record

- Broker account, portfolio, position, quote, historical, scanner, fundamentals, earnings, tradability, review, placement, and verification calls succeeded.
- Web results for same-minute July 23 news were incomplete; unverified causal headlines were not used as trade mandates. Broker data governed execution.
