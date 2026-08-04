#!/usr/bin/env python3
"""Deprecated compatibility entry point for OAuth callback exchange.

Delegates every callback to the canonical verifier. This file intentionally has
no token-writing or scope logic of its own.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

WORKFLOW = Path("/opt/data/scripts/google_reauth_workflow.py")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=("workspace", "youtube"))
    ap.add_argument("profile")
    ap.add_argument("callback", help="Complete localhost callback URL")
    args = ap.parse_args()
    command = f"{args.kind}-exchange"
    return subprocess.run(
        [sys.executable, str(WORKFLOW), command, args.profile, args.callback],
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
