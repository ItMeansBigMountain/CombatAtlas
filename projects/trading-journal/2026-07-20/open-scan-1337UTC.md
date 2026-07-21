# Agentic OPEN Scan — 2026-07-20 13:37 UTC

## Decision
- **No new order; hold NVDA and SOFI.** No review/place call was made because no candidate cleared the opening-gap/retest and aggregate-risk gates.
- Account limited to Agentic ••••1041 (full broker account 433711041 used only in tool calls). Account is active, cash, and `agentic_allowed=true`.

## Live broker state
- Account value: **$185.5846**; equity value **$102.2346**; cash / buying power **$83.35**.
- Open-ish equity orders checked separately: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled` — all empty. Therefore liquid buying power after pending orders is **$83.35**.
- Recent orders/fills since 2026-07-17 00:00 UTC: none.
- Positions at live 13:36:57–13:36:58 UTC quotes:
  - NVDA 0.121165 sh, avg $206.33; $207.60; value ~$25.15; unrealized +$0.15 (+0.62%).
  - SOFI 4.477580 sh, avg $17.87; $17.17; value ~$76.88; unrealized -$3.13 (-3.92%).
- Kill switches: value above $10; no open-order ambiguity; account/tool state verified. Starting-capital drawdown is about 7.2%, below the 10% recent-high pause threshold, but the exact recent account high was not supplied by the portfolio tool. No evidence of a 5% one-day account drawdown from available broker state.

## Deployment math
- Policy target from currently liquid balance: deploy exactly **80% = $66.68**, reserve **20% = $16.67**.
- Existing equity exposure is ~55.1% of total account value and counts separately under the current policy.
- Existing planned technical risk to practical review levels (NVDA $189.80 / SOFI $16.47) is approximately **$5.29**, already close to the default ~$6 aggregate-risk target. Spending $66.68 on the available high-beta setups with defensible stops would breach that target; cash remains undeployed rather than forcing a trade.

## Market regime
- Opening risk-on rebound, but still a retest rather than a confirmed new uptrend: SPY $748.28 (+0.67% vs prior close), QQQ $704.67 (+1.34%), IWM $295.03 (+0.34%).
- Sector flow: semiconductors led sharply (SMH +2.88%); XLK +1.57%, XLU +1.04%, XLI +0.67%. Financials, energy, healthcare, and staples were flat-to-negative.
- Prior-session daily structure remained damaged in growth: QQQ prior close $695.33 was below its 10/20/50-day averages (~714.29/718.35/719.01); SPY was below its 10-day and around its 20/50-day averages; IWM was below 10/20-day but above 50-day. Thus the first seven minutes' semiconductor gap was not chased.
- Macro/news context: futures and live tape showed a strong technology-led rebound. However, last week's chip drawdown and skepticism around AI monetization remain material; Alphabet/hyperscaler earnings are a near-term sector catalyst. June inflation reportedly moderated but remained above target, while geopolitical risks supported recent energy strength. Web search quality was mixed, so broker market data and earnings calendar received greater weight.

## Ranked candidates
1. **NVDA — 8.0/10, hold only.** $207.60 (+2.36%); above 20-day (~$202.13), below 50-day (~$209.91), 20-day range $189.80–$213.99, ATR14 ~$7.35. Strong liquidity/fundamentals and relative strength in the rebound, but already owned and opening entry is below resistance. Invalidation/review: close/loss of $199–202; hard thesis review near $189.80. Targets: $214, then $220–225.
2. **PLTR — 7.2/10, watch.** $133.46 (+0.82%); above 10/20-day (~$131.93/$125.25), near 50-day (~$132.48), resistance $138.90. Better structure than most growth peers, but expensive valuation and no fresh catalyst confirmation. Trigger only on a hold/retest of $131.5–133 or breakout acceptance above $139; invalidation ~$125; targets $145/$152.
3. **AMD — 7.0/10, wait for retest.** $520.24 (+4.94%); strong liquid semiconductor rebound, but still below 10/20-day (~$529.85/$533.02), ATR14 ~$40.70, and opening move is extended. A defensible stop near $495–500 creates too much dollar risk for a $66.68 allocation. Trigger: reclaim/hold $530–533 after retest; invalidation below $495; targets $560/$584.
4. **AVGO — 6.8/10, watch.** $382.50 (+3.15%); reclaimed around its 20-day (~$381.84) but remains below 50-day (~$402.94). Trigger only if $378–382 holds; invalidation below $370/356; targets $403/$415. Gap and wide technical stop fail sandbox risk math now.
5. **HOOD — 6.1/10, watch.** $100.24 (+0.28%); above 50-day (~$93.02), but below 10/20-day (~$111.59/$107.29) and rejected from $102.48 opening high. Invalidation below $92.80; targets $107/$112. Relative strength and immediate chart quality lag tech leaders.

Robinhood Daily Movers was also queried beyond stale watchlists. Its list was dominated by ADRs/small or special-situation names and a sharp ISRG decline. These were rejected for liquidity/catalyst/technical clarity; ISRG remained below all key averages after a high-volume breakdown despite its opening bounce.

## Position management
- **NVDA: hold, no add.** Do not move invalidation lower. Reassess on loss of $199–202 or failure at $210–214.
- **SOFI: hold under close watch, no add.** $17.17 is below 10/20-day (~$18.06/$17.91) but above 50-day (~$17.02) and the 20-day low ($16.47). Finance sector was slightly weak. Reassess/exit if $16.47–16.70 breaks; recovery targets $17.90, then $19.20–19.74.

## Orders / fills / tools
- Reviews: none.
- Placements/cancellations: none.
- Fills: none since the requested recent-order window.
- Tool failures: none. Web-news search produced mixed-quality current sources; treated as a research limitation, not broker-state uncertainty.
