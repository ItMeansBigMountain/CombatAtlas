# OPEN Agentic Swing Scan — 2026-07-29

- Scan time: 13:36–13:45 UTC / 09:36–09:45 ET
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only
- Decision: **HOLD JPM, SLB, and UL; NO NEW ENTRY, EXIT, ROTATION, REVIEW, CANCELLATION, OR STOP WIDENING. Reassess after opening volatility and the July 29 FOMC decision.**

## Live broker state and kill switches

- MCP connected and dynamically discovered 52 tools. Account 433711041 is active, cash, named Agentic, and `agentic_allowed=true`; no other account was operated.
- Live portfolio: total value **$185.5552**, equity value **$177.0952**, cash/unleveraged buying power **$8.46**, pending deposits $0.
- Fully sellable positions: JPM 0.195159 @ $341.67; SLB 1.443558 @ $50.67; UL 0.508952 @ $66.47.
- All practical open-ish equity states queried separately and empty: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`. Pending notional $0; liquid buying power after pending orders **$8.46**.
- Recent fills reconciled: UL buy $33.83 / 0.508952 @ $66.4699 on July 28; NVDA sell 0.121165 @ $198.0666 on July 27. No July 29 fill appeared.
- Kill switches clear: value >$10; broker/account state and risk are calculable; value is about **1.23% below** the July 24 value of $187.8664 and **7.22% below** the conservative $200 funding proxy, below the 10% drawdown pause. No new-entry action was nevertheless justified.

## Opening market regime

- Live: SPY **$740.07 (-0.11%)**, QQQ **$676.13 (+0.09%)**, IWM **$293.51 (+0.05%)**. SPY is below completed SMA10/20/50 (~744.37/746.65/744.86); QQQ is below all three (~696.32/708.06/716.75); IWM is below SMA10/20 but above SMA50. This is not a confirmed broad risk-on tape.
- Sector leadership remains defensive/value: XLE **+2.78%**, XLV approximately flat with a strong 10/20/50-day uptrend, while XLF retains a strong completed trend despite opening -0.33%. XLK is below all key averages and SMH remains deeply below them. Technology/chips remain the weak pocket.
- Macro/event risk is unusually high: the FOMC rate decision and press conference are due today, while heavy earnings and tariff/oil uncertainty can reverse opening moves. Opening data were sampled only minutes after the bell, so volume was not treated as confirmation.

## Position management

### JPM — HOLD
- Live **$356.73**, bid/ask $356.82/$357.00; value ~$69.62; unrealized **+$2.94**. Above SMA10/20/50 (~348.01/341.64/324.62), 20-day relative strength ~+8.98%, and near $359.30 resistance.
- Strong Q2 results and upward estimate revisions support the thesis; Fed/rate and credit sensitivity are the immediate risks.
- Binding reassessment/exit **$346**; targets **$365/$375**. Current marked cushion to stop ~$2.09. Do not widen or add near resistance before FOMC.

### SLB — HOLD
- Live **$51.13**, bid/ask $51.10/$51.16; value ~$73.81; unrealized **+$0.66**. Above SMA10/20 (~48.34/$47.48), near SMA50 ~$51.29, with 20-day relative strength ~+9.98%; $53.20 is resistance.
- Q2 beat and guidance for sequential growth support the thesis; cyclicality, Middle East disruption, and oil reversal remain risks. XLE leadership is supportive this morning.
- Binding reassessment/exit **$50.00**; targets **$54.80/$57.00**. Current marked risk to stop ~$1.63. No chase/add.

### UL — HOLD, monitor gap retest
- Live **$65.57**, bid/ask $65.56/$65.57; value ~$33.37; unrealized **-$0.46**. It is down ~1.94% after the prior session's earnings gap but remains above SMA10/20/50 (~62.06/61.76/59.37) and above the binding failed-gap threshold.
- Q2 underlying sales reportedly grew 5.8% with volume +5.5%, supporting the fundamental thesis. The opening pullback and post-gap supply are risks; no averaging down.
- Binding reassessment/exit **$63.70**; targets **$70.75/$74.90**. Current marked risk to stop ~$0.95.

## Ranked fresh candidates

1. **JPM — 8.0/10, existing hold.** Clean financial relative strength and strong fundamentals, but near resistance and already owned.
2. **AAPL — 7.5/10, wait.** Strong 10/20/50 trend and ~+17.7% 20-day strength, but live ~$340.70 is near $342.89 resistance and tech/QQQ confirmation is weak ahead of event risk.
3. **XOM — 7.3/10, wait for retest.** Energy leadership, strong trend and +3.33% opening move, but live ~$158.13 is near $158.71 20-day resistance; chasing gives poor invalidation.
4. **RTX — 7.1/10, wait.** Strong trend and ~+15.3% 20-day strength, but live ~$218.78 is close to $221.34 resistance and industrials opened weak.
5. **UL — 7.0/10, existing hold.** Catalyst-backed defensive trend; manage the post-gap retest rather than add.

## Allocation and action

- Existing equity exposure **$177.0952 / 95.44%** of account value; cash **$8.46 / 4.56%**.
- Available liquid buying power after pending orders: **$8.46**. Mechanical 80%/20% split is **$6.768 deployable / $1.692 reserved**, but existing exposure already materially exceeds the portfolio deployment objective. Spending the residual reserve into opening/FOMC risk would be forced trading, not disciplined deployment.
- Current marked risk to binding stops is approximately **$4.68** aggregate, within the ~$6 soft target. JPM's stop is above cost and locks a gain; aggregate original-cost risk net of that locked gain is ~$1.53.
- **Orders reviewed: none; no setup qualified. Orders placed/cancelled: none. Fills this scan: none. Cash deployed: $0. Final liquid reserve: $8.46.**
- Stops are written reassessment levels, not broker-native protective orders; gaps can exceed planned loss. Recheck at midday after opening structure and FOMC expectations develop.

## Sources/tool record

Robinhood MCP supplied live account, portfolio, positions, five open-ish state checks, fills, quotes, daily OHLCV, fundamentals, earnings calendar/results, and tradability. Web checks corroborated the July 29 FOMC event, JPM estimate revisions/strong Q2, SLB's Q2 beat and growth guidance, and UL's volume-led Q2 result. No unresolved broker/tool failure remained.
