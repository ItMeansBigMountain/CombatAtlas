# Autonomous OPEN Swing-Trading Scan — 2026-07-22

- Scan window: 2026-07-22 13:30–13:40 UTC (09:30–09:40 ET)
- Account: Robinhood Agentic account ending 1041 only
- Policy: `playbook/autonomous-policy.md` read and applied
- Scope: long fractional equities only; no options, shorts, crypto, leverage, averaging down, or other accounts
- Decision: **HOLD / NO TRADE / NO ROTATION.** No existing invalidation fired, the four-position policy maximum is already occupied, marked risk is near the soft cap, and opening gaps did not offer a clean non-chasing entry or a materially superior rotation.

## Broker identity, account state, and kill switches

- Identity verified live: active individual cash account, nickname Agentic, `agentic_allowed=true`, self-directed, not deactivated. The other returned accounts were not operated.
- 13:40 UTC portfolio: account value $186.7490; equity value $183.4190; cash and authoritative buying power $3.33; unleveraged buying power $3.33; pending deposits $0.
- Four reconciled long fractional positions, all fully sellable: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09.
- Explicit open-ish order queries were empty for every required state: `new`, `queued`, `confirmed`, `unconfirmed`, and `partially_filled`. Pending equity commitment: $0.
- Recent order/fill history reconciled: the latest order remains the 2026-07-21 Agentic UNH $13.34 market buy, filled 0.031089 shares @ $429.085 with $0 fees. There were no 2026-07-22 fills or closing trades; realized equity P&L for the day is $0 with zero realized trades.
- Below-$10 account kill switch: clear.
- Daily gate: prior-close proxy $188.3712 versus current $186.7490 = -$1.6222 (-0.861%), well inside the -5% pause.
- Peak drawdown gate: versus the latest journal-observed high-water value $203.1386 (2026-06-23), current drawdown is -8.07%, inside the -10% pause. Versus the conservative $200 funding proxy it is -6.63%. The journal high-water value is used because the broker portfolio endpoint does not expose a direct peak field.
- Aggregate marked downside to current management invalidations is approximately $4.74: NVDA $1.05, SOFI $1.70, JPM $1.59, UNH $0.39. Entry-cost downside to those levels is about $6.45, so no additional risk was added near the default ~$6 soft cap.

## Opening regime, sectors, macro, and events

As of approximately 13:40 UTC, SPY was $747.12 (-0.16%), QQQ $704.77 (-0.59%), and IWM $295.705 (-0.28%). SPY remained above its 20/50-day region but below SMA10; QQQ remained below SMA10/20/50 and was the weakest major benchmark. This is a mixed/defensive opening, not broad risk-on confirmation.

Sector breadth showed rotation away from technology: XLB +1.38%, XLE +1.25%, XLU +1.04%, and XLP +0.82% led; XLK -0.79% and SMH -0.87% lagged. XLF -0.10%, XLV +0.03%, XLI +0.09%, XLY -0.06%, XLRE +0.13%, and XLC +0.11% were mixed. Energy retained the strongest 20-day trend (+8.21% through the prior close); financials and health care remained constructive, while QQQ/XLK/SMH structures were still unrepaired.

Macro risk remains elevated. The Federal Reserve's July report said inflation had risen and remained above its 2% objective, with tariff and war-related energy pressures material; current reporting also highlights oil/Iran risk. Major after-close earnings include GOOGL/GOOG, TSLA, IBM, TXN, and NOW, creating overnight index and technology gap risk. The next FOMC window is July 28–29. No held company reports today; SOFI's verified July 29 report remains the nearest held binary event.

## Existing-position management

Management levels are scan-time soft exit triggers, not resting broker stop orders. None was widened.

| Symbol | 13:40 UTC price | Position value / unrealized P&L | Structure and relative strength | Invalidation | Targets | Action |
|---|---:|---:|---|---:|---:|---|
| NVDA | $206.675 | $25.04 / +$0.04 (+0.17%) | Above prior SMA10/20 but below SMA50 $209.74 and $213.81 resistance; holding better than weak SMH but not a clean add. | $198 | $214 / $220 | Hold; no add. |
| SOFI | $17.280 | $77.37 / -$2.64 (-3.30%) | Weakest holding; below SMA10/20 near $17.89 but above SMA50 $17.07 and above the $16.90 trigger. Earnings July 29 raises event risk. | $16.90 sustained loss | $18.60 / $19.74 | Hold under close monitoring; never average down. |
| JPM | $345.165 | $67.36 / +$0.68 (+1.02%) | Strong rising SMA10/20/50 structure and financial-sector relative strength; below $351.24 resistance. | $337 | $351.24 / $360 | Hold; no add near resistance. |
| UNH | $435.570 | $13.54 / +$0.20 (+1.51%) | Above rising SMA10/20/50 after earnings beat and raised adjusted-EPS guidance; health care stable. | $423 | $450 / $461.62 | Hold. |

No stop/invalidation or profit target fired. SOFI remains first exit-review candidate if $16.90 fails on sustained trade/close; JPM, NVDA, and UNH theses remain intact.

## Broad-universe scan and ranked candidates

Robinhood live scanners covered daily gainers and upcoming earnings, then liquidity, price, capitalization, tradability, fundamentals, earnings, and technical filters were applied beyond existing watchlists.

1. **T — 7.3/10 watch.** $23.275 (+4.56%) after verified EPS $0.65 versus $0.59 estimate. Price cleared prior $22.98 20-day resistance and SMA10/20, but faded from $24.29 and sat only marginally above SMA50 $23.01. Prefer a $22.90–$23.05 breakout retest that holds; invalidation $22.25; targets $24.29 then $25.00. Fundamentally profitable, PE ~7.4 and dividend yield ~5.05%, but the first ten-minute fade prevents chasing.
2. **PHM — 7.0/10 watch.** $127.82 (+2.86%) after verified EPS $2.48 versus $2.36 estimate. Above SMA10 $124.77 and SMA50 $122.66, but still below SMA20 $129.30 and fading from $129.06. Prefer a controlled hold/retest of $126–$127 or a reclaim of $129.30; invalidation $124, hard structural invalidation $121.77; targets $129.30 then $140.09. PE ~12.5, but recent revenue and margin trends were weaker and housing remains rate-sensitive.
3. **BLFS — 6.8/10 watch.** $30.91 (+5.89%), above rising SMA10/20/50 and briefly at a new 52-week high $31.4935 with strong early volume. Require a breakout/retest above $31.50; invalidation $29.65; no chase. Small-cap and negative earnings reduce rank.
4. **ARWR — 6.2/10 no-chase.** $88.83 (+19.20%), new 52-week high after positive plozasiran event data/analyst support. Prior trend was below SMA10/20/50 and ATR was ~5.43%; the opening move exceeded multiple ATRs. Require a multi-session base/retest near $84–$87; current entry is disqualified as extended.
5. **SMCI — 5.8/10 no-chase.** $30.30 (+18.82%) on AI-rack/liquid-cooling narrative. Despite strong liquidity and improving recent net margin, prior trend was below SMA10/20/50 with 6.16% ATR and -28.09% 20-day return. Require a hold/retest around $28.50–$29.00 and trend repair; current opening gap is disqualified.

DELL (+7.15%, ATR ~7.99%) and HPE were also reviewed but remained high-volatility rebound/chase candidates. MCO, TDY, TEL, and the broader earnings list did not present cleaner opening setups. Today-after-close reporters were excluded from new swing entries because of immediate binary risk.

## Sizing, review, execution, and verification record

- Liquid BP after pending orders: $3.33 - $0 pending = $3.33.
- Mechanical 80% target: $2.66; nominal 20% reserve: $0.67.
- Current account deployment: $183.4190 / $186.7490 = 98.22%; cash is $3.33 = 1.78% of account value.
- The $3.33 is the deliberately retained 19.98% reserve from the 2026-07-21 $16.67 tranche after the $13.34 UNH deployment. It was not recursively treated as a fresh tranche. Doing so would create a fifth position, erode the intended reserve to $0.67, and add immaterial exposure while aggregate planned risk is already around the soft cap.
- **Order previews:** none. No candidate reached intended-action status, so no broker review was appropriate.
- **Actions:** no buy, sell, cancel, or replacement order was sent. No position was averaged down. No options, shorts, crypto, leverage, or other account was used.
- **Post-decision verification:** portfolio remained four long positions; every open-ish order state remained empty; no new fill appeared.
- **Final decision:** no-trade is policy-compliant rather than forced deployment. Reassess only after a valid retest/confirmation, a position exit frees a slot, or an existing invalidation fires.

## Tool/source exceptions and failures

- The 25-symbol quote batch returned all live quotes but omitted official close objects because that endpoint includes closes for at most 20 symbols. Each quote still included `adjusted_previous_close` and `previous_close`; those broker fields were used for day-change calculations. This did not affect order state or execution because no order was intended.
- Same-minute web search did not provide reliable current release detail for every opening mover (notably some SMCI/DELL/HPE moves). Unverified headlines were not used as trade mandates.
- Robinhood financial-history rows were unavailable for ARWR, BLFS, TDY, and TEL in the requested batch; they were treated as unavailable rather than inferred.
- No broker/account/order/position call failed, and no uncertain state was used to authorize a trade.
