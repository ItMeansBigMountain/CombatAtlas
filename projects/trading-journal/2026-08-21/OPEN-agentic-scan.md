# Agentic OPEN Scan — 2026-08-21 13:36 UTC

## Decision
- Account: Robinhood Agentic ••••1041 only; autonomous equities policy ACTIVE.
- Action: HOLD MA, BAC, XOM, SHOP. NO ORDER, NO ROTATION, NO ADD at the opening scan.
- Rationale: only six minutes of price discovery had elapsed; fresh mover candidates were opening gaps or lacked verified catalyst/retest confirmation. Four-position policy maximum is already occupied and existing planned risk is above the default $6 target, so adding risk merely to spend cash is prohibited.

## Broker / kill switches
- Account active, cash, agentic_allowed=true. Account value $326.5931; equity value $312.6331; cash and authoritative buying power $13.96; unsettled funds $0.
- Open-ish equity states checked individually: new, queued, confirmed, unconfirmed, partially_filled — all empty. Pending commitment $0.
- Latest fill verified: agentic XOM buy for $55.83, 0.332975 shares at $167.6699 on 2026-08-20 17:32:05Z; fees $0.
- Kill switch: account value >$10. Approximate live position mark implied a +$0.92 move versus prior closes (+0.28% of account), so the 5% daily loss pause was not active. Value is only ~0.33% below the prior afternoon snapshot of $327.6608, so the 10% recent-high gate was not active on available journal snapshots. Broker/risk state coherent.
- Liquid balance after orders $13.96: nominal 80% deployable $11.17; required 20% reserve $2.79. No deployment because entry/risk gates bind. Existing equities are ~95.7% of account value.

## Market regime
- Mixed/rotation, constructive opening: SPY $764.71 (+0.28%), QQQ $711.98 (+0.15%), IWM $299.36 (+0.57%). SPY was above SMA20/50 (760.99/750.94); QQQ above SMA20 but below SMA50 (707.73/713.05); IWM above SMA50 but around SMA20 (296.32/298.16).
- Opening sector leadership: XLE +0.77%, XLF +0.68%, XLI +0.44%, XLV +0.35%; XLU -0.34%. Energy and healthcare have strongest 20/60-day trends: XLE +7.36%/+10.20%, XLV +6.78%/+16.08%. Macro/news context remains higher oil and inflation risk after Middle East disruption; rates/yields remain a cross-current. No major US data or earnings were scheduled for Aug. 21 in the checked market calendar.

## Position ranking and management
1. **XOM — HOLD, 14/16.** $167.56 (+0.85% day), value ~$55.79, near cost. Above SMA20/50 $157.92/$148.68; +5.90%/+10.91% 20/60-day momentum; XLE leading. Q2 EPS $3.52 missed $3.76, but higher oil and raised long-term production/cash-flow targets support the catalyst. Stop/invalidation $163.50; targets $176.50/$182; 3–5 session time stop. Do not add during opening volatility.
2. **MA — HOLD, 13/16.** $574.32, value ~$65.21, +$0.21 unrealized. Above SMA20/50 $566.21/$535.85; +8.21%/+16.40% momentum. Q2 EPS $5.04 beat $4.76. Stop $561; targets $584/$601.77. Opening bid/ask was temporarily wide, reinforcing no add.
3. **SHOP — HOLD/protect, 12/16.** $147.08, value ~$126.79, +$2.58 unrealized. Above SMA20/50 $139.15/$125.76; +31.41%/+40.31% momentum. Q2 EPS $0.42 beat $0.37, but ~99x trailing P/E and extension increase reversal risk. Stop $140; targets $158.87/$170; no add.
4. **BAC — HOLD, weakest, 10/16.** $62.32 (+0.74%), value ~$65.21, +$0.21 unrealized. Above SMA50 $60.38 but below SMA20 $63.04; 20/60-day momentum +0.95%/+18.51%. XLF opening strength and Q2 EPS $1.21 vs $1.11 support holding. Hard stop $60.70; targets $65.20/$67. Do not average down; exit if hard stop breaks or relative weakness persists.

## Broad scan / ranked fresh candidates
- Universe included all 20 Robinhood Daily Movers, narrowed by price, liquidity, spread, fundamentals, and daily charts; detailed OHLCV was computed for ten liquid/relevant names.
1. **MRVI — 11/16, WATCH/RETEST.** New 52-week high $8.48, +17.6% 20-day and +89.3% 60-day momentum, above SMA20/50, but loss-making and at resistance without a verified fresh catalyst. Require multi-session hold/retest near $8.00–8.20; speculative half-size only.
2. **MRNA — 10/16, WATCH ONLY.** +9.5% opening gap and extreme +133.8%/+183.5% 20/60-day momentum, but loss-making, ATR ~$14.55, and opening gap lacks a confirmed retest/catalyst in checked sources. Do not chase; require consolidation near $135–140 and explicit catalyst confirmation.
3. **MARA — 9/16, NO TRADE.** +8.3% opening move and highly liquid, but below SMA50 with negative 20/60-day momentum and negative earnings; crypto-linked volatility conflicts with quality guardrail.
- AAP, AMRC, ONT, CAPR, SPRY, EYPT, and BTBT rejected for broken intermediate trends, weak quality, low price, wide spreads, or unconfirmed binary/speculative catalysts.

## Orders / fills / cash
- Reviews called: none; no setup passed the confirmed-entry gate, so order review would not cure strategy failure.
- Orders placed: none. New cash deployed: $0.00. Buying power remains $13.96; policy reserve remains at least $2.79.
- Next trigger: reassess opening gaps only after a retest/volume confirmation; manage BAC first if $60.70 fails, SHOP at $140, XOM at $163.50, and MA at $561. Never widen stops.

## Tool/source notes
- Robinhood account, portfolio, positions, all five open-ish states, recent fill, quotes, fundamentals, earnings, curated movers, and OHLCV succeeded.
- Web news search was sparse for several opening movers; absence of verified catalyst was treated as a reason not to trade, not as positive evidence.
