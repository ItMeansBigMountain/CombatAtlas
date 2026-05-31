# Google Credentials Inventory

Last reviewed: 2026-05-31

Private keys, client secrets, and token values were intentionally **not** copied into this document.

## Summary

| Label | Credential type | Google project ID / name | Principal | Canonical path | Status |
| --- | --- | --- | --- | --- | --- |
| Workspace / assistant service account | Service account JSON | `airy-sled-497503-r8` | `ai-service@airy-sled-497503-r8.iam.gserviceaccount.com` | `/opt/data/credentials/google-creds.json` | Previously identified as the personal-assistant Google Workspace credential. Keep as canonical for Workspace-style automation unless a newer instruction supersedes it. |
| Secondary service account | Service account JSON | `gen-lang-client-0835809364` | `ai-service@gen-lang-client-0835809364.iam.gserviceaccount.com` | `/opt/data/google_service_account.json` | Currently referenced by `/opt/data/.env` as `GOOGLE_APPLICATION_CREDENTIALS`. Needs a decision: keep as active default, or switch default back to `/opt/data/credentials/google-creds.json`. |
| Legacy tweet video generator OAuth | OAuth client JSON | `autotweet-357502` | OAuth client ID only; secret not exposed here | `/opt/data/HeRmEz/projects/tweet_video_generator/googleAUTH/cred.json` | Legacy YouTube/social video project OAuth credential. Mode tightened to `600`. Duplicated in legacy/archive paths. |

## Duplicate copies found

### `airy-sled-497503-r8`

Same service-account principal appears at:

- `/opt/data/credentials/google-creds.json`
- `/opt/data/HeRmEz/.hermes/credentials/google-creds.json`

Recommended canonical path:

```text
/opt/data/credentials/google-creds.json
```

### `gen-lang-client-0835809364`

Same service-account principal appears at:

- `/opt/data/google_service_account.json`
- `/opt/data/HeRmEz/.hermes/google_service_account.json`

Recommended canonical path if retained:

```text
/opt/data/google_service_account.json
```

### `autotweet-357502`

Same OAuth client credential appears at:

- `/opt/data/HeRmEz/projects/tweet_video_generator/googleAUTH/cred.json`
- `/opt/data/HeRmEz/projects/legacy-src/tweet_video_generator/googleAUTH/cred.json`
- `/opt/data/HeRmEz/legacy-projects/tweet_video_generator/googleAUTH/cred.json`
- `/opt/data/HeRmEz/legacy-projects/legacy-src/tweet_video_generator/googleAUTH/cred.json`

Recommended action:

- Keep only if the legacy tweet/video generator still needs YouTube OAuth.
- Do not use it for Google Workspace assistant automation.
- Do not use service-account JSON for user-channel YouTube uploads/analytics unless Google explicitly supports that flow for the target operation.

## Current active environment reference

`/opt/data/.env` currently points Google Application Default Credentials at:

```text
GOOGLE_APPLICATION_CREDENTIALS=/opt/data/google_service_account.json
```

That means the runtime default currently resolves to project:

```text
gen-lang-client-0835809364
```

## API lookup result

Tried to look up human-readable project display names through Cloud Resource Manager using the service-account credentials. Both service-account projects returned `cloudresourcemanager_api_disabled`, so I could confirm the project IDs from the JSON files but not the console display names.

## Recommended organization

Use purpose-based names instead of guessing from file names:

```text
/opt/data/credentials/google-workspace-assistant-sa.json -> airy-sled-497503-r8
/opt/data/credentials/google-secondary-sa.json           -> gen-lang-client-0835809364
/opt/data/credentials/google-youtube-legacy-oauth.json   -> autotweet-357502 OAuth client
```

Do not rename/move yet unless we also update all code/env references in the same commit.

## Decision needed before deleting or switching anything

Choose the active default for `GOOGLE_APPLICATION_CREDENTIALS`:

1. Keep current: `/opt/data/google_service_account.json` / `gen-lang-client-0835809364`.
2. Switch back to prior canonical: `/opt/data/credentials/google-creds.json` / `airy-sled-497503-r8`.

Given prior notes, option 2 looks more consistent for personal-assistant Workspace automation, but it should be tested before changing the global `.env`.
