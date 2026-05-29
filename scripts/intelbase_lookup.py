#!/usr/bin/env python3
"""IntelBase email lookup helper.

Docs scanned:
- https://docs.intelbase.is/introduction
- https://docs.intelbase.is/llms.txt
- https://docs.intelbase.is/api-reference/introduction.md
- https://docs.intelbase.is/api-reference/endpoint/lookup_email.md
- https://docs.intelbase.is/api-reference/openapi.json

The public OpenAPI spec currently exposes one endpoint:
POST https://api.intelbase.is/lookup/email
Auth: x-api-key: <INTEL_BASE_API_KEY>

Use only for accounts you own, have consent to investigate, or are authorized
by an organization to assess. This helper does not support name-based lookups
because IntelBase's published API currently documents email lookup only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://api.intelbase.is/lookup/email"
ENV_KEY = "INTEL_BASE_API_KEY"
DEFAULT_ENV_PATHS = (Path("/opt/data/.env"), Path.home() / ".hermes" / ".env")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _load_key_from_env_files() -> str | None:
    """Best-effort fallback for gateway/cron shells that did not source .env."""
    for env_path in DEFAULT_ENV_PATHS:
        try:
            text = env_path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == ENV_KEY:
                value = value.strip().strip('"').strip("'")
                return value or None
    return None


def get_api_key() -> str:
    key = os.getenv(ENV_KEY) or _load_key_from_env_files()
    if not key:
        raise SystemExit(
            f"Missing {ENV_KEY}. Add it to /opt/data/.env or export it in the shell."
        )
    return key


def lookup_email(
    email: str,
    *,
    timeout_ms: int | None = 15000,
    include_data_breaches: bool = False,
    exclude_modules: list[str] | None = None,
) -> dict[str, Any]:
    if not EMAIL_RE.match(email):
        raise ValueError(f"Not a valid email address: {email!r}")

    payload: dict[str, Any] = {"email": email}
    if timeout_ms is not None:
        payload["timeout_ms"] = int(timeout_ms)
    if include_data_breaches:
        payload["include_data_breaches"] = True
    if exclude_modules:
        payload["exclude_modules"] = exclude_modules

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "accept": "application/json",
            "x-api-key": get_api_key(),
            "user-agent": "hermes-intelbase-helper/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=max((timeout_ms or 15000) / 1000 + 10, 15)) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = {"raw": raw}
            return {"ok": True, "status": resp.status, "data": parsed}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            detail = {"raw": raw}
        return {"ok": False, "status": exc.code, "error": detail}
    except urllib.error.URLError as exc:
        return {"ok": False, "status": None, "error": str(exc.reason)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lookup an authorized email address with IntelBase."
    )
    parser.add_argument("email", help="Email address to look up")
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Maximum IntelBase lookup time in milliseconds (default: 15000)",
    )
    parser.add_argument(
        "--include-data-breaches",
        action="store_true",
        help="Ask IntelBase to include data breach results when available",
    )
    parser.add_argument(
        "--exclude-module",
        action="append",
        default=[],
        help="IntelBase module name to exclude; repeat for multiple modules",
    )
    parser.add_argument(
        "--i-am-authorized",
        action="store_true",
        help="Required acknowledgement that the lookup is authorized/consensual",
    )
    args = parser.parse_args(argv)

    if not args.i_am_authorized:
        parser.error(
            "add --i-am-authorized after confirming this lookup is for your own "
            "account, consented, or part of an authorized security investigation"
        )

    try:
        result = lookup_email(
            args.email,
            timeout_ms=args.timeout_ms,
            include_data_breaches=args.include_data_breaches,
            exclude_modules=args.exclude_module or None,
        )
    except Exception as exc:  # Keep CLI failures machine-readable.
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
