# Autonomous MIDDAY Agentic Swing Scan — 2026-07-21

- Scan window: 2026-07-21 15:57–16:07 UTC (11:57–12:07 ET)
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`
- Asset scope: equities only; fractional long shares; no options, shorts, crypto, or other accounts
- Decision: **HOLD / NO NEW ORDER.** Preserve the required reserve and tighten management invalidations; do not churn into extended rebound leaders.

## Policy, broker state, and kill switches

- Account verified active, cash account, `agentic_allowed=true`, buying power not blocked.
- Final verified portfolio value: **$187.0097**.
- Equity value: **$183.6797**; cash and authoritative buying power: **$3.33**; pending deposits: $0.
- Equity deployment: **98.22% of total account value**; cash: **1.78%** of total value.
- The relevant deployment tranche was the $16.67 liquid balance verified earlier today. The filled $13.34 UNH order used **80.02%**, leaving $3.33 or **19.98%** as the mandated reserve. The remaining $3.33 is therefore not a fresh qualifying tranche to redeploy.
- Pending-order commitment: **$0**. Separate queries for `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled` all returned empty.
- Today's only equity order remained the agentic UNH buy: $13.34 / 0.031089 shares, filled at $429.085 at 13:52:49Z, $0 fees. No other fill appeared.
- Opening scan baseline $185.0369 to final verification $187.0097: **+$1.97 / +1.07%**, safely inside the 5% session pause gate.
- Conservative funding proxy $200 to current $187.0097: **-6.50%**, inside the 10% drawdown pause gate. Direct broker high-watermark remains unavailable, so this proxy is documented rather than presented as exact.
- Account-above-$10 gate: clear. Broker state and position inventory reconciled. No kill switch fired.

## Midday market regime and flows

Live 16:06–16:07Z tape:

- SPY $748.18, +0.82% day, above intraday VWAP and near the session high; daily structure still only partially repaired because the prior close was below the 10/20/50-day averages.
- QQQ $708.76, +1.82% day, above intraday VWAP but still below prior-session SMA10/20/50 ($711.62/$716.12/$719.01).
- IWM $295.67, +1.15% day, stronger breadth than the opening snapshot.
- XLK $180.44, +2.69%, led sector recovery; XLF $56.155, +0.21%; XLV $159.35, +0.06%.
- Regime: **risk-on intraday rebound inside an incompletely repaired technology correction**. Semiconductors and storage were rebound leaders after a severe July selloff, but many liquid leaders were already +10% to +15% at midday. Macro/event risk remains elevated around large-cap technology earnings (GOOGL and TSLA verified for July 22 after close), the July 28–29 FOMC window, and Middle East/oil volatility. This favors holding defined-risk positions and rejecting gap-chasing.

## Holdings — live reassessment and management

Values and P/L use live quotes around 16:06–16:07Z. Stops below are policy management invalidations, not resting broker orders; fractional stop orders were not represented as supported in this workflow. Stops were not widened.

| Rank | Symbol | Shares / avg | Live / value | P/L | Technical + fundamental thesis | Stop / targets | Action |
|---:|---|---|---|---:|---|---|---|
| 1 | UNH | 0.031089 / $429.09 | $432.32 / $13.44 | +$0.10 (+0.75%) | Above SMA10/20/50 and intraday VWAP; +2.56% day. Q2 revenue $112.0B, operating earnings $8.0B, cost control improved, and adjusted EPS guidance raised to $19.50–$20.00. | Stop $423 unchanged; T1 $450; T2 $461.62. | Hold. Thesis valid. |
| 2 | JPM | 0.195159 / $341.67 | $344.12 / $67.16 | +$0.48 (+0.72%) | Above SMA10/20/50, near session high, and outperforming XLF. Q2 managed revenue $58.0B and strong markets/investment-banking results support the post-earnings thesis. | **Tighten** management stop from $332–333 to $337; T1 $351.24; T2 $360. | Hold; protect today-low/near-term support. |
| 3 | NVDA | 0.121165 / $206.33 | $206.37 / $25.00 | ~$0.00 (+0.02%) | Above SMA10/20 after today's rebound, but still below SMA50 $209.82 and $213.99 resistance. AI demand/FCF story remains strong; chip sector remains high-volatility after July correction. | Stop $198 unchanged; T1 $214; T2 $220. | Hold; no add. |
| 4 | SOFI | 4.477580 / $17.87 | $17.425 / $78.02 | -$1.99 (-2.49%) | Strong intraday recovery above VWAP, but still below SMA10/20 near $17.90 and remains the weakest daily structure. Q1 top-line growth was strong, while Tech Platform revenue weakness and verified July 29 earnings create binary risk. | **Tighten** management stop from $16.47 to $16.90; T1 $18.60; T2 $19.74. | Hold for current bounce; no averaging down. Exit review on sustained loss of $16.90. |

Aggregate current-price risk to tightened stops is approximately **$5.04**, below the default $6 soft cap: NVDA ~$1.01, SOFI ~$2.35, JPM ~$1.39, UNH ~$0.29. The adjustments reduce risk without widening any stop.

## Broad liquid swing scan

- Ran the live saved daily-gainers scan across 305 names and filtered to price >= $5, market cap >= $2B, and volume >= 500k: 46 liquid large-/mid-cap candidates.
- Ran the upcoming-earnings scan across 345 names and separately checked the verified high-market-cap earnings calendar.
- Reviewed live quotes, spreads/liquidity, daily and 5-minute structure, SMA10/20/50, ATR, 20-day ranges, fundamentals/valuation, recent quarterly financials, earnings dates, and current catalysts for the strongest liquid candidates.
- Rejected the highest raw movers AEHR, CIFR, NBIS, OUST, BE, WDC, MU, COIN and peers as immediate entries because most were +10% to +26% on the day, several remained below declining daily averages, and ATRs were roughly 6%–15%. Their rebound strength was real, but entry quality and stop distance were inferior after the gap.

### Ranked fresh opportunities

1. **AAPL — 8.0/10 watch.** $328.70 around 16:04Z; above SMA10/20/50 ($320.89/$306.95/$303.43), +1.7% from the open and near the session high. Latest quarter revenue $111.2B with 26.6% net margin; valuation near 40x earnings. Resistance $334.99; preferred trigger is a confirmed breakout/retest above $335 or pullback hold $320–324, not a midday chase. Stop framework $314–315; targets $350/$365.
2. **PLTR — 7.7/10 watch.** $134.44; above SMA10/20 and slightly above SMA50, holding near its session high. Q1 revenue $1.633B and net margin 53.3%; rapid growth but ~151x P/E and August 3 earnings/event risk are substantial. Trigger above $138.90 with volume or constructive $130–132 retest; stop $124.50; targets $151/$160.
3. **PANW — 7.3/10 watch.** $342.49; daily trend strong above SMA10/20/50 and Q3 revenue grew 31% YoY to $3.0B with NGS ARR +60%, but shares reversed from $352 and valuation is rich. Support $334–342; resistance $352 then $368.80. Require a confirmed hold/reclaim, stop $329, targets $369/$390.
4. **COIN — 6.9/10 watch, no chase.** $181.20, +12.95% and at the session high on above-normal volume, but prior daily trend was below SMA50, latest two quarters were loss-making, and catalyst quality was less certain. Preferred retest $168–176; stop $158–160; targets $190/$205.
5. **MU — 6.6/10 watch, no chase.** $961.38, +11.08%, powerful intraday recovery and latest reported revenue/margins accelerated sharply, but price remained below declining SMA20/50 after a -23.7% 20-day move; ATR ~8.8%. Require consolidation/retest, not same-day gap entry.
6. **NBIS/WDC/BE — 5.8–6.3/10 watch only.** +12% to +15% rebound strength but daily returns remained roughly -35% to -40% over 20 sessions and ATRs ~10%–15%; unsuitable risk-adjusted entries for this account at midday.

Existing UNH and JPM rank above fresh candidates on current location and defined risk. NVDA remains comparable to PANW but already supplies technology exposure. SOFI is the weakest holding, yet its thesis had not invalidated and replacing it at a realized loss with a +10%–15% rebound leader would be churn rather than a materially better risk-adjusted rotation.

## Decision and execution record

- **No new order, no sale, no cancellation, and no broker review call was required because nothing was placed.**
- The $3.33 buying power is the retained 19.98% reserve from today's $16.67 qualifying liquid tranche. Re-spending 80% of that reserve recursively would violate the policy requirement not to spend the buffer merely to hit a target.
- Four positions already satisfy the 1–4 equity limit. A fifth position was not allowed; no candidate justified rotating out an unbroken thesis after considering taxes/slippage/churn and the extended market tape.
- Management change only: tighten SOFI invalidation to $16.90 and JPM to $337; NVDA $198 and UNH $423 unchanged. These are stricter, never wider.
- Final verification confirmed four long fractional equities, $3.33 cash/buying power, no pending order commitment, and no new fills after UNH.

No guaranteed-return claim. All positions remain exposed to gap risk, earnings/macro surprises, and losses beyond soft invalidations.