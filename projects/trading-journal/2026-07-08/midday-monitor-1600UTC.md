# Agentic Midday Monitor / Manager — 2026-07-08 16:00 UTC

## Policy / account gate
- Policy loaded: `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`; ACTIVE; equities/fractional only; no options/shorts.
- Account operated: Robinhood Agentic `433711041` / ending 1041 only.
- Kill switch: not triggered; post-action account value $188.76 > $10.
- Broker/tool state: live portfolio, positions, open-order states, quotes, historicals, order review, placement, and post-action fill verification completed. Initial script failed with `HERMES_HOME` pointed at Google profile; reran with `HERMES_HOME=/opt/data`, which found cached Robinhood MCP token and restored tool state.

## Current state after action
- Timestamp: quotes/order state around 2026-07-08T16:01:44Z.
- Account value: $188.7592.
- Equity value: $77.0592.
- Cash: $111.70; displayed buying power remained $53.74 immediately after sell, likely settlement/broker display timing.
- Deployment: ~40.8% by equity value / account value after exiting AMD. This is below the 70%–90% target, but acceptable because the exit was risk-management driven and no clean replacement setup met policy gates in the weak midday tape.
- Open-ish equity states checked before action: new=0, queued=0, confirmed=0, unconfirmed=0, partially_filled=0.
- Post-action unconfirmed orders: 0.

## Positions after action
- SOFI: 4.477580 sh @ $17.87 avg; live ~$17.2199; value ~$77.06; unrealized P/L about -$2.91 (-3.64%). Bid/ask $17.21/$17.22. Decision: hold; no add while below near-term reclaim/support area.
- AMD: exited. Sold 0.115059 sh at average execution $503.7011 after the position broke the $506 review trigger while QQQ/SMH remained weak.

## Broad / sector regime
- SPY: $741.03 to $741.11, about -0.9% day; near/below SMA20 ~$741.29 and only marginally near SMA10 ~$740.74, so broad tape is soft rather than supportive.
- QQQ: ~$703.25, about -0.9%, below SMA10 ~$717.77 and SMA20 ~$720.43; tech remains in repair mode.
- IWM: ~$291.31, about -1.65%, below SMA10 ~$298.22 and SMA20 ~$294.35; small-cap risk appetite is weak.
- XLK: ~$178.07, below SMA10 ~$183.78 and SMA20 ~$184.75.
- XLF: ~$55.15, red today but still above SMA10/SMA20; fintech sector not enough to justify adding to SOFI while SOFI is below its own short averages.
- SMH: ~$580.87, roughly flat/red but still below SMA10 ~$617.58 and SMA20 ~$619.06; semiconductor sector bounce is not confirmed.
- XLY: ~$114.62, about -2.36%, below SMA10/SMA20; discretionary beta is weak.

## Candidate / watchlist read
- SOFI: constructive medium-term fundamentals remain, but the chart is below SMA10 ~$17.89 and slightly below SMA20 ~$17.41 after losing the $17.75-$18.00 near-term area. Hold only unless it reclaims $17.75-$18.00 with volume; review/exit if it loses ~$16.80-$17.00 with weak XLF confirmation.
- AMD: chart failed the prior $506 review trigger; price ~$503.5-$503.9, below SMA10 ~$534.10 and SMA20 ~$520.76, while QQQ/SMH remain weak. Exit was preferred over letting a tiny sandbox position drift deeper below plan.
- AVGO: +~4% and above SMA10/SMA20, but chasing a same-day semiconductor outlier while SMH is below its short averages does not provide clean R:R.
- NVDA: slightly green and liquid, but still below SMA20 and not enough to offset weak QQQ/SMH regime.
- HOOD, PLTR, HIMS, RBLX, RKLB: volatile/red or extended, no clean midday entry with controlled stop.

## Fundamental / news / cash-flow context
- Market news backdrop is risk-off: July 8 market reports cite pressure from renewed Iran/oil/geopolitical concerns and a continuation of tech/chip weakness after July 7 chip-stock declines.
- Semiconductor context remains mixed: AI infrastructure remains the secular growth narrative, but recent reports highlighted parabolic chip moves, SMH volatility, and a sharp pullback after a very strong quarter. That supports reducing AMD when its technical support failed rather than adding to a losing chip position.
- SOFI context remains fundamentally better than the current tape: recent Q1 2026 reports cite record revenue around $1.1B, GAAP net income around $166.7M, strong loan/deposit/member growth, and new product ambitions. Offsetting concerns include unchanged full-year guidance, technology-platform weakness/lost client commentary, short-seller noise, and heavy operating cash use to fund loan growth. Net: hold existing, do not add until price confirms.
- Sector/cash-flow read: money is not broadly rotating into risk at midday. XLF is relatively better than QQQ/IWM/XLK/SMH, but SOFI itself is not confirming that rotation.

## Order review and execution
- Reviewed before placement: AMD sell, market, 0.115059 shares, regular hours, GFD.
- Review checks: `{}` / no broker alerts returned.
- Required quote disclosure from review: Bid $503.50 × 600 Q · Ask $503.96 × 100 Q · Last $503.50 × 150 D. Updated 12:01 PM ET.
- Placement: submitted with ref_id `17f40341-847b-478c-8285-1089b60c219d`.
- Order ID: `6a4e745c-9c9c-472e-8119-9106ddba5268`.
- Final verified state: filled.
- Execution: sold 0.115059 AMD at average price $503.701100; fees $0.00; execution ID `6a4e745d-1ecb-4052-988b-5b19c849e2f1`; timestamp 2026-07-08T16:01:33.095Z.

## Decision / action
- Action taken: exited AMD position for risk management.
- No replacement buy placed: after the exit, deployment is under target, but broad/sector tape is weak, current SOFI position is below near-term reclaim levels, and alternate candidates did not offer a clean policy-compliant R:R >= 1.5:1 with aligned technical + news/sector context.

## Next triggers
- SOFI hold while above ~$16.80-$17.00; review/possible exit if that zone fails with weak XLF/market confirmation.
- Consider SOFI add only on reclaim/hold above ~$17.75-$18.00, then follow-through toward $18.60-$19.20, with spread tight and max planned risk clear.
- Consider fresh tech/semis only if QQQ/SMH stabilize/reclaim short moving averages; avoid chasing isolated green chip names into weak sector breadth.

## Journal
- Journal path: `/opt/data/HeRmEz/projects/trading-journal/2026-07-08/midday-monitor-1600UTC.md`.
