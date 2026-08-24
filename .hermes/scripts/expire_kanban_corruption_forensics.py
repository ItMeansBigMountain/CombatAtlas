#!/usr/bin/env python3
"""Expire Kanban corruption snapshots after a healthy quiet period.

Safety gates:
- only files directly under /opt/data matching kanban.db.corrupt.*.bak or
  kanban.db.corrupt.current;
- live /opt/data/kanban.db must pass SQLite quick_check;
- no corruption snapshot may be newer than the quiet-period cutoff;
- no candidate may be open by any process;
- dry-run unless --apply is supplied;
- append immutable metadata (name, size, mtime, SHA-256, integrity result)
  to a JSONL forensic ledger before unlinking.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import glob
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path("/opt/data")
LIVE_DB = ROOT / "kanban.db"
LEDGER = ROOT / "forensics" / "kanban-corruption" / "expired-manifest.jsonl"
LOCK = ROOT / "forensics" / "kanban-corruption" / ".expiry.lock"
PATTERNS = ("kanban.db.corrupt.*.bak", "kanban.db.corrupt.current")


def quick_check(path: Path) -> str:
    try:
        # immutable=1 prevents SQLite from creating -wal/-shm sidecars while
        # inspecting quarantined snapshots whose header requests WAL mode.
        con = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True, timeout=2)
        try:
            row = con.execute("PRAGMA quick_check").fetchone()
            return str(row[0]) if row else "no result"
        finally:
            con.close()
    except Exception as exc:
        return f"ERROR: {exc}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def open_paths() -> set[Path]:
    found: set[Path] = set()
    proc = Path("/proc")
    for pid in proc.iterdir():
        if not pid.name.isdigit():
            continue
        fd_dir = pid / "fd"
        try:
            fds = list(fd_dir.iterdir())
        except OSError:
            continue
        for fd in fds:
            try:
                found.add(Path(os.path.realpath(fd)))
            except OSError:
                pass
    return found


def candidates() -> list[Path]:
    result: set[Path] = set()
    for pattern in PATTERNS:
        result.update(Path(p) for p in glob.glob(str(ROOT / pattern)))
    return sorted(p for p in result if p.is_file() and p.parent == ROOT)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="delete eligible files")
    parser.add_argument("--retention-days", type=int, default=30)
    parser.add_argument("--now", type=float, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.retention_days < 7:
        print("REFUSED: retention must be at least 7 days", file=sys.stderr)
        return 2

    LOCK.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with LOCK.open("a+") as lock_handle:
        try:
            fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0

        live_status = quick_check(LIVE_DB)
        if live_status != "ok":
            print(f"REFUSED: live Kanban database is not healthy: {live_status}", file=sys.stderr)
            return 1

        files = candidates()
        if not files:
            return 0
        now = args.now if args.now is not None else dt.datetime.now(dt.timezone.utc).timestamp()
        cutoff = now - args.retention_days * 86400
        newest = max(p.stat().st_mtime for p in files)
        if newest > cutoff:
            # A recent incident keeps the entire forensic set until the board has
            # remained healthy for one full retention window.
            return 0

        opened = open_paths()
        eligible = [p for p in files if p.stat().st_mtime <= cutoff]
        busy = [p for p in eligible if p.resolve() in opened]
        if busy:
            print("REFUSED: corruption snapshots are open: " + ", ".join(p.name for p in busy), file=sys.stderr)
            return 1

        records = []
        for path in eligible:
            stat = path.stat()
            records.append({
                "expired_at": dt.datetime.fromtimestamp(now, dt.timezone.utc).isoformat(),
                "retention_days": args.retention_days,
                "path": str(path),
                "name": path.name,
                "size": stat.st_size,
                "mtime": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).isoformat(),
                "sha256": sha256(path),
                "quick_check": quick_check(path),
                "live_db_quick_check": live_status,
            })

        total = sum(r["size"] for r in records)
        if not args.apply:
            print(json.dumps({"mode": "dry-run", "eligible": len(records), "bytes": total, "retention_days": args.retention_days}))
            return 0

        LEDGER.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with LEDGER.open("a", encoding="utf-8") as ledger:
            os.chmod(LEDGER, 0o600)
            for record in records:
                ledger.write(json.dumps(record, sort_keys=True) + "\n")
            ledger.flush()
            os.fsync(ledger.fileno())

        deleted = 0
        for record in records:
            path = Path(record["path"])
            # Re-check parent and exact prefix immediately before unlink.
            if path.parent == ROOT and (path.name == "kanban.db.corrupt.current" or (path.name.startswith("kanban.db.corrupt.") and path.name.endswith(".bak"))):
                path.unlink()
                deleted += 1
        print(json.dumps({"deleted": deleted, "bytes": total, "ledger": str(LEDGER), "retention_days": args.retention_days}))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
