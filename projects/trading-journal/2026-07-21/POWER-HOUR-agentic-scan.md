# Autonomous POWER-HOUR Swing Scan — 2026-07-21

- Scan window: 2026-07-21 19:31–19:33 UTC (15:31–15:33 ET)
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only; no options, shorts, crypto, averaging down, or other accounts
- Decision: **HOLD / NO TRADE / NO ROTATION.** All four theses remain above management invalidations. The only liquid buying power is the required $3.33 reserve from this morning's $16.67 tranche, and fresh leaders are either extended or offer no material risk-adjusted improvement over valid holdings.

## Live broker state and kill switches

- Account 433711041 independently verified active, cash, and `agentic_allowed=true`; no other account was operated.
- Portfolio value $187.0557; equity value $183.7257; cash and unleveraged buying power $3.33; pending deposits $0.
- Four reconciled long equity positions: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09.
- Pending commitments $0. Explicit `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled` equity-order queries all returned empty.
- Today's sole fill remains UNH buy $13.34 / 0.031089 shares @ $429.085 at 13:52:49Z, $0 fees. No later fill appeared.
- Below-$10 kill switch clear. Versus morning baseline $185.0369, value is +$2.0188 (+1.09%), so the 5% daily-loss pause is clear. Versus the conservative $200 funding proxy, drawdown is -6.47%, below the 10% pause threshold; direct broker high-watermark is unavailable and not claimed.
- Initial collection under an isolated `uv run` returned unknown-tool errors because that process did not load the registered MCP tools. Retried with the profile's normal Python runtime; all account, order, quote, historical, fundamental, and earnings calls succeeded and reconciled. No action depended on failed data.

## Market regime, macro, events, and flows

- 19:32Z tape: SPY $748.29 (+0.84%), QQQ $708.75 (+1.82%), IWM $296.10 (+1.30%). All traded above intraday VWAP, but SPY remained just below SMA10 $749.17 and QQQ remained below SMA10/20/50 ($711.62/$716.12/$719.01).
- Sector leadership was concentrated: SMH +4.25% and XLK +2.71%, yet both remained below their prior-session SMA10/20/50 structures; XLE reached a 20-day high while XLP and XLC lagged. This is a risk-on rebound, not a fully repaired technology trend.
- Current reporting tied chip strength to bargain buying after the correction, while Alphabet/Tesla and other major technology earnings are the next AI-capex validation test. Elevated oil and renewed Middle East fighting remain inflation/macro risks; the July 28–29 Fed window is another overnight/swing risk.
- No held company reports tonight. SOFI's verified July 29 earnings remains the closest position-specific binary event; NVDA's next confirmed earnings is later in August. JPM and UNH already reported, and their post-earnings theses remain intact.

## Overnight holdings and management plan

Management levels are soft scan-time exit triggers, not represented as resting broker orders. No stop was widened.

| Symbol | 19:32Z quote / value | P/L | Technical and thesis status | Stop / targets | Overnight action |
|---|---:|---:|---|---|---|
| NVDA | $206.87 / $25.07 | +$0.07 (+0.26%) | Above VWAP and SMA10/20, but below SMA50 $209.82 and resistance $213.99. Chip rebound supports hold; major-tech earnings can create gap risk. | $198; $214/$220 | Hold; no add. |
| SOFI | $17.415 / $77.98 | -$2.04 (-2.55%) | Recovered above VWAP and SMA50, but remains below SMA10/20 near $17.90 and is the weakest holding. Growth thesis survives; Tech Platform quality and July 29 earnings are risks. | $16.90; $18.60/$19.74 | Hold only while $16.90 survives; never average down. |
| JPM | $344.12 / $67.16 | +$0.48 (+0.72%) | Above VWAP and rising SMA10/20/50; strong post-earnings revenue/markets context. Near $351.24 resistance, so no chase/add. | $337; $351.24/$360 | Hold. |
| UNH | $434.75 / $13.52 | +$0.18 (+1.32%) | Above VWAP and SMA10/20/50 after earnings beat and raised adjusted-EPS guidance; strongest held structure. | $423; $450/$461.62 | Hold. |

Aggregate marked risk to management stops is approximately $5.14 (NVDA $1.07, SOFI $2.31, JPM $1.39, UNH $0.37), within the default ~$6 soft cap. Overnight gaps can exceed these levels.

## Rotation and fresh-opportunity decision

- **XOM:** $151.16, +1.89%, above SMA10/20/50 and breaking the prior $150 20-day high as energy/oil leads. Best fresh watch, but current entry is extended above a preferable $148–150 retest. Framework: stop $144.50, targets $158/$165.
- **AAPL:** $327.85, above all major averages but below $334.99 resistance. Prefer a breakout/retest above $335 or $320–324 pullback; no slot or deployable tranche.
- **COIN:** $176.58, +10.06%, at/above the prior 20-day high but below intraday VWAP with ~5.3% ATR. Catalyst-supported strength does not justify chasing or rotating from an unbroken holding.
- **AMD/MU:** +7.3%/+11.5% with ~7%–8% ATR; powerful semiconductor rebound but too extended and volatile for clean new overnight entries.
- PLTR and PANW faded below VWAP or key short-term levels and do not offer a materially superior swap.

SOFI remains the first exit-review candidate, but it did not breach $16.90. Selling it at a loss to chase a same-day rebound leader would be churn, not evidence-based rotation.

## Deployment and exact action record

- Equity deployment: $183.7257 / $187.0557 = **98.22%**; cash reserve: $3.33 = **1.78%** of account value.
- Policy tranche accounting: morning liquid buying power $16.67; UNH fill deployed $13.34 = **80.02%**; retained cash $3.33 = **19.98%**. Pending orders are $0.
- The retained $3.33 is not recursively treated as a new tranche. Spending nominally 80% ($2.66) would violate the intended buffer, create a fifth position, and add immaterial exposure.
- **No order was reviewed, placed, sold, or canceled during power hour. No fill occurred during this scan.** No valid stop/invalidation fired, and no candidate justified rotation after event risk, entry extension, and churn were considered.

Next management triggers: sustained SOFI loss of $16.90, JPM below $337, NVDA below $198, or UNH below $423. Reassess after the close/next scheduled scan; no outcome is guaranteed.