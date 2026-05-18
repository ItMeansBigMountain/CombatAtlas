# Credentials Status

Updated: 2026-05-17

Do not store real credentials in Git. Real local values are in ignored `.env` files only.

## Local `.env` files created

- `MusicAI/.env` — Spotify, Genius OAuth credentials, Imgflip credentials, Flask local settings. Watson values still blank.
- `RTS-JS-ChatRooms/.env` — Agora App ID and primary certificate, Flask local settings.

Both files are ignored by Git and set to owner-only permissions (`0600`).

## Still needed

### Genius

The MusicAI code currently expects `GENIUS_API_KEY`, which is the **Genius Client Access Token**, not just OAuth client ID/secret.

To get it:

1. Go to <https://genius.com/api-clients>
2. Open the app/client.
3. Copy the **Client Access Token**.
4. Put it into `GENIUS_API_KEY` locally and into deployment environment variables later.

The OAuth client ID/secret are saved locally too in case we wire OAuth back in, but the current code path uses direct bearer-token access.

### IBM Watson NLU

Needed values:

- `WATSON_API_KEY`
- `WATSON_SERVICE_URL`

How to retrieve:

1. Go to <https://cloud.ibm.com/resources>
2. Open the Natural Language Understanding service instance.
3. Click **Manage** or **Service credentials**.
4. Copy `apikey` into `WATSON_API_KEY`.
5. Copy `url` into `WATSON_SERVICE_URL`.

If there is no service instance, create one from IBM Cloud Catalog → Natural Language Understanding, then create service credentials.

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
