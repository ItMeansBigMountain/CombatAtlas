# Canonical YouTube Upload Method for Hermes Projects

This is now the shared upload pattern for all HeRmEz YouTube automation projects.

## Canonical credential locations

Secrets live outside git:

```text
/opt/data/secrets/youtube-main/youtube_client_secret.json
/opt/data/secrets/youtube-main/youtube_upload_token.json
/opt/data/secrets/youtube-main/youtube_oauth_pending.json
```

The token was verified with `youtube.upload` scope and a private YouTube API smoke test.

## Canonical scripts

Use these shared scripts from any YouTube project:

```bash
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py
```

## Upload command

Private-first is the default. For any generated MP4:

```bash
python3 /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py \
  /absolute/path/to/final.mp4 \
  --title "Video Title" \
  --description "Description" \
  --tags "discipline,self improvement,faceless" \
  --privacy private
```

Dry-run before real upload:

```bash
python3 /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py \
  /absolute/path/to/final.mp4 \
  --title "Video Title" \
  --privacy private \
  --dry-run
```

## When a new/expired credential is needed

1. Create Google OAuth Client ID: **Web application**.
2. Enable **YouTube Data API v3**.
3. Add redirect URI:

```text
http://localhost:5000/
```

4. Save client JSON to:

```text
/opt/data/secrets/youtube-main/youtube_client_secret.json
```

5. Generate auth URL:

```bash
python3 /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py auth-url
```

6. User opens link, approves, then pastes the full `http://localhost:5000/?code=...` URL.
7. Exchange it:

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 python3 /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py exchange 'FULL_LOCALHOST_URL'
```

8. Verify:

```bash
python3 /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py check
```

## Rules

- Never commit client secrets, tokens, or returned localhost OAuth URLs.
- First uploads are always `private` unless explicitly told otherwise.
- Private uploads do not require a separate approval step; the user will make videos public manually after review.
- Each automation project can render videos locally, but upload should go through this shared method.
- If Google says `deleted_client`, stop retrying old tokens and run a fresh OAuth flow.
- If exchange says `Missing code verifier`, regenerate a fresh auth URL with the current script; old codes cannot be reused.
