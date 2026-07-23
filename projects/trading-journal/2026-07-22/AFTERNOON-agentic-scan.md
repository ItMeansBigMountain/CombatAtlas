# Autonomous AFTERNOON Swing/Rotation Scan — 2026-07-22

- Scan: 2026-07-22 17:30–17:32 UTC
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Decision: **HOLD / NO TRADE / NO ROTATION**

## Live broker state

- Account verified active cash account with `agentic_allowed=true`; no other account operated.
- Portfolio value **$187.0207**; equity value **$183.6907**; cash and buying power **$3.33**; pending deposits $0. Below-$10 kill switch clear.
- Positions reconciled: NVDA 0.121165 @ $206.33; SOFI 4.477580 @ $17.87; JPM 0.195159 @ $341.67; UNH 0.031089 @ $429.09. No options/shorts.
- All open-ish equity states (`new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`) explicitly returned empty; pending commitment $0.
- Recent filled-order query reconciled the held lots, including JPM $66.68 @ $341.6699 (July 20) and UNH $13.34 @ $429.085 (July 21). No fill/action occurred in this scan.
- Daily drawdown pause not triggered relative to yesterday's $187.0557 close-scan baseline (approximately flat). Direct high-watermark remains unavailable; no new risk was taken.

## Market and sector regime

At ~17:31Z: SPY $749.215 (+0.12% vs prior close), QQQ $708.93 (-0.01%), IWM $294.51 (-0.68%), XLK $181.06, XLF $56.00, SMH $591.74. Breadth is mixed: large caps flat, small caps lagging, semiconductors rebounding intraday but SMH remains below its 20/50-day averages. Oil/Middle-East escalation remains an inflation risk; major technology earnings and the July 28–29 Fed window are near-term event risks. Financials retain the cleanest relative trend; defensive healthcare has a confirmed post-earnings catalyst.

## Holdings and management

| Symbol | Live / value | P/L | Structure + fundamental context | Stop / targets | Action |
|---|---:|---:|---|---|---|
| NVDA | $214.21 / $25.95 | +$0.95 (+3.82%) | Above 10/20-day averages and testing 20-day resistance near $214; AI earnings record remains supportive, but below 50-day trend and chip regime is not fully repaired. | $198 / $214, $220 | Hold; no add into resistance. |
| SOFI | $17.14 / $76.75 | -$3.27 (-4.09%) | Above $16.90 management stop but below 10/20-day averages (~$17.89); weakest holding. Q1 EPS only met estimate and July 29 earnings creates binary risk. | $16.90 / $18.60, $19.74 | Hold narrowly; exit review on sustained loss of $16.90; never average down. |
| JPM | $346.93 / $67.71 | +$1.03 (+1.54%) | Above rising 10/20/50-day averages; XLF near highs. Q2 EPS $6.14 beat $5.59 estimate. Resistance $351.24. | $337 / $351.24, $360 | Hold; no chase. |
| UNH | $433.43 / $13.47 | +$0.13 (+1.01%) | Above 10/20/50-day averages after Q2 beat and raised 2026 adjusted-EPS guidance; turnaround evidence remains intact. | $423 / $450, $461.62 | Hold. |

Marked risk to unchanged stops is approximately $5.13, within the ~$6 soft aggregate target. Stops are scan-time management triggers, not resting orders; none was widened.

## Ranked fresh candidates

1. **AMD (7.5/10):** $557.01, high-volume catalyst move during Advancing AI event; above 10/20/50-day averages. Strong AI-server roadmap and repeated EPS beats support the thesis, but +intraday extension, ~7% ATR, August 4 earnings, and resistance near $585 make entry R:R poor. Wait for $525–540 retest; invalidation ~$500; targets $585/$620.
2. **NVDA (7.2/10):** best liquid AI quality but already held and testing $214 resistance; no averaging/chasing.
3. **JPM (7.1/10):** strongest low-volatility trend and post-earnings quality, but already held near $351 resistance.
4. **UNH (7.0/10):** strong earnings/guidance catalyst and repaired trend, but already held; preferable add only after a clean $423–428 retest, not with no deployable tranche.
5. **SMCI (5.8/10):** $31.31 on exceptional volume, but below 10/20/50-day structure and governance/margin/cash-flow concerns make the spike unsuitable for a swing entry.

## Deployment and action record

- Current marked equity exposure: approximately **$183.88 / $187.02 = 98.32%**; broker cash reserve **$3.33 (1.78%)**.
- Pending orders: $0. Nominal 80% of current liquid balance is $2.664 and 20% is $0.666, but the $3.33 is the retained 20% reserve from the prior $16.67 decision tranche, not recursively new deployable capital.
- Four-position policy maximum is already reached. Spending $2.66 would create an immaterial fifth holding, erode the intended broker buffer, and increase risk without a superior setup.
- **No order reviewed, placed, sold, or canceled. No fill occurred.** Existing theses remain valid; SOFI did not breach $16.90, and rotating into extended AMD/SMCI strength would be churn.

Next triggers: SOFI sustained below $16.90; JPM below $337; NVDA below $198; UNH below $423. No outcome is guaranteed.
