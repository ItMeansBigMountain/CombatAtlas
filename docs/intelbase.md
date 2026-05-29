# IntelBase Helper

Scanned docs:

- `https://docs.intelbase.is/introduction`
- `https://docs.intelbase.is/llms.txt`
- `https://docs.intelbase.is/api-reference/introduction.md`
- `https://docs.intelbase.is/api-reference/endpoint/lookup_email.md`
- `https://docs.intelbase.is/api-reference/openapi.json`

Published API surface as of this scan:

- Base URL: `https://api.intelbase.is`
- Authentication: `x-api-key: <INTEL_BASE_API_KEY>` header
- Endpoint: `POST /lookup/email`
- Body fields:
  - `email` string, required
  - `timeout_ms` integer, optional
  - `include_data_breaches` boolean, optional
  - `exclude_modules` string array, optional
- Docs note that the calling IP must be whitelisted in the IntelBase dashboard.

## Usage

```bash
python scripts/intelbase_lookup.py you@example.com --i-am-authorized
python scripts/intelbase_lookup.py you@example.com --include-data-breaches --timeout-ms 30000 --i-am-authorized
```

The helper reads `INTEL_BASE_API_KEY` from the shell, `/opt/data/.env`, or `~/.hermes/.env`.

## Safety boundary

Use only for accounts you own, have consent to investigate, or are authorized by an organization to assess. The current documented IntelBase API supports **email lookup**, not broad name/person lookup.
