# Autonomous MIDDAY Swing-Trading Scan — 2026-07-22

- Scan window: 2026-07-22 16:00–16:03 UTC (12:00–12:03 ET)
- Account: Robinhood Agentic account ending 1041 only
- Policy: `playbook/autonomous-policy.md` read and applied
- Scope: long fractional equities only; no options, shorts, crypto, leverage, averaging down, widened stops, or other accounts
- Decision: **HOLD / NO TRADE / NO ROTATION.** All four positions remain above unchanged management invalidations. The portfolio already occupies the four-position policy maximum, is 98.23% invested, and marked downside to management levels is approximately $5.90, near the default $6 aggregate-risk cap. No scanned setup was materially superior enough to justify churn.

## Live broker state and kill switches

- Broker identity verified: account `433711041` is the active cash account nicknamed Agentic, `agentic_allowed=true`, self-directed, and not deactivated. No other account was operated.
- Final 16:03 UTC portfolio: account value $187.8270; equity value $184.4970; cash and authoritative buying power $3.33; pending deposits $0.
- Positions reconciled and fully sellable: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09. No intraday quantity and no shares held for sells.
- Explicit open-ish order queries were empty in every required state: `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled`. Pending equity commitment: $0.
- Today's equity-order query was empty: no July 22 fills, cancellations, rejections, or placements. Latest fill remains the July 21 UNH $13.34 Agentic market buy, filled 0.031089 @ $429.085 with $0 fees.
- Below-$10 kill switch: clear.
- Daily drawdown proxy: $187.8270 versus prior-close proxy $188.3712 = -0.29%, inside the -5% pause.
- High-water drawdown proxy: -7.54% versus journal-observed $203.1386 high, inside the -10% pause.
- Broker/tool/risk state was sufficient for a decision. No management level was widened.

## Market, macro, and sector regime

At 16:03 UTC, SPY was $749.59 (+0.18% versus official prior close), QQQ $709.15 (+0.03%), and IWM $294.65 (-0.64%). Daily structure remains mixed: SPY is near/above SMA10/20/50, QQQ remains below SMA10/20/50 despite its intraday rebound, and IWM is below SMA10/20 but above SMA50. This is rotation rather than broad confirmation.

Semiconductors reversed sharply: SMH $591.01 (+1.19%) and NVDA $213.48 (+2.99%), but SMH remains below its SMA20/50 and NVDA is testing prior 20-day resistance near $213.99. Energy remained a leader: XLE $59.095 (+1.02%), above its prior 20-day high near $58.38. Utilities and staples were also positive earlier, while small caps lagged. Macro/event risk remains elevated around oil/Middle East developments and tonight's GOOGL/TSLA/IBM/TXN/NOW earnings; the next FOMC window is July 28–29.

## Holding reassessment

Management levels are scan-time soft exit triggers, not resting broker stop orders.

| Holding | 16:03 price | Value / P&L vs average | Technical and fundamental/catalyst thesis | Stop / targets | Action |
|---|---:|---:|---|---|---|
| NVDA | $213.48 | $25.87 / +$0.87 | Strong intraday reversal from $204.95 to near the $213.61 high; reclaimed SMA10/20/50, but is testing $213.99 20-day resistance after a volatile semiconductor selloff. Fundamentals remain exceptional: latest broker financials show quarterly revenue $81.6B and 71.46% net margin, with AI infrastructure demand the core catalyst. | $198 unchanged; $214 / $220 | Hold. No add into resistance. |
| SOFI | $17.225 | $77.13 / -$2.89 | Bounced from $16.96 and remains above $16.90 invalidation and SMA50 ~$17.04, but stays below SMA10/20 ~$17.9 and is the weakest holding. Quarterly revenue has risen to $1.10B with positive margins, but July 29 earnings are binary; financial-services growth and Tech Platform quality remain key. | $16.90 sustained loss; $18.60 / $19.74 | Hold under close watch; first exit-review candidate; never average down. |
| JPM | $348.43 | $68.00 / +$1.32 | Strong rising SMA10/20/50 structure and +0.93% day relative strength; approaching $351.24 resistance. Q2 produced record profit supported by investment banking and trading, though higher expense guidance is a risk. | $337 unchanged; $351.24 / $360 | Hold. No add below resistance. |
| UNH | $433.75 | $13.48 / +$0.14 | Above rising SMA10/20/50 after Q2 adjusted EPS beat and raised outlook; intraday consolidation $432.30–$436.32 is constructive. Risks remain reserve quality, membership contraction, and regulatory/DOJ overhang. | $423 unchanged; $450 / $461.62 | Hold. |

Quote-derived downside to management levels: NVDA $1.88, SOFI $1.46, JPM $2.23, UNH $0.33; aggregate approximately $5.90. No stop or target fired.

## Broad scan and ranked opportunities

Robinhood's live gainer scan returned 298 names. The universe was filtered for price above $5, market cap above $1B, volume above 500k, liquidity/fractional tradability, and non-chasing swing structure. Daily and 5-minute OHLCV, fundamentals, financials, earnings, and web/news context were applied to holdings and the leading shortlist.

1. **GM — 8.0/10 watch, no chase.** $82.61 around midday, +~4% versus official prior close and up sharply from the morning low; intraday range $80.04–$84.33. Q2 revenue was $48.0B, adjusted EBIT $3.9B, adjusted auto FCF $5.0B, and management raised full-year guidance. Preferred entry remains a $80.50–$81.50 retest/hold; stop $78; targets $87/$91; representative R:R from $81 is 2.0/3.33. Current price is extended above the preferred retest and does not justify selling an intact holding.
2. **JPM — 7.9/10 held continuation.** Strongest clean held trend. Fresh trigger only on a breakout/retest above $351.25; stop $342 for a fresh setup; targets $366/$375. Already held, so no add near resistance.
3. **UNH — 7.7/10 held continuation.** Earnings/guidance catalyst and improving trend. Trigger $438 after holding $430; stop $423; targets $461.62/$475. Already held.
4. **XLE — 7.4/10 breakout watch.** $59.095, above SMA10/20/50 and prior $58.38 20-day high as energy leads. Prefer a $58.50–$58.70 retest; stop $57.40; targets $61/$62; R:R about 2.1/3.0 from $58.60. Do not chase the intraday extension.
5. **T — 7.1/10 earnings-gap watch.** $22.97 after fading from $24.29; price cleared SMA10/20 but remains near SMA50 resistance around $23.07. Broker earnings data confirms a beat; valuation is low at ~7.4x trailing earnings. Require a stable $22.80–$23.05 retest; stop $22.25; targets $24.29/$25. The first-half fade weakens entry quality.

SMCI (+~25%), ARWR (+~23%), WAB (+~11%), ONDS (+~11%), DELL (+~10%), and other scanner leaders were rejected as extended, high-volatility, low-relative-volume, or lacking a sufficiently verified same-day catalyst/clean invalidation. PHM faded to ~$125 after earnings and remains below SMA20, so it did not qualify. No candidate was materially superior on risk-adjusted basis to the intact portfolio.

## Deployment, review, execution, and verification

- Liquid buying power after pending/open orders: $3.33 - $0 = $3.33.
- Mechanical 80% amount: $2.664; nominal 20% reserve: $0.666.
- Total account deployment: $184.4970 / $187.8270 = 98.23%; cash = 1.77% of account value.
- The $3.33 is the deliberately retained 20% reserve from the prior $16.67 liquid tranche, not a new tranche to recursively subdivide. Spending $2.66 would create a fifth position, leave only $0.67 cash, and add immaterial exposure while aggregate risk is near the $6 soft cap.
- Order previews: none; no action reached intended-order status.
- Real actions: none. No buy, sell, cancel, option, short, crypto, leverage, averaging down, or other-account action occurred.
- Final verification at 16:03 UTC: four positions unchanged, all five open-ish states empty, today's equity-order list empty, buying power still $3.33.

## Final decision

**Hold all four; no rotation and no new trade.** Reassess SOFI immediately on a sustained breach of $16.90; otherwise wait for a confirmed breakout/retest, a target/stop, or a genuinely superior setup that justifies rotation. No guaranteed-return claim is made.