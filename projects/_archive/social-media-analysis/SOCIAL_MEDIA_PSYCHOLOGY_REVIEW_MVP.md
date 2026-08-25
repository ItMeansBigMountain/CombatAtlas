# Social Media Psychology Review MVP

- **Date:** 2026-05-03
- **Goal:** Let users upload/export social media data and receive statistical + optional LLM-assisted behavioral insights.
- **Revenue priority:** high; modern use case with paid AI tier.

## Product positioning

This should **not** claim to diagnose depression or mental illness. Position it as:

> ?A private behavioral mirror for your social media patterns.?

## Core outputs

| Output | Free/local tier | Paid LLM tier |
| --- | --- | --- |
| Topic stats | yes | yes |
| Word/phrase frequency | yes | yes |
| Sentiment trend | yes | yes |
| Posting time/frequency behavior | yes | yes |
| Algorithmic behavior profile | basic rules | richer explanation |
| Depression-risk language signals | cautious flags only | cautious narrative with disclaimers |
| Personalized recommendations | generic | paid LLM report |

## Input methods

1. Upload full export directory from supported platforms.
2. Upload CSV/JSON text post history.
3. Paste sample posts manually.
4. Later: OAuth/API imports if platform policies allow.

## Stripe standard

Use Stripe Checkout first because it is low-code and supports one-time payments and subscriptions. The paid tier should gate LLM usage and report generation.

Suggested pricing gates:

| Tier | Price model | Includes |
| --- | --- | --- |
| Free | $0 | local stats, no LLM, limited upload size |
| One-time report | fixed price | one LLM-generated report |
| Subscription | monthly | recurring reports, saved history, trend tracking |

Required env placeholders:

```text
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_ONE_TIME_REPORT=
STRIPE_PRICE_MONTHLY=
OPENAI_API_KEY=
MAX_FREE_UPLOAD_MB=
```

## Safety boundaries

- No clinical diagnosis.
- No ?you are depressed? statements.
- Use language like ?signals,? ?patterns,? ?risk indicators,? and ?consider speaking with a professional.?
- Keep uploaded data private by default.
- Allow delete/export.
- Never train on user data without explicit opt-in.

## Source references

- Stripe Checkout docs: https://docs.stripe.com/payments/checkout
- Stripe Checkout lifecycle: https://docs.stripe.com/payments/checkout/how-checkout-works
- Stripe subscriptions: https://docs.stripe.com/subscriptions

## Next implementation slice

Create a local archive analyzer that accepts a directory and emits:

```text
report.json
word_frequency.csv
topic_summary.json
posting_behavior.json
```

Then add Stripe Checkout only after local stats work.
