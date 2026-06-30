# Post-Morning Agentic Market Scan — 2026-06-29

## Account state
- Account: Robinhood Agentic account ending 1041 / 433711041.
- Autonomous policy: ACTIVE in playbook; equities only, fractional allowed, options/shorts disabled, kill switch below $10 or uncertain broker/risk state.
- Portfolio value: $194.66; equity value: $140.92; cash/buying power: $53.74; deployment about 72.4%.
- Positions: SOFI 4.477580 shares avg $17.87; AMD 0.115059 shares avg $521.47.
- Live position marks at scan: SOFI $18.105 (+1.26% day; approx +$1.05 / +1.32% unrealized); AMD $527.04 (+1.05% day; approx +$0.64 / +1.07% unrealized).
- Options: no nonzero positions.
- Open equity orders: none found across new, queued, confirmed, unconfirmed, partially_filled.
- Recent agentic orders this week: SOFI buy $50 filled 2026-06-26; AMD buy $60 filled 2026-06-25; NVDA sell filled 2026-06-25; HOOD sell filled 2026-06-24; SOFI buy $30 filled 2026-06-24; HOOD buy $50 filled 2026-06-22.

## Market read
- SPY $738.48 (+1.30%), QQQ $716.03 (+1.35%), IWM $297.59 (-0.75%). Large-cap/tech bid is bullish, but small-cap weakness makes the tape selective rather than fully risk-on.

## Candidate scan
- Sources used: Robinhood Daily Movers list, live Robinhood quotes/tradability, recent daily historicals, web search, Gmail routed source probe.
- Gmail source probe: personal-main Gmail valid for Gmail, but no TLDR/Robinhood Snacks matches found in the last 3 days; Calendar/Drive scopes still insufficient on verify and not needed for this scan.
- Daily movers reviewed included CMCSA, CHTR, BLD, IRDM, RPAY plus current/AI exposure names SOFI, AMD, NVDA, MU.

## Top candidates / technical + catalyst notes
- IRDM: $53.03, +21.84% day; tradable/fractional. Prior close below 10/20-day averages, now gapping above recent 20-day range high area. ATR14 from recent closes about 7.8%, high volatility. Catalyst check showed trading halt/news-pending references and extended-trading strength; exact catalyst needs stronger confirmation. Setup quality: watch only after halt/news clarity and retest; current entry is extended.
- CHTR: $154.11, +15.31% day; tradable/fractional. Big gap above recent 20-day range after previously sitting below 10/20-day averages. Search surfaced possible SpaceX/mobile collaboration and insider-buy interest. Setup quality: interesting gap leader, but current entry is extended; wait for VWAP/opening-range retest.
- CMCSA: $25.48, +9.97% day; tradable/fractional. Reclaiming above 10/20-day area, strong liquidity, but recent technical context had been weak and search results were mixed. Setup quality: better only if it holds $25 and confirms sector follow-through.
- SOFI: $18.105, +1.26% day; current holding. Above 10/20-day averages; recent range support roughly $17.35-$17.88, resistance near $18.80. Setup quality: hold existing position while above $17.35/$17.00 invalidation zone; not urgent to add because existing sandbox deployment is already near target.
- AMD: $527.04, +1.05% day; current holding. Above 20-day but near/below 10-day; ATR high at roughly 6.9%. Setup quality: hold small position, no add unless it reclaims momentum cleanly or pulls back to support with risk defined.
- RPAY: $4.285, +19.69% day; tradable/fractional but under $5, lower liquidity, higher spread risk. Rejected by default screen.
- BLD: $382.08, -10.21% day; tradable/fractional but sharp breakdown, not a long setup for this policy.

## Best setup / decision
- No new trade placed.
- Best actionable idea is not an immediate entry: watch CHTR or IRDM for a post-gap retest/hold rather than chase the first spike. Existing portfolio is already about 72% deployed, inside the 70%-90% target, with SOFI and AMD green on the day.
- If retest criteria appear later: CHTR above ~$147-$150 with volume support could target $160-$165; invalidation below retest support. IRDM above ~$50-$51 after news confirmation could target $56-$58; invalidation below failed retest. These require live confirmation before any order review.

## Risk / invalidation
- Kill switch not triggered: account value $194.66 > $10.
- Broker/account state certain enough for reporting, but no clean immediate entry due to extended gap leaders and existing deployment.
- SOFI management: hold while above roughly $17.35-$17.00; review exit if it loses that zone or market breadth deteriorates.
- AMD management: hold while above recent support; review exit if it loses the $500-$505 zone or AI/semiconductor strength fades.

## Tool / system upgrades
- Add a compact scanner script that ingests Robinhood Daily Movers, fetches quotes/historicals, computes SMA10/SMA20/ATR/20-day range, and emits a ranked JSON summary to avoid manual parsing of huge historical payloads.
- Add a reliable catalyst feed for Daily Movers; web search was noisy and did not always identify the actual halt/news catalyst.
- Fix Google Workspace skill/script path assumptions in cron: `/opt/data/skills/productivity/google-workspace/scripts/google_api.py` worked; `/opt/data/HeRmEz/skills/...` did not exist.
- Consider a local runbook note for profile-scoped Gmail probes: personal-main Gmail works, but Calendar/Drive scopes are insufficient and should be reported separately, not treated as scan failure.
