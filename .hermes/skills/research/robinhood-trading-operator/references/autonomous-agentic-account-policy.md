# Autonomous Agentic Account Policy

Session learning: the user explicitly activated no-per-trade-approval autonomous trading for the Robinhood Agentic account ending `1041` / account number `433711041` only.

## Active scope

- Account: Robinhood Agentic account `433711041` / ending `1041` only.
- Default instruments: equities only.
- Fractional shares: allowed and expected for the small account.
- Options: disabled unless separately authorized.
- Shorts: disabled unless separately authorized.
- Other Robinhood accounts: never trade without separate explicit approval.

## Active guardrails

- Kill switch: stop trading if account value drops below `$10`.
- Stop if broker/account/tool state is uncertain.
- Stop if risk cannot be calculated from live account + market data.
- Stop if no clean setup exists.
- Prefer starter positions around `$25-$50`.
- Do not deploy more than 60% of account value across open positions unless a written trade plan justifies it.
- Target max risk per trade: about `$2` unless the user changes it.
- Target aggregate planned open risk: about `$6` unless the user changes it.
- Minimum R:R: `1.5:1`; prefer `2:1+`.
- If account is down 5%+ in one day or 10%+ from recent high, pause new entries and write a review before resuming.
- If a position loses ~8% from entry or breaches thesis/invalidation, review for exit rather than adding.

## Workflow correction

Broad permission alone was initially treated as insufficient. The user then provided exact activation language:

> Activate autonomous trading for Agentic account 1041 with the policy above and kill switch below $10.

That phrase activates Mode 5 for this account only. Future sessions should not keep asking for per-trade approval when acting within the saved policy. They should still verify live broker/account state first.

## Broker-state uncertainty pattern

If Robinhood MCP returns transient server errors such as 502/unreachable, do **not** trade. Report: autonomous mode is armed/active but paused because broker state is uncertain. Resume only after account, positions, orders, quotes, and risk can be verified live.

## Investor-profile / second-trade broker gate

Robinhood may block additional Agentic-account orders with HTTP 400 and a message like: `We're required to have you answer some questions about your investing goals before we can allow you to continue using Robinhood.` Treat this as a broker setup gate, not a strategy/risk failure. Do not retry or route around it. Report that no order was placed, verify same-day orders if needed, journal the blocked attempt, and give the user the broker setup URL returned by the tool, typically:

`https://applink.robinhood.com/investment_profile?account_number=433711041&context=second_trade`

After the user completes the investor profile, rerun the normal live account/positions/orders/quotes/review workflow before placing anything; do not reuse stale preview data.

## Journal path

The active policy file lives at:

`/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`

Journal every autonomous preview, placement, management action, exit, post-trade review, no-trade decision, and tool failure under:

`/opt/data/HeRmEz/projects/trading-journal/YYYY-MM-DD/`

## Research-informed operating lessons

- Robinhood provides the MCP connector, not a full trading strategy. Hermes must explicitly run the saved policy/playbook each scan.
- Treat the agent like an employee: exact task, scope, risk limits, reporting cadence, and escalation rules.
- Keep beta capital small and isolated; do not treat autonomous trading as an income system.
- Avoid over-deploying cash early; leave buying power for risk control and cleaner entries.
- Options are rolling out and remain disabled here unless separately authorized.
- If model/platform/tool capability is uncertain, pause rather than infer autonomy.
