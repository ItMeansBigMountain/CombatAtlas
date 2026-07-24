# AFTERNOON Agentic Swing / Rotation Scan — 2026-07-23

- Scan completed: 2026-07-23 17:34 UTC / 13:34 ET
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only; no options, shorts, other accounts, averaging down, or widened stops
- Decision: **HOLD NVDA AND JPM; NO ROTATION; NO NEW ENTRY.** No order was reviewed or placed in this afternoon scan because no candidate met the live-entry gate and authoritative available buying power supported only a $2.664 policy allocation.

## Verified account state and kill switches

- Account identity verified through `get_accounts`: nickname Agentic, cash individual account, active, `agentic_allowed=true`.
- Final account value: **$184.7411**; equity value **$93.3011**; cash **$91.44**; pending deposits $0.
- Broker-authoritative buying power after pending/open orders: **$3.33**. Cash from today's exits remains largely unavailable as buying power; no settlement assumption was used.
- Final positions: NVDA 0.121165 shares @ $206.33 average; JPM 0.195159 shares @ $341.67 average. Every share is sellable.
- Explicit open-ish order queries were empty for `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled`, both before and after the scan.
- Today's verified prior fills remain: SOFI full exit, 4.477580 shares @ $16.75 at 13:37:22 UTC; UNH full exit, 0.031089 shares @ $421.635 at 16:03:52 UTC. No afternoon-scan fill occurred.
- Kill switches: account value is above $10; change from the $185.1878 opening snapshot is approximately **-0.241%**, below the 5% daily pause; drawdown from the conservative $200 funding proxy is approximately **-7.629%**, below the 10% pause. Broker/account/tool/risk state was sufficiently certain for management decisions.

## Market and sector regime

At the 17:31–17:34 UTC refresh: SPY $738.13 (-1.24%), QQQ $692.36 (-1.84%), and IWM $291.325 (-0.84%). The regime was risk-off and growth-led to the downside. QQQ was below its prior daily SMA10/20/50 ($710.96/$714.25/$719.17), while SPY fell below its prior SMA10/20/50 area ($749.43/$745.67/$745.08). IWM remained above its prior SMA50 ($290.88) but below SMA10/20.

Sector flow was sharply selective: industrials XLI +1.54%, healthcare XLV +0.92%, energy XLE +0.83%, and utilities XLU +0.27% led; consumer discretionary XLY -4.58%, staples XLP -1.74%, semiconductors SMH -1.26%, technology XLK -0.97%, financials XLF -0.57%, and materials XLB -1.02% lagged. Current macro/news context showed higher oil and Treasury yields amid U.S.–Iran escalation, plus post-earnings pressure in technology/consumer names. This favored defense, transport, healthcare, and energy relative strength but increased headline-reversal and inflation/rate risk.

## Existing-position management

### NVDA — HOLD, no add

- Final quote $209.6599 (-1.13%); position value approximately $25.4034; unrealized gain approximately **$0.4035 / +1.61%**.
- Daily structure from the latest completed session: close $212.06; SMA10 $207.44, SMA20 $202.29, SMA50 $209.68; ATR14 approximately $7.46; RSI14 approximately 62.7; 20-day range $189.80–$214.39.
- Intraday: $205.96 low, $210.87 high, approximate VWAP $208.68; price recovered above VWAP but semiconductor and QQQ flows remained weak.
- Fundamentals: PE approximately 31.76; latest reported quarter revenue $81.615B, net income $58.321B, net margin 71.46%; latest verified EPS $1.87 vs $1.76 estimate. Next verified earnings: 2026-08-26 PM.
- Thesis: exceptional AI/data-center growth and margins remain intact, but market/sector relative weakness and $214.39 resistance constrain upside.
- **Stop/invalidation $198; targets $214 and $220.** Planned risk from average entry to stop is approximately $1.009. No stop widening and no averaging down.

### JPM — HOLD, no add into resistance

- Final quote $347.90 (-0.09%); position value approximately $67.8958; unrealized gain approximately **$1.2158 / +1.82%**.
- Daily structure: prior close $348.21; SMA10 $341.28, SMA20 $337.16, SMA50 $320.39; ATR14 approximately $7.81; RSI14 approximately 63.8; 20-day high $351.24.
- Intraday: $345.42 low, $349.23 high, approximate VWAP $347.60; price held near VWAP and materially outperformed XLF.
- Fundamentals: PE approximately 14.70, P/B approximately 2.58; latest verified EPS $6.14 vs $5.59 estimate. Recent reported revenue/net income trend remained strong; latest available quarter revenue $49.836B and net income $16.494B.
- Thesis: bank earnings and relative strength remain constructive, but rising-yield/macro sensitivity and nearby $351.24 resistance argue against adding.
- **Stop/invalidation $337; targets $351.24 and $360.** Planned risk from average entry to stop is approximately $0.911. No stop widening.

Aggregate planned open risk from average entries to written stops is approximately **$1.921**, within the policy's ~$6 target.

## Broad liquid universe and shortlist

Robinhood's live Daily Gainers scan returned 281 equities and Upcoming Earnings returned 347. The liquid filter used price >= $5, volume >= 500,000, market cap >= $2B, then live quotes, account tradability/fractional checks, completed daily OHLCV, 5-minute intraday bars, fundamentals, earnings, and current news. Microcaps, low-liquidity names, low-price spikes, and extended/unclear-stop event gaps were rejected. The checked shortlist was regular-hours and fractional tradable for account 1041.

1. **CSX — 7.7/10, best watch; wait for retest.** $52.725 (+5.60%), intraday $51.62–$53.30, approximate VWAP $52.60. Prior completed daily SMA10/20/50 $49.93/$48.96/$47.28, ATR14 $0.92, RSI14 61.6; breakout volume exceeded the recent average. Q2 EPS $0.54 vs $0.49 estimate; industrial/rail flow aligned with XLI leadership. PE ~31.13 is not cheap. Preferred entry $51.20–$51.60, stop $49.80, targets $54.50/$56; from $51.50, R:R ~1.76/2.65. Live price remained above the entry zone.
2. **RTX — 7.6/10, strong catalyst; no chase.** $209.047 (+7.27%), intraday $202.51–$213.49, approximate VWAP $209.67. Prior SMA10/20/50 $194.77/$193.63/$185.03, ATR14 $4.53, RSI14 56.3. Q2 EPS $1.89 vs $1.66 and reported revenue $24.71B beat estimates; defense/geopolitical and XLI flows supported the move. PE ~36.43 and the rejection from $213.49 reduce entry quality. Entry $203.90–$205 retest/hold, stop $199, targets $214/$220; from $204.50, R:R ~1.73/2.82.
3. **ALLE — 7.3/10, earnings gap; wait for base.** $158.06 (+12.94%), intraday $148.715–$159.27, approximate VWAP $154.73. Prior SMA10/20/50 $137.25/$137.92/$133.54, ATR14 $3.63, RSI14 58.1. Q2 EPS $2.40 vs $2.21; PE ~19.04 is more moderate than other gap leaders. The price is roughly five prior ATRs above the prior close, so entry $151–$153 only after a hold/base, stop $147, targets $160/$166; from $152, R:R 1.60/2.80.
4. **XOM — 7.1/10, energy leader but overbought/event risk.** $157.4826 (+1.96%), intraday $156.06–$158.57, approximate VWAP $157.54. Prior SMA10/20/50 $145.83/$141.68/$138.59, ATR14 $2.19, RSI14 **84.7**. XLE/oil/geopolitical flows support it, but Q2 earnings are verified for 2026-07-31 AM and latest available net margin had compressed to 4.91%. Entry $154.80–$156 hold, stop $150, targets $165/$170; from $155.50, R:R ~1.73/2.64. No chase at current overbought price.
5. **TMO — 7.0/10, strong earnings but extended/fading.** $571.63 (+8.58%), intraday $568.84–$587.49, approximate VWAP $576.02. Prior SMA10/20/50 $530.15/$520.07/$487.42, ATR14 $14.39, RSI14 58.6. Q2 EPS $6.03 vs $5.71; PE ~29.86 and healthcare flow support the thesis, but the price faded below VWAP after a large gap. Require a $545–$555 base, stop $535, targets $590/$610.

MEDP was rejected despite EPS $4.25 vs $3.99 because its gap faded from $677.90 to about $605, below approximate VWAP $619.12. LMT was rejected for a similar post-earnings fade below intraday VWAP after a +9% gap. CLF remained below its declining prior SMA50 despite a 20% event spike; HIMS remained below its prior SMA10/20. No candidate was materially superior enough at a valid entry to justify selling NVDA or JPM.

## Allocation, action, previews, and verification

- Available liquid buying power after all pending/open-order checks: **$3.33**.
- Exact policy target if a setup qualified: **$2.664 deployed (80%)**, **$0.666 retained (20%)**.
- Existing equity exposure: **$93.3011 / 50.50% of account value**. Existing holdings count separately from current available liquid balance under policy.
- **New deployed cash this scan: $0.00. Reserve buying power: $3.33.** The $2.664 mechanical allocation was not forced into an extended gap or an immaterial starter position.
- Management actions: hold NVDA and JPM with unchanged written stops/targets; no trim, exit, add, or rotation.
- Order previews: **none**; no exact live setup passed the entry and materiality gates, so review was not appropriate.
- Executions/fills this scan: **none**.
- Final verification: positions remained NVDA and JPM only; all five open-ish order states remained empty; portfolio buying power remained $3.33.

## Tool/source record and gaps

- Robinhood MCP directly supplied account identity, portfolio/buying power, positions, recent fills, each open-ish order state, scanners, live quotes, account tradability, daily and intraday OHLCV, RSI/ATR indicators, fundamentals, quarterly financials, and earnings.
- Current macro/company-news context was checked through web search, including the July 23 RTX earnings report and July 22–23 market/oil/yield coverage.
- Robinhood quarterly financial rows were unavailable for CSX, MEDP, ALLE, and DHR in the requested batch; current fundamentals and verified earnings remained available. This was treated as a research-data gap, not filled with assumptions.
- No broker/order tool failed, and no rejected placement occurred.
