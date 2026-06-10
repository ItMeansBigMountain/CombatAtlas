# Legacy Django API setup

This folder is the legacy Django runtime candidate for journal-ai. The repository root is currently plan/documentation only; run backend validation from this directory.

## Local validation

Use a local virtual environment and install only the checked dependency manifest:

```bash
cd legacy-src/persistent-gpt-api
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements.txt
python3 manage.py check
python3 manage.py test
```

If `uv` is not available, create a venv with Python and use pip inside that venv:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py test
```

## Environment split

Local development defaults are intentionally safe enough for `manage.py check`:

- `APP_ENV=development` by default.
- `DEBUG` defaults to `true` locally and `false` when `APP_ENV=production`.
- `SECRET_KEY` falls back to a development placeholder locally, but is required in production.
- `ALLOWED_HOSTS` defaults to `localhost,127.0.0.1`; set it explicitly for production/tunnel hosts.
- SQLite defaults to `db.sqlite3`; override with `SQLITE_PATH` if needed.
- `CSRF_TRUSTED_ORIGINS`, `SECURE_SSL_REDIRECT`, secure cookie flags, and optional HSTS settings are environment-driven for production hosts.

## Vercel deployment

The backend includes a Vercel Python runtime entrypoint at `api/index.py` and routes all traffic through it via `vercel.json`.

Required Vercel environment variables:

- `APP_ENV=production`
- `SECRET_KEY=<long random Django secret>`
- `ALLOWED_HOSTS=.vercel.app,your-custom-domain.example` (or the exact Vercel host)
- `CSRF_TRUSTED_ORIGINS=https://your-project.vercel.app` (plus any custom domains)

Recommended production variables:

- `SECURE_SSL_REDIRECT=true`
- `SESSION_COOKIE_SECURE=true`
- `CSRF_COOKIE_SECURE=true`
- `SECURE_HSTS_SECONDS=31536000` after confirming the production domain is HTTPS-only

Smoke-test after deploy:

```bash
curl -fsS https://your-project.vercel.app/healthz/
```

Expected response:

```json
{"status":"ok","service":"journal-ai-api"}
```
