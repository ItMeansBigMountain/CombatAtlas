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

Copy `.env.example` to `.env` for local overrides. Do not commit `.env`, local SQLite databases, virtualenvs, caches, or build artifacts.
