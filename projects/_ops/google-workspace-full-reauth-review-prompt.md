# Review prompt — full Google Workspace + YouTube reauthorization

Use this prompt in a fresh Hermes session after Oyama approves it. **Review/audit first; do not generate OAuth URLs or alter tokens until the account/scope plan has been presented and approved.**

---

Reauthorize every Google identity used by Hermes and maintained projects with the complete permissions actually needed across our sessions. Follow the `google-workspace` skill and its user-specific references. Treat current Google documentation and live project configuration as authoritative; use session history only to reconstruct established intent and past failures.

## User authorization policy

The user has explicitly approved **full read/write Google Workspace automation for all five Workspace profiles**, including both personal accounts. Older notes saying either personal account is read-only/no-send are stale and must not narrow the requested grants.

Canonical Workspace profiles:

- `personal-main` — `affan.fareed@gmail.com`
- `personal-secondary` — `fareed320@gmail.com`
- `trapiistan` — `trapiistan@gmail.com`
- `classicalechos` — `classicalechos@gmail.com`
- `burner` — `laflametoast@gmail.com`

Canonical YouTube OAuth lanes:

- `trapiistan` — expected channel **Sosai Oyama**, `UCsxzQlusqwmMUdjMvKAJDfA`
- `classicalechos` — expected channel **Classical Echos**, `UCcIpxiU2CLEsBdHcc7_lcyA`
- `fareed320` — expected channel **A F**, `UCX_nUA3Yr9VR884DNanyMYA`

## Required audit before authorization

1. Search relevant Hermes session history for Google Workspace, Gmail, Calendar, Drive, Docs, Sheets, Contacts/People, YouTube upload/analytics, OAuth errors, scope failures, and callback handling.
2. Audit maintained projects, cron scripts, environment references, the profile registry, and every Google credential consumer. Identify the exact account, API, operation, credential class, token path, and required scope for each consumer.
3. Inspect live token metadata safely without printing access tokens, refresh tokens, client secrets, authorization codes, raw credential JSON, or private keys.
4. Keep credential classes separate:
   - Workspace user OAuth per named profile
   - YouTube user OAuth per channel
   - service accounts only for explicitly shared/delegated resources
   - API keys only for public/API-key-compatible requests
   - pytubefix/device login separate from Google API upload OAuth
5. Reconcile conflicts among memory, registry files, scripts, and old session notes in favor of the latest explicit user instruction above. Report conflicts before acting.
6. Check whether each required Google API is enabled in the OAuth client project. Distinguish project-side API enablement from token-side OAuth scopes.

## Proposed scope baseline to validate

For **each of the five Workspace profiles**, validate and propose the canonical full Workspace bundle:

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/contacts`

Do not silently add broader or unrelated scopes. If maintained consumers require additional Gmail settings, Contacts/People, Calendar, Drive, or other Google scopes, cite the exact consumer and operation and propose the smallest additional scope before authorization.

For **each YouTube lane**, validate and propose:

- `https://www.googleapis.com/auth/youtube`
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

If a project needs monetary analytics or another YouTube permission, identify the exact operation and ask before adding it.

## Review gate

Before generating links, present a compact Discord-friendly report using bold bullets, not a Markdown table:

- every profile and verified email/channel identity;
- every maintained consumer found across sessions/projects;
- current auth/health state;
- proposed scopes grouped by credential lane;
- missing APIs or scope gaps;
- conflicts/stale aliases;
- exact number of authorization links that will be generated;
- any behavior that full write permissions enable.

Then stop and request approval of the final matrix. Do not revoke existing grants first, because that can interrupt healthy consumers and is unnecessary for normal reauthorization.

## Authorization workflow after approval

1. Use `/opt/data/scripts/google_reauth_workflow.py` and `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.
2. Generate one fresh, labeled URL per approved lane with isolated PKCE pending state, `login_hint`, `access_type=offline`, and `prompt=consent select_account` (or the helper's equivalent).
3. Paste every actionable URL directly in Discord and also save a non-secret handoff at `/opt/data/HeRmEz/projects/_ops/google-oauth-reauth-current.md`.
4. Tell the user to verify the Google consent-screen account/channel. `login_hint` is not an account lock.
5. Explain that localhost failure after consent is expected. Request complete address-bar callback URLs in these forms:
   - `workspace:<profile>: <full localhost callback URL>`
   - `youtube:<profile>: <full localhost callback URL>`
6. Accept multiple labeled callbacks in one message. Exchange each callback only into its matching profile-specific token path.
7. Never expose token JSON or secrets in chat, logs, prompts, or tracked files.

## Verification after exchange

For every Workspace profile, verify the expected Gmail email plus harmless live probes for:

- Gmail profile and labels
- Calendar list
- Drive list
- Docs API access
- Sheets API access
- People/Contacts access

For every YouTube profile, verify `channels.list(mine=true)` against the expected channel title and ID, then perform non-destructive capability checks for upload/metadata/read/analytics scopes. Do not upload, send mail, modify messages, edit documents, or create events merely to test authorization.

Check granted scopes exactly, token-path permissions, durable storage, registry references, cron/script defaults, stale shared-token aliases, and accidental narrow-scope token overwrites. Update non-secret maps only after verified identity. State clearly that offline refresh tokens are long-lived but can still be revoked or expire under Google policy.

Finally, replay only the previously blocked harmless health checks. Present success/failure per profile and list any consumer still blocked. Do not report success merely because token exchange succeeded.

## User communication preferences

- Compact bold bullets in Discord; no Markdown status tables.
- Put each OAuth URL directly in chat, clearly labeled.
- Report raw failures in fenced blocks.
- Never make the user guess which Google account/channel to select.
- Audit first, authorize second, verify identity and capabilities third.

---

Cached at: `/opt/data/HeRmEz/projects/_ops/google-workspace-full-reauth-review-prompt.md`
