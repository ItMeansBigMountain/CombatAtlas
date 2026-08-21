# Afternoon Swing Scan and XOM Execution

- Timestamp: 2026-08-20T17:32:05Z
- Account: Robinhood Agentic ••••1041 (433711041)
- Policy: autonomous-policy.md ACTIVE; equities/fractionals only
- Mode: Pre-authorized autonomous execution

## Broker and risk state
- Pre-trade account value: $327.4610
- Pre-trade equity value: $257.6710
- Pre-trade liquid buying power: $69.79
- Open-ish orders checked: new, queued, confirmed, unconfirmed, partially_filled — none before entry
- Recent fill: AVGO sell 0.095750 @ $393.5001 on 2026-08-17
- Kill switch: clear (value > $10); no unsettled funds; account active and agentic_allowed
- Daily/recent-high drawdown: no live high-water-series field was available; no broker/tool uncertainty affecting order risk calculation
- Date-specific trading plan: none found for 2026-08-20

## Regime
Mixed/rotation. Prior completed-session data: SPY above SMA20/SMA50 (+2.9% 20d), IWM above both (+2.7% 20d), but QQQ only marginally above SMA20 and below SMA50. At scan time SPY -0.56%, QQQ -0.74%, IWM -1.40%; energy was the clear positive sector (XLE +0.66%) while consumer discretionary and healthcare were weak. Macro backdrop: strong but narrow AI/energy earnings leadership, sticky inflation/rate uncertainty, and geopolitical/oil support. This favored a smaller, sector-diversifying energy entry rather than adding correlated growth exposure.

## Existing positions — decisions
- MA 0.113541 @ $572.48; live $577.845. HOLD. Score 13/16. Above rising SMA20 $564.03 and SMA50 $534.28; +7.8% 20d/+15.1% 60d; latest EPS $5.04 beat $4.76. Management invalidation: close/hold below $561; target zone $584 then $601.77.
- BAC 1.046363 @ $62.12; live $62.7201. HOLD / weakest holding. Score 11/16. Above SMA20 $63.01 only marginally and above SMA50 $60.23; +21.9% 60d, latest EPS $1.21 beat $1.11, but today/sector relative action softened. Invalidation $60.70; target $65.20 then $67. No add.
- SHOP 0.862075 @ $144.09; live $146.86. HOLD, no add. Score 13/16. +23.8% 20d/+42.3% 60d, above SMA20 $137.39/SMA50 $125.02; latest EPS $0.42 beat $0.37 and agentic-commerce growth catalyst. High valuation (PE ~98.9) and ATR ~5.2% require discipline. Invalidation $136.50; targets $158.85 then $170; time-stop review if relative strength fails.

## Ranked fresh candidates
1. XOM — 14/16: breakout/retest continuation; energy-sector relative strength, +6.7% 20d/+6.4% 60d, above SMA20 $157.46 and SMA50 $148.33, liquid, ATR ~2.3%, clear support. Q2 adjusted earnings $14.7B, operating cash flow $23.6B, FCF $17.2B; record Permian output. Risk: commodity/geopolitical reversal; Q2 EPS missed estimate ($3.52 vs $3.76 broker series).
2. MA — 13/16 but already held; strong quality/earnings and trend, no incremental concentration needed.
3. SHOP — 13/16 but already held and volatile/extended; no add above support.
4. MU — 11/16 reduced-size watch only; strong AI/HBM catalyst and +24.8% 60d, but below SMA50 and ATR ~6.8%, too volatile/extended for this cash slice.
5. VIST — 10/16 watch only; energy strength and low PE, but negative 60d relative trend and wider spread/lower liquidity.
Rejected: AVGO/META/GOOGL due to weak 20/60d structures; BAC/JPM for weaker afternoon sector action.

## XOM trade plan
- Setup: breakout-retest continuation / energy relative-strength rotation
- Entry: market during regular hours after live review
- Planned notional: exactly 80% of $69.79 liquid buying power = $55.83
- Planned cash reserve: $13.96 (20%)
- Technical stop/invalidation: $163.50; do not widen
- Target 1: $176.50
- Target 2: $182.00 only if energy relative strength persists
- Expected duration: days to several weeks
- Estimated max loss from fill: 0.332975 × ($167.6699 - $163.50) = about $1.39
- Potential profit to T1: about $2.94
- R:R to T1: about 2.11:1
- Time stop: review/exit if no follow-through within 3–5 sessions or XLE relative strength breaks
- Exit reason: breach $163.50, failed breakout, energy-sector reversal, material oil/geopolitical catalyst reversal, or superior confirmed rotation

## Review and execution
- Review: BUY XOM, regular-hours market, $55.83; no broker alerts.
- Compliance disclosure: Bid $167.61 × 100 N · Ask $167.64 × 200 Q · Last $167.625 × 100 K. Updated 1:31 PM ET.
- Order ID: 6a873a15-714d-4084-8d06-a634a4a502df
- Result: FILLED 0.332975 XOM @ $167.6699 at 2026-08-20T17:32:05.639Z; fees $0.
- Fractional stop was not submitted because the broker tool supports fractional shares only for regular-hours market orders. The $163.50 invalidation must be enforced at scheduled scans.

## Post-trade verification
- Account value: $327.56076047
- Equity value: $313.60076047
- Cash / buying power reserve: $13.96
- Positions: MA, BAC, SHOP, XOM (four equities)
- Open-ish orders rechecked across new/queued/confirmed/unconfirmed/partially_filled: none
- Deployment: $55.83 of the pre-trade $69.79 liquid balance (80.00%); reserve $13.96 (20.00%).
