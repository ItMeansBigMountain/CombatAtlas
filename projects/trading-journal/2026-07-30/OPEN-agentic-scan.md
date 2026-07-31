# OPEN Agentic Swing Scan — 2026-07-30

- Scan time: 13:35–13:40 UTC / 09:35–09:40 ET
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only
- Decision: **HOLD UL; BUY MA $58.88 and SHEL $58.87. Both reviewed, placed, and filled.**

## Live broker state and kill switches

- MCP connected; 52 tools discovered. Account 433711041 was active, cash, Agentic, and `agentic_allowed=true`; no other account was operated.
- Pre-trade portfolio: total value $180.5493; equity $33.3593; buying power/cash $147.19; pending deposits $0.
- Existing position: UL 0.508952 shares @ $66.47, fully sellable.
- All practical open-ish states were queried and empty before action: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`. Recent fills reconciled, including JPM exit 0.195159 @ $345.3735 and SLB exit 1.443558 @ $49.4126 on July 29.
- Kill switches clear: value >$10; live broker and risk state calculable; approximately 9.79% below the conservative $200 funding proxy and materially less than 10% below the recent documented portfolio high, so no drawdown pause triggered.

## Market regime

- Opening tape improved sharply after the prior selloff: SPY ~$735.28 (+0.80%), QQQ ~$675.11 (+2.02%), IWM ~$290.18 (+0.56%). However, completed daily structure remained damaged: SPY below SMA10/20/50; QQQ well below SMA10/20/50; IWM below SMA10/20/50. Regime classified as **high-volatility rebound / selective risk-on, not a fully repaired uptrend**.
- Opening sector leadership: semiconductors/technology surged (SMH about +4.6%, XLK +3.7%) on Microsoft’s verified EPS beat and 43% Azure growth, while healthcare, staples, and communications weakened. Financials and energy were approximately flat at sector level, making stock-specific earnings confirmation important.
- Macro remained restrictive: core PCE reportedly eased to 3.3% y/y but remains above the Fed target; Treasury yields rose after the Fed press conference. AAPL and AMZN report after close, adding index event risk.

## Broad scan and ranking

Robinhood Daily Movers plus liquid mega-cap, sector leaders, earnings winners, benchmark/sector ETFs, live quotes, daily OHLCV, fundamentals, financials, earnings, and web/news context were used beyond stale personal watchlists.

1. **MA — 8.4/10, BUY.** Verified Q2 EPS $5.04 vs $4.76 estimate; opening breakout above prior $569.99 20-day high; completed trend above SMA10/20/50 with +9.68% 20-day strength and high liquidity. Clear earnings-backed invalidation below $566.
2. **SHEL — 8.2/10, BUY.** Q2 adjusted earnings $9.8B, CFFO $21.4B, $3B buyback, net debt ~$41.8B; opening breakout over the prior $89.41 20-day high; completed trend above SMA10/20/50 and +13.93% 20-day strength. Clear invalidation below $87.80.
3. **MSFT — 7.8/10, WAIT.** Verified EPS $4.74 vs $4.23 and Azure +43%, but the ~15% opening gap was too extended for controlled swing risk.
4. **BMY — 7.3/10, WAIT.** Verified EPS $2.04 vs $1.61 and strong trend, but price did not confirm the beat with a breakout.
5. **PWR/EME — 6.8/10, AVOID FOR NOW.** Large verified EPS beats, but both remained deeply below declining SMA10/20/50 structures; catalyst did not repair trend.

## Position plans and exact actions

### UL — HOLD
- Live after action: ~$65.58; 0.508952 shares @ $66.47.
- Thesis: upgraded 2026 outlook, volume-led growth, defensive exposure; completed price remains above SMA10/20/50.
- Binding reassessment/exit: **$63.70**. Targets: **$70.75 / $74.90**.
- Planned risk: ~$1.41; T1 reward ~$2.18, **1.55:1**. No averaging down.

### MA — BOUGHT/FILLED
- Reviewed: buy $58.88 market; no broker alerts.
- Compliance quote: **Bid $579.01 × 160 Q · Ask $580.40 × 80 N · Last $579.77 × 41 D. Updated 9:39 AM ET.**
- Filled: **0.101447 shares @ $580.3999**, $58.88, fee $0. Order `6a6b5412-7705-44a0-ae9c-221c91a2598b`.
- Stop/reassessment: **$566**. Targets: **$603 / $615**. Expected duration: days to several weeks.
- Planned risk ~$1.46; T1 reward ~$2.29 (**1.57:1**); T2 reward ~$3.51 (**2.40:1**).
- Exit early if the earnings breakout fails and closes/retests below $566, payment-volume/guidance thesis deteriorates, or financial relative strength breaks.

### SHEL — BOUGHT/FILLED
- Reviewed: buy $58.87 market; no broker alerts.
- Compliance quote: **Bid $90.40 × 200 Q · Ask $90.41 × 300 Q · Last $90.40 × 200 D. Updated 9:39 AM ET.**
- Filled: **0.651145 shares @ $90.4099**, $58.87, fee $0. Order `6a6b5412-fce8-4e3e-b65a-77778744c7c7`.
- Stop/reassessment: **$87.80**. Targets: **$94.90 / $98.00**. Expected duration: days to several weeks.
- Planned risk ~$1.70; T1 reward ~$2.92 (**1.72:1**); T2 reward ~$4.94 (**2.91:1**).
- Exit early if the breakout loses $87.80, energy/oil reverses materially, or cash-flow/buyback thesis changes.

## Allocation and post-trade verification

- Liquid buying power after pending orders before entries: **$147.19**. Policy target: exactly 80% = **$117.752** deployable; 20% = **$29.438** reserved.
- Deployed: **$117.75** across MA and SHEL; final buying power/cash **$29.44**. This matches the 80%/20% liquid-balance target to the cent.
- Post-trade portfolio: total value **$180.4232**; equity **$150.9832 (83.68%)**; cash **$29.44 (16.32%)**.
- Verified positions: UL, MA, SHEL. Both new orders independently verified **filled**, leaving $0 pending notional.
- Aggregate planned risk to written invalidations: **~$4.57**, within the ~$6 soft policy target. Stops are written scan-managed levels, not broker-native protective orders; gaps can exceed planned loss.

## Tool record / failures

- Initial Daily Movers request used the obsolete `watchlist_id` parameter, historicals used obsolete `span`, and one fundamentals batch exceeded the 10-symbol maximum. All were journaled here, corrected using dynamically discovered schemas (`list_id`, RFC3339 `start_time`, max-10 batches), and successfully rerun.
- MCP session shutdown emitted a non-blocking HTTP 400 after successful calls; all broker payloads and fills were returned and independently verified, so broker state was not left uncertain.
