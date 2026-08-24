#!/usr/bin/env python3
"""Fail closed when the HeRmEz backup stage contains unsafe/generated content."""
from __future__ import annotations
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = Path("/opt/data/HeRmEz")
MAX_BLOB = 50 * 1024 * 1024
DENIED_PARTS = {
    "node_modules", ".next", ".nuxt", ".terraform", ".terragrunt-cache",
    ".vercel", ".angular", ".turbo", ".parcel-cache", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv",
    "dist", "build", "coverage", "obj", "test-results",
}
DENIED_PREFIXES = (
    ".hermes/home/", ".hermes/.nuget/", ".hermes/.dotnet/",
    ".hermes/kanban/workspaces/", ".hermes/sandboxes/",
    "projects/_tmp/",
)
SECRET_NAME = re.compile(
    r"(^|/)(\.env($|\.)|auth\.json$|auth\.lock$|.*(?:secret|token|credential).*|oauth.*\.json$|.*\.(?:pem|p12|pfx)$|id_(?:rsa|ed25519).*)",
    re.I,
)
ALLOWED_SECRET_NAMES = re.compile(r"(^|/)\.env(?:\..+)?\.(?:example|template)$|(^|/)\.env\.example$")
DENIED_SUFFIXES = (".db", ".db-wal", ".db-shm", ".sqlite", ".sqlite3", ".pyc", ".tsbuildinfo")


def run(*args: str, text: bool = False):
    return subprocess.check_output(args, cwd=REPO, text=text)


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return [p.decode("utf-8", "surrogateescape") for p in raw.split(b"\0") if p]


def staged_size(path: str) -> int:
    raw = run("git", "cat-file", "-s", f":{path}", text=True).strip()
    return int(raw)


def verify_sanitized_config(errors: list[str]) -> None:
    """Reject credential material in the Git-backed config snapshot."""
    path = ".hermes/config.yaml"
    try:
        raw = run("git", "show", f":{path}", text=True)
    except subprocess.CalledProcessError:
        return
    try:
        import yaml
        data = yaml.safe_load(raw) or {}
    except Exception as exc:
        errors.append(f"cannot parse staged sanitized config: {exc}")
        return
    basic = ((data.get("dashboard") or {}).get("basic_auth") or {})
    for key in ("password", "password_hash", "secret"):
        if str(basic.get(key) or "").strip():
            errors.append(f"dashboard credential present in sanitized config: dashboard.basic_auth.{key}")


def main() -> int:
    errors: list[str] = []
    verify_sanitized_config(errors)
    for path in staged_paths():
        parts = set(Path(path).parts)
        lower = path.lower()
        if any(path.startswith(prefix) for prefix in DENIED_PREFIXES):
            errors.append(f"generated/runtime prefix: {path}")
        if parts & DENIED_PARTS:
            errors.append(f"generated dependency/build path: {path}")
        if lower.endswith(DENIED_SUFFIXES):
            errors.append(f"runtime database/cache suffix: {path}")
        if SECRET_NAME.search(path) and not ALLOWED_SECRET_NAMES.search(path):
            errors.append(f"secret-like filename: {path}")
        try:
            size = staged_size(path)
        except subprocess.CalledProcessError:
            continue
        if size > MAX_BLOB:
            errors.append(f"blob exceeds 50 MiB ({size} bytes): {path}")
    if errors:
        print("ERROR: HeRmEz backup stage rejected:", file=sys.stderr)
        for err in sorted(set(errors)):
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("HeRmEz backup stage verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
