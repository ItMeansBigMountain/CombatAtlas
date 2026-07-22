# Autonomous AFTERNOON Swing Opportunity & Rotation Scan — 2026-07-21

- Scan window: 2026-07-21 17:31–17:34 UTC (13:31–13:34 ET)
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only; no options, shorts, crypto, averaging down, or other accounts
- Decision: **HOLD / NO TRADE / NO ROTATION.** The remaining $3.33 is the 19.98% reserve left after this morning's exact 80% deployment of the then-available $16.67 tranche. Four-position limit is full, no thesis has invalidated, and extended rebound leaders do not justify churn.

## Broker state and kill switches

- Account verified active cash account and `agentic_allowed=true`.
- Live portfolio value $186.8843; equity value $183.5543; cash and authoritative buying power $3.33; pending deposits $0.
- Pending commitments $0: explicit `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled` queries all empty.
- Positions reconciled: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09.
- Latest fill unchanged: UNH $13.34 / 0.031089 shares @ $429.085 at 13:52:49Z, $0 fees. No later fills.
- Kill switch below $10 clear. Value versus opening baseline $185.0369 is +$1.85 (+1.00%), so 5% daily-loss pause clear. Conservative $200 funding proxy drawdown is -6.56%, below 10% pause threshold; direct broker high-watermark unavailable.
- A realized-P&L probe failed because asset class was not specified; this did not make portfolio/order/risk state uncertain because live positions, fills, prices, and cash reconciled independently. Failure journaled; no order depended on it.

## Market regime and broad scan

- Live tape: SPY $748.46 (+0.86%), QQQ $709.69 (+1.96%), IWM $295.74 (+1.17%). XLK +2.82% and SMH +4.75% led; broad risk appetite improved, but QQQ remained below prior-session SMA10/20/50 (~$711.62/$716.12/$719.01), so this is a strong rebound inside an incompletely repaired technology correction.
- Scanned 49 liquid benchmarks, sectors, mega-/large-cap and momentum equities with quotes and three-month daily OHLCV; checked SMA10/20/50, ATR14, 20-day range, relative strength, volume, spreads, fundamentals/valuation, and current web catalysts.
- Macro/catalyst context: chip shares rebounded after a multiweek correction, with major technology earnings still the next validation test for AI capex. Inflation/oil and the upcoming Fed window remain macro risks. Crypto-linked strength had a concrete catalyst—reported progress on the U.S. Clarity Act and five straight days of spot-Bitcoin ETF inflows—but same-day extension increased entry risk.

## Holdings and unchanged management levels

Live quotes around 17:33Z. Invalidation levels are management triggers, not represented as resting broker stop orders; none was widened.

| Symbol | Live / value | P/L | Technical + fundamental assessment | Stop / targets | Action |
|---|---:|---:|---|---|---|
| NVDA | $206.66 / $25.04 | +$0.04 (+0.16%) | Above SMA10/20, still below SMA50 $209.82 and resistance $213.99. AI-demand thesis remains constructive but event/sector volatility argues against adding. | $198; $214/$220 | Hold, no add. |
| SOFI | $17.345 / $77.67 | -$2.35 (-2.94%) | +1.97% rebound but still below cost and near the prior SMA10/20 area; weakest holding. Q1 growth supports the business thesis, but Tech Platform weakness and July 29 earnings risk remain. | $16.90; $18.60/$19.74 | Hold only while $16.90 survives; never average down. |
| JPM | $345.11 / $67.35 | +$0.67 (+1.01%) | Above rising SMA10/20/50 and within 1.75% of $351.24 resistance; Q2 revenue/markets strength supports thesis. | $337; $351.24/$360 | Hold. |
| UNH | $435.03 / $13.52 | +$0.18 (+1.38%) | Above SMA10/20/50 following earnings beat and raised adjusted-EPS guidance; cleanest current relative strength. | $423; $450/$461.62 | Hold. |

Estimated aggregate risk to management stops remains about $5.04, inside the default $6 soft cap.

## Ranked fresh opportunities

1. **XOM — 8.0/10 watch, no entry:** $150.69, +1.57%; above SMA10/20/50 ($143.49/$140.02/$137.93), breaking the prior 20-day high with 1.28x prior completed-session volume ratio and ~2.0% ATR. Energy/oil strength supports sector flow. Preferred entry is a $148–150 retest/hold; invalidation $144.50; targets $158/$165. At current location, no slot and no fresh deployable tranche.
2. **COIN — 7.7/10 watch, no chase:** $179.26, +11.74%, above its prior 20-day high; Clarity Act progress and reported ETF inflows support the move. However, ~5.2% ATR, ~60x P/E, incomplete SMA50 repair, and same-day extension make entry quality poor. Retest $168–176; stop $158–160; targets $190/$205.
3. **UNH — 7.6/10 existing hold:** $435.03, +3.20%, orderly trend above all key averages with ~3% ATR and earnings/guidance support. Existing exposure already captures setup; no add.
4. **JPM — 7.5/10 existing hold:** $345.11, +1.84%, rising trend and strong post-earnings fundamentals, but close to $351.24 resistance. Hold rather than add.
5. **NVDA — 7.1/10 existing hold:** $206.66, +1.66%; improving above SMA10/20, but $209.82–214 resistance and pending hyperscaler earnings make a fresh add inferior.
6. **AMD/MU — 6.2–6.7/10 watch only:** +8.1%/+12.9% rebounds with ATR around 7%–8%; volatile, extended, and not clean swing entries despite semiconductor leadership.

## Deployment and action record

- Current equity deployment: $183.55 / $186.88 = 98.22%; cash reserve $3.33 = 1.78% of account value.
- Policy tranche accounting: morning liquid buying power $16.67; $13.34 deployed to UNH = 80.02%; $3.33 retained = 19.98%. Pending orders remain $0.
- The reserve is not recursively treated as a new tranche. Nominal 80% of $3.33 would be only $2.66 and would create a fifth position, violate the intended reserve, and add immaterial exposure.
- **No order reviewed, placed, sold, or canceled. No exact fills/actions occurred during this afternoon scan.** No holding breached its tightened invalidation and no candidate offered enough improvement to justify realizing SOFI's loss or churning a valid holding.

All outcomes remain uncertain; gap risk can exceed management levels. Reassess at power hour and exit-review SOFI on sustained loss of $16.90, JPM below $337, NVDA below $198, or UNH below $423.