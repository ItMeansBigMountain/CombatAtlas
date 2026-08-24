#!/usr/bin/env python3
"""Launch the dashboard with protected env-file credentials.

This avoids shell expansion of scrypt hashes and explicitly removes any stale
plaintext password inherited from the container environment.
"""
from pathlib import Path
import os

ENV_PATH = Path("/opt/data/.env")
for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    os.environ[key] = value
os.environ.pop("HERMES_DASHBOARD_BASIC_AUTH_PASSWORD", None)
os.environ["HOME"] = "/opt/data"
os.execv(
    "/opt/hermes/.venv/bin/hermes",
    [
        "/opt/hermes/.venv/bin/hermes",
        "dashboard",
        "--host",
        "127.0.0.1",
        "--port",
        "4860",
        "--no-open",
    ],
)
