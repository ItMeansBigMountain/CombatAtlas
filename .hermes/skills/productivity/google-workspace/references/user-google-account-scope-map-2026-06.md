# User Google account scope map and mass OAuth refresh — 2026-06

Use this reference when the user asks to refresh Google tokens, map accounts, or avoid repeated re-auth prompts across Gmail/Calendar/Drive/Docs/Sheets/YouTube automation.

## User communication preference

- In Discord replies, do **not** present account/scope status as Markdown tables. The user explicitly said tables look terrible/unreadable in Discord.
- Use bold bullets and short nested bullets instead.
- Be concrete: account → purpose → scopes/token path → next action.

## Account map

- **personal-secondary = fareed320@gmail.com**
  - Full Workspace automation.
  - Source inbox for newsletters and faceless YouTube scripts.
  - Can read, label, archive/trash processed source emails, send if needed, and use Calendar/Drive/Docs/Sheets.
  - Canonical token: `/opt/data/google_profiles/personal-secondary/google_token.json`.
  - Legacy alias may exist: `/opt/data/google_profiles/fareed320 -> /opt/data/google_profiles/personal-secondary`.

- **trapiistan = trapiistan@gmail.com**
  - Hermes main Workspace account.
  - Owns/updates the content calendar for video schedules and automation reports.
  - Also has YouTube OAuth for the **Sosai Oyama** channel.
  - Workspace token: `/opt/data/google_profiles/trapiistan/google_token.json`.
  - YouTube token: `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`.

- **classicalechos = classicalechos@gmail.com**
  - Content/channel account.
  - Owns the **Classical Echos** YouTube channel and recent faceless uploads.
  - Workspace token: `/opt/data/google_profiles/classicalechos/google_token.json`.
  - YouTube token: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`.
  - Current shared default YouTube uploader token may be copied from this token when Classical Echos is the active channel.

- **burner = laflametoast@gmail.com**
  - Burner/disposable Google account.
  - Full Workspace automation allowed.
  - Token: `/opt/data/google_profiles/burner/google_token.json`.

- **personal-main = affan.fareed@gmail.com**
  - Read-only only.
  - Do not request or use write scopes for this account unless the user explicitly changes the policy.
  - Token: `/opt/data/google_profiles/personal-main/google_token.json`.

## Workspace scopes

For full automation accounts, request:

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/contacts.readonly`

For `personal-main` / `affan.fareed@gmail.com`, request read-only equivalents only:

- `gmail.readonly`
- `calendar.readonly`
- `drive.readonly`
- `documents.readonly`
- `spreadsheets.readonly`
- `contacts.readonly`

## YouTube scopes

For YouTube automation accounts, request:

- `https://www.googleapis.com/auth/youtube.upload` — upload videos.
- `https://www.googleapis.com/auth/youtube.force-ssl` — edit video metadata/status/privacy/captions/comments; required to change existing videos from private to public.
- `https://www.googleapis.com/auth/youtube.readonly` — verify channel/video ownership and public/private status.
- `https://www.googleapis.com/auth/yt-analytics.readonly` — performance loop and self-improving content analytics.

Do not rely on `youtube.upload` alone if the workflow needs to edit privacy/metadata after upload.

## Mass refresh workflow

1. Generate one auth URL per identity and token family; never overwrite all accounts into a single token.
2. Store Workspace pending state under `/opt/data/google_profiles/<profile>/google_oauth_pending.json`.
3. Store YouTube pending state under `/opt/data/secrets/youtube-<profile>/youtube_oauth_pending.json`.
4. Include `login_hint`, but still tell the user to verify the selected consent-screen account/channel; `login_hint` is not a hard lock.
5. Ask the user to return the full localhost redirect URLs labeled by account.
6. Exchange redirects into their dedicated token paths.
7. Verify live, without printing secrets:
   - Gmail: `users.getProfile` returns expected email.
   - Calendar: list a small sample of calendars.
   - YouTube: `channels.list(mine=true)` returns expected channel title and ID.
   - YouTube video correction: `videos.list(part=snippet,status,id=...)` can see target videos before attempting updates.
8. Write/update a non-secret account map in the workspace, e.g. `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.

## Operational pitfalls

- YouTube uploads are channel-specific. If a token can upload but cannot see/edit an existing video ID, the user likely authenticated the wrong channel/account. Re-auth with the owning channel selected.
- YouTube `publishAt` represents a scheduled future public release as `privacyStatus=private` until publish time. The user prefers not to upload as private by default, so prefer cron/calendar-triggered public uploads unless native YouTube scheduled release is explicitly requested.
- Gmail `gmail.modify` lets the agent trash messages after verified processing; permanent deletion requires broader Gmail scope and is usually unnecessary.
- For newsletter video source cleanup, delete/trash only after a verified YouTube `video_id` is returned.
