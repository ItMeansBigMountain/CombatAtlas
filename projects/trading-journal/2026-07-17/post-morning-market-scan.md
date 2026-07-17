# Post-Morning Agentic Portfolio Market Scan — 2026-07-17

Timestamp: 2026-07-17 ~13:53 UTC
Account: Robinhood Agentic 433711041 / ending 1041
Mode: Autonomous policy ACTIVE; equities only. Live account, positions, orders, quotes, and risk state verified.
Decision: NO NEW TRADE. Preserve cash and manage the two holdings while the broad tape is risk-off and both positions test written invalidation zones.

## Account / broker state

- Total value: $182.84; equity value: $99.49; cash/buying power: $83.35; deployment: 54.41%.
- NVDA: 0.121165 shares, live $199.56, value ~$24.18, average $206.33, unrealized -$0.82 (-3.28%).
- SOFI: 4.477580 shares, live $16.845, value ~$75.42, average $17.87, unrealized -$4.59 (-5.74%).
- Options positions: none.
- Open equity orders: none across new, queued, confirmed, unconfirmed, and partially_filled states.
- Recent order: AVGO position was sold July 16 at $376.01; no AVGO position remains. No review or order occurred in this scan.
- Account is above the $10 kill switch. Deployment is below the 70%–90% preference, but the target is conditional on clean setups and supportive live risk state.

## Gmail / source checks

- The personal-main Workspace token failed live verification with `invalid_grant` (expired/revoked), so routed TLDR and Robinhood Snacks source signals were unavailable.
- Web/news and live Robinhood data were used instead. No Gmail modifications were attempted.

## Broad market

- SPY $743.12 (-1.01%): below SMA10 $750.24 and slightly below SMA20/50 (~$744.90/$743.99); support is near the 20-day low $716.58.
- QQQ $689.54 (-2.32%): below SMA10/20/50 ($716.02/$719.70/$718.73) and below the prior 20-day low $700.91; clear technology risk-off breakdown.
- IWM $294.71 (-0.30%): below SMA10/20 ($295.87/$296.59) but above SMA50 $290.07; relatively stronger than Nasdaq.
- Regime: bearish/risk-off, led by technology and semiconductor weakness; small caps are less weak but not confirming a broad risk-on tape.

## Position management

- NVDA $199.56 (-3.78%): below SMA10 $204.04, SMA20 $202.22, and SMA50 $209.79; ATR14 ~$7.00. It has breached the prior $201–$202 reassessment zone intraday. Do not add. Require a reclaim of $201–$202 to stabilize; sustained trade/close below ~$198 raises exit priority, with $189.80 as next major support.
- SOFI $16.845 (-2.74%): below SMA10 $18.16, SMA20 $17.92, and SMA50 $17.00; ATR14 ~$0.94. Intraday low $16.47 breached the $16.70 written thesis zone before rebounding. Do not average down. Reclaim $17.00 is needed; sustained trade below $16.70 or another loss of $16.47 requires exit review.

## Broader candidate scan

- UNH — $429.85 (+1.53% at second live pull; earlier $430.91/+1.78%), above SMA10/20/50 (~$424.96/$418.86/$401.64), ATR14 ~$12.64. Q2 EPS reportedly beat consensus ($6.38 vs $4.94), supporting healthcare relative strength. Best structure is a controlled retest, but today’s $425.30–$437.47 range is still volatile after the prior earnings gap. Score 7/10. Disconfirm on a failed-gap close below ~$423–$425.
- MAN — $54.82 (+6.14%), new 52-week high $54.98, volume ~389k versus ~1.65M 30-day average at the early scan. Earnings/mover interest and labor-cycle sensitivity matter, but the bid/ask spread was ~$0.45 (~0.82%) and the initial move was extended. Score 5.5/10; avoid chasing. Disconfirm below the opening area ~$53.1–$53.5.
- ABT — $101.45 (+2.65%), early high $102.13, liquid (~3.12M shares versus ~14.7M 30-day average). Reported Q2 EPS beat ($1.31 vs $1.28), and defensive healthcare rotation helps. Score 6.5/10; watch a hold above $100 and breakout confirmation over $102.13. Disconfirm below ~$98.8–$100.
- NET — $275.51 (+1.12%), above SMA10/20/50 (~$267.32/$249.51/$236.09), ATR14 ~$13.99, 20-day high $291. Strong cloud/security trend and relative strength, but valuation is extreme (Robinhood PE negative; PB ~63) and spread at the live pull was relatively wide. Score 6/10; only consider $267–$270 support hold or a confirmed $291 breakout. Disconfirm below ~$249.
- NFLX / ISRG — rejected. NFLX $66.02 (-11.20%) after Q2 revenue reportedly missed expectations despite a small EPS beat; ISRG $365.68 (-9.11%) at a fresh 52-week low. Both are falling-knife earnings reactions without clean long invalidation.
- JBHT — $295.60 (-0.94%) despite reported EPS beat; near highs but not showing post-earnings confirmation today. Watch only, not an entry.

## Best setup

- Best paper setup: UNH earnings-retest continuation, long equity only — not active now.
- Trigger: hold $425–$430, then reclaim $437.50 with improving market/healthcare relative strength.
- Illustrative stop/invalidation: below $423 on a confirmed entry.
- Targets: $450 first, then $461.60 prior high.
- Expected duration: several days to two weeks. A live entry must preserve at least 1.5:1 R:R and about $2 maximum planned risk.
- No order review or placement: market regime is bearish, current holdings already need risk management, and no candidate offers a clean immediate entry with confirmation.

## Risk / invalidation

- Priority is existing-position risk, not raising deployment during a QQQ breakdown.
- NVDA: no add; reassess on sustained trade below ~$198 or reclaim of $201–$202.
- SOFI: no add; sustained loss of $16.70 / repeat break of $16.47 requires exit review; $17 reclaim is the first repair signal.
- Do not widen levels or average down. No options and no non-Agentic account activity.

## Tool / system upgrades

- Repair profile-scoped Google OAuth for personal-main so routed TLDR and Robinhood Snacks signals are available.
- Promote the compact direct-MCP collector into a maintained scanner using the newly available Robinhood tools: saved scans/daily movers, earnings calendar/results, technical indicators, financials, and price-book spread.
- Fix the candidate collector’s historical-response normalizer: this run returned a list shape different from the older dictionary shape, leaving second-batch moving averages unavailable; existing live quote/fundamental data and previously computed candidate history were used.
- Add persistent position-plan state and automatic alerts for intraday breach/reclaim of written invalidation zones.

## Final decision

No new trade. Hold/manage NVDA and SOFI for now, with exit review prioritized if their breached/retested levels fail to recover. No order review, placement, cancellation, or options activity occurred.
