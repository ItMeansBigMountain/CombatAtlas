# Affiliate Operations

Amazon-first local registry for programs, accounts, tracking IDs, links, tax-interview status, payment readiness, earnings imports, and audit history.

## Privacy boundary

Never enter passwords, access keys, bank numbers, SSNs/TINs, or tax-document contents. Store only status and a secure external reference. The SQLite database is local and should not be committed.

## Current verified state

The supplied screenshot verifies that the US Amazon Associates dashboard is accessible and shows an active account session. It does **not** expose a tracking ID, payment method, tax interview status, API credential, or reliable earnings total. Those fields remain `unknown`.

## Commands

```bash
python3 affiliate_ops.py report
python3 affiliate_ops.py add-account --alias amazon-us-primary --tracking-id YOUR-ID-20 --status active
python3 affiliate_ops.py set-tax --account amazon-us-primary --status completed --form W-9 --jurisdiction US --submitted YYYY-MM-DD --document-ref 'secure-vault://reference-only'
python3 affiliate_ops.py add-link --account amazon-us-primary --label ryan-obstacle --destination https://www.amazon.com/dp/1591846358 --asin 1591846358 --campaign daily-stoic --channel youtube
python3 affiliate_ops.py export-env --account amazon-us-primary
python3 dashboard.py
```

Dashboard: `http://127.0.0.1:8765` (localhost only).

## YouTube labels

The export command maps these labels into the Daily Stoic pipeline:

- `daily-stoic-life` → `DAILY_STOIC_AFFILIATE_URL`
- `ryan-obstacle` → `RYAN_HOLIDAY_AFFILIATE_URL`
- `robert-48-laws` → `ROBERT_GREENE_AFFILIATE_URL`

Only create links after reading the tracking ID from Associates Central. Never guess it.

## Creators API

Product Advertising API passed its documented May 15, 2026 deprecation date. New integration work targets Amazon Creators API when this Associates account actually has access and credentials. SiteStripe remains the safe no-API fallback.

`creators_api.py` is a real server-side OAuth/catalog client that stays disabled until these are supplied from an external secret environment:

- `AMAZON_CREATORS_CREDENTIAL_ID`
- `AMAZON_CREATORS_CREDENTIAL_SECRET`
- `AMAZON_CREATORS_CREDENTIAL_VERSION` (`3.1` for North America)
- `AMAZON_PARTNER_TAG`
- `AMAZON_MARKETPLACE` (`www.amazon.com` for US)

It caches OAuth tokens, conservatively limits calls to one request/second, batches 1–10 ASINs for `GetItems`, requests `offersV2`, and never writes credentials. Missing credentials return `AMAZON_API_NOT_CONFIGURED`; it does not fabricate sample data. Secrets belong in `/opt/data/secrets/affiliate-ops/` with mode `0600`.

## Publishing gate

No unverified tracking ID, Special Link, or API credential is configured. Current direct product-link fallbacks are non-attributed marketing links. FTC-compliant YouTube affiliate endorsements require disclosure inside the video itself—preferably spoken and visual—not only in the description. Add that render/script disclosure before enabling tracked-link publishing.
