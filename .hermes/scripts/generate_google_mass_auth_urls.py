#!/usr/bin/env python3
"""Compatibility wrapper for the canonical Google/YouTube OAuth workflow.

Do not define scopes here. All maintained authorization URLs must come from
/opt/data/scripts/google_reauth_workflow.py so scope policy cannot drift.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

WORKFLOW = Path("/opt/data/scripts/google_reauth_workflow.py")


def run(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(WORKFLOW), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def main() -> None:
    print(json.dumps({
        "workspace": run("workspace-auth-url", "--all"),
        "youtube": run("youtube-auth-url", "--all"),
        "canonical_workflow": str(WORKFLOW),
    }, indent=2))


if __name__ == "__main__":
    main()
