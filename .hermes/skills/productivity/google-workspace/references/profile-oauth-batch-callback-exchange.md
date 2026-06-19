# Profile OAuth batch callback exchange and verification

Use this when the user returns multiple Google OAuth `localhost` callback URLs in one message or text file.

## Pattern

1. Generate fresh profile-scoped auth URLs with `/opt/data/scripts/google_profile_oauth.py auth-url <profile>` immediately before asking for callbacks. Old pending PKCE state may be stale.
2. Ask the user to return callbacks in `profile: http://localhost:1/?code=...&state=...` form. If they upload a text file, parse each block by profile name and the next `http://localhost:1/` URL.
3. Exchange each callback with:

```bash
python3 /opt/data/scripts/google_profile_oauth.py auth-code <profile> '<full callback url>'
```

4. Confirm all pending files are cleared:

```bash
python3 /opt/data/scripts/google_profile_oauth.py list
```

5. Verify each token with harmless live probes:
   - Gmail `users.getProfile` returns the expected email.
   - Gmail `labels.list` succeeds.
   - Calendar `calendarList.list(maxResults=1)` succeeds.
   - Drive `files.list(pageSize=1)` succeeds.

6. Preserve the user-specific policy:
   - `personal-main` / `affan.fareed@gmail.com`: Gmail read-only only; full Calendar/Drive/Docs/Sheets/Contacts.
   - Other automation identities: full Workspace bundle.

## Pitfalls

- Do not force refresh with a superset of scopes that the token was not granted; use the token's stored `scopes` for refresh, then probe APIs. Forcing extra scopes can produce `invalid_scope` even when the token is usable for its granted capabilities.
- `login_hint` is not an account lock. Always verify returned Gmail email matches the expected profile.
- A restored legacy token may be sufficient for a narrow pipeline, but if the profile policy calls for full Workspace, generate a fresh full-scope URL and exchange it when the user provides the callback.
- A browser failure at `http://localhost:1` is expected in headless OAuth. The full address-bar URL is the artifact needed for exchange.
