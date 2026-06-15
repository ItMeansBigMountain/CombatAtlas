# personal-main read-only OAuth repair pattern

Use this when `personal-main` / `affan.fareed@gmail.com` loses context or a token refresh fails with `invalid_scope`.

## Durable account policy

`personal-main` is a read-only context account unless the user explicitly changes policy. Reauth should request only:

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/drive.readonly`
- `https://www.googleapis.com/auth/documents.readonly`
- `https://www.googleapis.com/auth/spreadsheets.readonly`
- `https://www.googleapis.com/auth/contacts.readonly`

Do not repair this account by granting Gmail send/modify, full Calendar, or full Drive scopes.

## Helper-script pitfalls

If using `/opt/data/scripts/google_profile_oauth.py`:

- The current profile registry may use `workspace_profiles`, not the older `profiles` key. The helper should accept both.
- Scope selection should be profile-aware: `personal-main` or `access: read_only_workspace` gets the read-only bundle; other automation identities get the full Workspace bundle.
- Generate the URL with `prompt=consent` and `login_hint=affan.fareed@gmail.com`.
- Store pending PKCE state under `/opt/data/google_profiles/personal-main/pending.json` and exchange into `/opt/data/google_profiles/personal-main/google_token.json`.

## Exchange and verification

1. Generate the auth URL for `personal-main`.
2. User opens it, confirms the consent-screen email is `affan.fareed@gmail.com`, approves, and pastes the full `http://localhost:1/?code=...&scope=...` redirect URL.
3. Exchange with the profile-scoped helper, preserving the returned scopes.
4. Verify live identity and read-only API reachability:
   - Gmail `users.getProfile(userId='me')` returns `affan.fareed@gmail.com`.
   - Calendar list succeeds.
   - Drive list succeeds.
   - Docs and Sheets service construction/discovery succeeds.
   - People/Contacts readonly probe succeeds.

Report compactly in Discord as bold bullets; do not paste tokens, refresh tokens, client secrets, or raw credential JSON.
