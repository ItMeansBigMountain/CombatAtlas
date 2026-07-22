# Agentic OPEN Scan — No Trade

- Timestamp: 2026-07-21 13:36–13:44 UTC (09:36–09:44 ET)
- Account: Robinhood Agentic ••••1041 only (full broker account 433711041 used in MCP calls)
- Mode: autonomous, policy-gated equities-only swing operation

## Live account / kill switches

- Broker account verified active, cash type, `agentic_allowed=true`.
- Account value: $185.0369; equity value: $168.3669; cash and buying power: $16.67.
- Prior recorded 2026-07-20 midday value: $185.1004; current change about -$0.0635 (-0.03%), well inside the 5% daily pause gate.
- Conservative $200 funding proxy drawdown: about 7.48%, inside the 10% drawdown pause gate; direct high-watermark data remains unavailable.
- Below-$10 kill switch: clear.
- Open-ish equity states checked separately: new, queued, confirmed, unconfirmed, partially_filled — all empty. Pending-order commitment: $0.
- Recent fill verified: JPM buy, $66.68 / 0.195159 shares, average $341.6699, filled 2026-07-20 13:53:25Z by agentic placement.
- Initial broad historical request failed because the MCP limit is 10 symbols; retried in five batches of up to 10 and succeeded. Failure and recovery journaled here.

## Positions at opening quote snapshot

| Symbol | Shares | Avg cost | Live | Value | P/L | Plan |
|---|---:|---:|---:|---:|---:|---|
| NVDA | 0.121165 | $206.33 | $206.76 | $25.05 | +0.21% | Hold; support/invalidation $199 then $189.80; target $214 then $225. |
| SOFI | 4.477580 | $17.87 | $17.205 | $77.04 | -3.72% | Hold, no average-down; invalidate on decisive close below ~$16.40 / fundamental reassessment into July 29 earnings; target $18.50 then $20. |
| JPM | 0.195159 | $341.67 | $339.21 | $66.20 | -0.72% | Hold post-earnings; invalidate below $325; target $351 then $360. |

Estimated open-position risk to written invalidations is approximately $5.5–$6.0, already at the policy's default aggregate planned-risk ceiling. No stop was widened.

## Market regime

Opening tape was risk-on but gap-prone: SPY $745.80 (+0.50%), QQQ $706.20 (+1.46%), IWM $294.15 (+0.63%). Leadership was concentrated in technology/semiconductors: XLK +2.28% and SMH +3.66%, while XLF and XLV were modestly negative. This favors growth momentum, but the first minutes after a large gap are poor locations for blind swing entries.

Macro/fundamental context: inflation remains above the Fed's 2% objective and the July Fed report cited supply/energy pressure. Q2 earnings are the near-term index catalyst; Alphabet and Tesla are due Wednesday. JPM recently reported record Q2 profit and strong markets revenue, supporting the existing bank thesis. SOFI reports July 29; Q1 growth was strong but Tech Platform weakness and binary earnings risk argue against adding. Crypto was weak on July 20 despite stronger equity futures, reducing confidence in chasing COIN's opening spike.

## Broad liquid scan and rankings

Universe: SPY/QQQ/IWM, 9 sector/industry ETFs and 38 liquid mega-/large-cap equities beyond watchlists. Quotes, spreads, 50-session daily OHLCV, SMA10/20/50, ATR14, 20-day range, liquidity and available fundamentals were checked.

1. **PANW — 8.2/10:** $350.94; above SMA10 $342.04, SMA20 $330.55 and SMA50 $287.18; ATR 5.33%; 20-day high $368.80. Strong cybersecurity/AI demand and analyst upgrades, but opening entry was extended. Balanced trigger: hold/retest $342–346; stop $329; targets $369/$390; expected R:R about 1.6–2.7 depending fill.
2. **PLTR — 7.6/10:** $134.27; above SMA10 $132.16 and SMA20 $125.57, near 20-day high $138.90; ATR 5.27%. Trigger only above $139 with volume or constructive $130–132 retest; stop $124.50; targets $151/$160. Valuation and event risk remain high.
3. **COIN — 7.2/10:** $174.78, +8.94%, near 20-day high $176.48; ATR 5.33%. Strong price momentum but below-quality catalyst confirmation and crypto divergence made the opening gap chase unacceptable. Trigger: retest/hold $166–169 or breakout/retest above $176.50; stop $158; targets $190/$205.
4. **AAPL — 7.0/10:** $324.25; above SMA10/20/50 with ATR 2.58%, but below $334.99 resistance and down on the opening tape. Trigger above $335 or pullback to $315–320; stop $306; target $350/$365.
5. **NVDA — 6.8/10:** constructive rebound above SMA10/20 but still below SMA50 $209.82 and $213.99 resistance. Existing small position already captures the setup; no add.

## Liquidity deployment decision

- Available liquid buying power after pending orders: $16.67.
- Exact 80% deployment target: $13.336; required 20% reserve: $3.334.
- **Action: no trade, no preview, no placement, no cancellation.** Existing equities already represent 90.99% of account value and aggregate planned risk is near the default $6 ceiling. The best fresh candidates were opening-gap entries without a confirmed retest; spending $13.34 would add correlated risk for less than professional-quality location.
- Reassess at midday after opening ranges form. PANW is the preferred conditional candidate if it retests support and total risk can be reduced or remains calculably within policy.

No guaranteed-return claim. Equities only; no options or shorts used.
