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
- Target max risk per trade: about `$2` unless the user changes it.
- Target aggregate planned open risk: about `$6` unless the user changes it.
- Minimum R:R: `1.5:1`; prefer `2:1+`.

## Workflow correction

Broad permission alone was initially treated as insufficient. The user then provided exact activation language:

> Activate autonomous trading for Agentic account 1041 with the policy above and kill switch below $10.

That phrase activates Mode 5 for this account only. Future sessions should not keep asking for per-trade approval when acting within the saved policy. They should still verify live broker/account state first.

## Broker-state uncertainty pattern

If Robinhood MCP returns transient server errors such as 502/unreachable, do **not** trade. Report: autonomous mode is armed/active but paused because broker state is uncertain. Resume only after account, positions, orders, quotes, and risk can be verified live.

## Journal path

The active policy file lives at:

`/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`

Journal every autonomous preview, placement, management action, exit, and post-trade review under:

`/opt/data/HeRmEz/projects/trading-journal/YYYY-MM-DD/`
