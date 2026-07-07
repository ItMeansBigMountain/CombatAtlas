# Agentic Midday Trade Monitor — 2026-07-07 16:00 UTC

## Account / policy
- Account monitored: Robinhood Agentic 433711041 / ending 1041 only.
- Policy loaded: `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`; status ACTIVE; equities/fractional only; no options/shorts.
- Kill switch: not triggered; account value is above $10.
- Broker/tool state: Robinhood MCP account/portfolio/positions/orders/quotes/historicals calls succeeded.

## Live account state
- Total account value: $193.7744
- Equity value: $140.0344
- Cash / buying power: $53.74
- Deployment: ~72.27% in equities, ~27.73% cash; within 70%–90% target band.
- Open-equity-order states checked: new=0, queued=0, confirmed=0, unconfirmed=0, partially_filled=0.
- Recent equity orders since 2026-06-25: 3 returned.

## Positions
- SOFI: 4.477580 sh @ $17.87 avg; quote $18.005; value ~$80.62; unrealized P/L +$0.60 (+0.76%).
  - Technical read: still above SMA10 ~$17.83 and SMA20 ~$17.33, but faded to the $18.00 support area after morning strength; 20-day high ~$18.61, 20-day low ~$15.87. Invalidation/review remains loss of ~$17.75-$18.00 support.
  - Decision: hold; no add while price is testing support rather than reclaiming $18.75-$19.20.
- AMD: 0.115059 sh @ $521.47 avg; quote $516.075; value ~$59.38; unrealized P/L -$0.62 (-1.03%).
  - Technical read: below SMA10 ~$537.65 and near/below SMA20 ~$518.28; day move -6.52%; 20-day support zone remains roughly $506-$510 / broader 20-day low ~$452.40.
  - Decision: hold only; do not add into semiconductor weakness. Review/possible exit if AMD loses ~$506-$509 while QQQ/SMH remain weak.

## Broad / sector regime
- SPY: $747.39, -0.52%, still above SMA10/SMA20 near ~$740 but off highs.
- QQQ: $709.385, -1.86%, below SMA10/SMA20 near ~$720; tech pressure persists.
- IWM: $296.78, -0.71%, holding above SMA20 but below SMA10.
- XLK: $179.185, -2.39%, below SMA10/SMA20; technology is weak.
- XLF: $56.185, +0.08%, near/above 20-day high; financials/fintech still relatively better.
- SMH: $577.58, -4.42%, well below SMA10/SMA20; semiconductors are the main risk pocket.
- XLY: $117.40, -0.52%, near upper part of its 20-day range but not leading today.

## Candidate / watchlist technical read
- HOOD: $114.88, -2.27%; extended above SMA10/SMA20 but pulling back from 20-day high. No clean entry; wait for a controlled retest.
- NVDA: $194.745, -0.41%; below SMA10/SMA20, sector flow weak. No new long.
- AVGO: $368.46, -1.45%; below SMA10/SMA20. No new long.
- PLTR: $135.41, +2.17%; strong relative strength and near 20-day high, but extended versus SMA10/SMA20 and broad tech is weak. R:R from current price is not clean for the sandbox.
- SMCI: $26.035, -4.25%; broken below SMA10/SMA20 and below listed 20-day low in the data set. Avoid.
- HIMS: $37.24, -2.72%; trend remains above SMA10/SMA20 but pulling back near highs; no clear stop/target entry here.
- RBLX: $56.81, -0.39%; constructive trend but near 20-day high; no fresh entry due to extension.
- RKLB: $83.77, -10.01%; high volatility / weak tape, avoid.

## Fundamental / news / sector context
- SOFI: recent earnings/guidance context remains constructive: sources cite >$1B quarterly revenue, strong adjusted EBITDA/margins, continued member/product growth, and 2026 adjusted-revenue growth guidance around 30%. XLF is the relative sector leader today, supporting the decision to hold rather than cut solely on intraday weakness.
- AMD / semis: AMD retains an AI/data-center catalyst narrative around July events/customer-win speculation, but today’s sector tape is unfavorable. Market/news context indicates chip stocks gave back early-week gains and AI/semi names are being questioned after a sharp run; SMH -4.42% confirms cash is rotating away from semis intraday.
- PLTR / AI software: news context remains supportive around AI demand, contract/guidance narratives, and analyst interest, but the stock is extended near a 20-day high while QQQ/XLK are weak. No chase.
- Broad cash-flow read: money is relatively more supportive of financials/fintech (XLF flat/positive near highs) than technology/semiconductors (QQQ, XLK, SMH red and below short averages).

## Decision / action
- Action taken: no order preview and no order placement.
- Reason: existing deployment is already within the target band at ~72.27%; no position has breached the planned risk/invalidation zone; SOFI remains supported by better sector/fundamental context; AMD is weak but not yet through the $506-$509 review zone; new candidates either conflict with sector flow or are extended with poor R:R from current quotes.
- Policy gate result: no new/add/exit candidate reached clean technical + fundamental/news + sector alignment with R:R >= 1.5:1, so no `review_equity_order` call was warranted.

## Next management triggers
- SOFI: consider add only on reclaim/hold above ~$18.75-$19.20 with market confirmation, or review trim/exit if it loses ~$17.75-$18.00.
- AMD: review exit if price loses ~$506-$509 while QQQ/SMH stay weak; do not add until AMD reclaims short averages or semis stabilize.
- New entries: prefer financial/fintech strength or non-semi relative-strength setups after a controlled retest; avoid chasing extended PLTR/HOOD/RBLX/HIMS.

## Orders
- Orders placed: none.
- Order IDs: none.
