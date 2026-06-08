# Google Credentials Inventory

Last reviewed: 2026-06-08

Private keys, client secrets, access tokens, refresh tokens, and API key values were intentionally **not** copied into this document.

## Current storage decision

Google credentials are now staged under a durable, non-repo secrets directory:

```text
/opt/data/secrets/google/
```

That directory is outside `/opt/data/HeRmEz` and is excluded by the daily HeRmEz backup script, so it should survive VPS/container restarts without being committed or pushed to GitHub.

## Stable environment references

`/opt/data/.env` now contains stable path references:

```text
GOOGLE_CREDENTIALS_DIR=/opt/data/secrets/google
GOOGLE_APPLICATION_CREDENTIALS=/opt/data/secrets/google/service-accounts/hermes-base-airy-sled-497503-r8.json
HERMES_GOOGLE_OAUTH_CLIENT_SECRET=/opt/data/secrets/google/oauth-clients/hermes-user-oauth-client-secret.json
HERMES_GOOGLE_PROFILES_DIR=/opt/data/secrets/google/tokens
YOUTUBE_MAIN_CLIENT_SECRET=/opt/data/secrets/google/youtube/youtube-main-client-secret.json
YOUTUBE_MAIN_UPLOAD_TOKEN=/opt/data/secrets/google/youtube/youtube-main-upload-token.json
```

## Canonical credential files

| Purpose | Type | Project ID / name | Principal / client | Canonical path | Status |
| --- | --- | --- | --- | --- | --- |
| Workspace / assistant service account | Service account JSON | `airy-sled-497503-r8` | `ai-service@airy-sled-497503-r8.iam.gserviceaccount.com` | `/opt/data/secrets/google/service-accounts/hermes-base-airy-sled-497503-r8.json` | Active default via `GOOGLE_APPLICATION_CREDENTIALS`. |
| Secondary service account | Service account JSON | `gen-lang-client-0835809364` | `ai-service@gen-lang-client-0835809364.iam.gserviceaccount.com` | `/opt/data/secrets/google/service-accounts/gen-lang-client-ai-service.json` | Retained for compatibility/reference. |
| Hermes user OAuth client | OAuth client JSON | `hermes-user-oauth` | OAuth client ID redacted | `/opt/data/secrets/google/oauth-clients/hermes-user-oauth-client-secret.json` | Stable OAuth client-secret path for future Workspace OAuth flows. |
| Legacy tweet/video generator OAuth | OAuth client JSON | `autotweet-357502` | OAuth client ID redacted | `/opt/data/secrets/google/oauth-clients/autotweet-357502-client-secret.json` | Retained for legacy YouTube/social video code. |
| YouTube main OAuth client | OAuth client JSON | `faceless-youtube-channel` | OAuth client ID redacted | `/opt/data/secrets/google/youtube/youtube-main-client-secret.json` | Stable YouTube upload/client-secret path. |
| YouTube main upload token | OAuth token JSON | `faceless-youtube-channel` | token values redacted | `/opt/data/secrets/google/youtube/youtube-main-upload-token.json` | Stable YouTube upload token path. |
| Faceless YouTube channel OAuth client | OAuth client JSON | `faceless-youtube-channel` | OAuth client ID redacted | `/opt/data/secrets/google/youtube/faceless-youtube-channel-client-secret.json` | Retained copy. |
| Faceless YouTube upload token | OAuth token JSON | `faceless-youtube-channel` | token values redacted | `/opt/data/secrets/google/youtube/faceless-youtube-channel-upload-token.json` | Retained copy. |
| Google profile token: `personal-secondary` | OAuth token JSON | from token/client metadata | token values redacted | `/opt/data/secrets/google/tokens/personal-secondary/google_token.json` | Profile-isolated token copy. |
| Google profile token: `classicalechos` | OAuth token JSON | from token/client metadata | token values redacted | `/opt/data/secrets/google/tokens/classicalechos/google_token.json` | Profile-isolated token copy. |
| Google profile token: `personal-main` | OAuth token JSON | from token/client metadata | token values redacted | `/opt/data/secrets/google/tokens/personal-main/google_token.json` | Profile-isolated token copy. |
| Google profile token: `hermes-agent` | OAuth token JSON | from token/client metadata | token values redacted | `/opt/data/secrets/google/tokens/hermes-agent/google_token.json` | Profile-isolated token copy. |
| Google profile token: `burner` | OAuth token JSON | from token/client metadata | token values redacted | `/opt/data/secrets/google/tokens/burner/google_token.json` | Profile-isolated token copy. |

## Legacy/source copies retained locally

The following local copies may still exist for compatibility, but should not be treated as canonical:

- `/opt/data/credentials/google-creds.json`
- `/opt/data/google_service_account.json`
- `/opt/data/google_client_secret.json`
- `/opt/data/google_profiles/*/google_token.json`
- `/opt/data/secrets/youtube-main/*`
- `/opt/data/secrets/faceless-youtube-channel/*`
- `/opt/data/HeRmEz/.hermes/google_service_account.json`
- `/opt/data/HeRmEz/projects/tweet_video_generator/googleAUTH/cred.json`

## Git safety

- `.env` files are ignored.
- `google_service_account.json`, `*service_account*.json`, and `cred.json` are now ignored.
- Previously tracked credential files were removed from the Git index with `git rm --cached` while preserving the local files.
- The daily backup script already excludes `/opt/data/secrets/***`, `/opt/data/credentials/***`, `.env`, and files matching `*secret*`, `*token*`, `*credential*`, and `oauth*.json`.

## Important security note

Some credential files had already been tracked by Git before this cleanup. Removing them from the index prevents future backups/commits, but it does **not** erase any old GitHub history. Rotate those Google credentials if there is any chance the repository or old commits were exposed.
