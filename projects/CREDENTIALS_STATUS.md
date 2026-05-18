# Credentials Status

Updated: 2026-05-17

Do not store real credentials in Git. Real local values are in ignored `.env` files only.

## Local `.env` files created

- `MusicAI/.env` — Spotify, Genius OAuth credentials, Imgflip credentials, Flask local settings. Watson values still blank.
- `RTS-JS-ChatRooms/.env` — Agora App ID and primary certificate, Flask local settings.

Both files are ignored by Git and set to owner-only permissions (`0600`).

## Still needed

### Genius

Received and stored locally:

- Genius OAuth client ID/secret
- Genius Client Access Token as `GENIUS_API_KEY`

The MusicAI code currently uses `GENIUS_API_KEY` / Client Access Token for direct bearer-token API access.

### IBM Watson NLU / LLM replacement

Watson is still not configured.

Current blank local values:

- `WATSON_API_KEY`
- `WATSON_SERVICE_URL`

Preferred path now: replace Watson NLU sentiment/lyric analysis with an LLM fallback, likely OpenAI.

Local placeholders added to `MusicAI/.env`:

- `OPENAI_API_KEY=`
- `LLM_SENTIMENT_PROVIDER=openai`

Still needed if we use OpenAI:

- `OPENAI_API_KEY`

Implementation note: refactor MusicAI so Watson analysis is optional. If `WATSON_API_KEY` and `WATSON_SERVICE_URL` are absent but `OPENAI_API_KEY` is present, call the LLM sentiment analyzer instead. If neither exists, use deterministic/demo sentiment output so the app still deploys.

## Spotify redirect URL

For local development, the current MusicAI code/docs expect exactly:

```text
http://localhost:5000/login/
```

Add that as a redirect URI in the Spotify Developer Dashboard now.

For production, after we deploy MusicAI, add the production callback too:

```text
https://<musicai-vercel-or-host-domain>/login/
```

If we deploy on a different port/path or adjust the Flask route, the redirect must match exactly, including trailing slash.

## Agora notes

Agora App ID can be visible in client JavaScript. The primary certificate must stay server-side only. For production, generate short-lived Agora tokens server-side instead of exposing the certificate to browser code.
