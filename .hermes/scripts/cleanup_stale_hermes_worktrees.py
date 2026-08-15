#!/usr/bin/env python3
"""Safely remove abandoned Hermes temporary Git worktrees.

Default is audit-only. ``--apply`` removes only allowlisted /tmp directory prefixes
older than the grace period and never removes active, mounted, held, or non-directory
paths. Persistent /opt/data cache worktrees are monitor-only.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Iterable

TMP_ROOT = Path("/tmp")
CACHE_ROOT = Path("/opt/data/.cache")
LOCK_PATH = Path("/tmp/hermes-stale-worktree-cleanup.lock")
TMP_PREFIXES = (
    "hermez-reconcile.",
    "hermez-dmm-restore-publish",
    "hermez-bis-archive-publish",
    "hermez-restore-publish",
    "hermez-plugin-hub-publish",
)
CACHE_PREFIXES = (
    "hermez-parent-push",
    "hermez-barrage-cleanup",
    "hermez-pr-pointer-publish",
    "hermez-pointer-publish",
    "hermez-cwb-publish",
)
KEEP_MARKER = ".hermes-keep"
DEFAULT_MIN_AGE_HOURS = 48
HIGH_RSS_BYTES = 750 * 1024 * 1024
STALE_PROCESS_HOURS = 24
DEV_PROCESS_MARKERS = ("pyright", "tsserver", "gradle", "runelite", "language-server")


def has_allowed_prefix(name: str, prefixes: tuple[str, ...]) -> bool:
    return any(name == prefix or name.startswith(prefix) for prefix in prefixes)


def path_age_hours(path: Path, now: float | None = None) -> float:
    now = time.time() if now is None else now
    return max(0.0, (now - path.stat().st_mtime) / 3600)


def proc_references() -> set[Path]:
    refs: set[Path] = set()
    proc = Path("/proc")
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        for leaf in ("cwd", "root"):
            try:
                refs.add((entry / leaf).resolve(strict=True))
            except (FileNotFoundError, PermissionError, OSError):
                pass
        fd_dir = entry / "fd"
        try:
            fds = list(fd_dir.iterdir())
        except (FileNotFoundError, PermissionError, OSError):
            continue
        for fd in fds:
            try:
                refs.add(fd.resolve(strict=True))
            except (FileNotFoundError, PermissionError, OSError):
                pass
    return refs


def contains_reference(path: Path, refs: Iterable[Path]) -> bool:
    resolved = path.resolve(strict=True)
    for ref in refs:
        try:
            ref.relative_to(resolved)
            return True
        except ValueError:
            continue
    return False


def is_mount(path: Path) -> bool:
    return os.path.ismount(path)


def allocated_bytes(path: Path) -> int:
    total = 0
    for root, dirs, files in os.walk(path, followlinks=False):
        try:
            total += os.lstat(root).st_blocks * 512
        except OSError:
            pass
        for name in files:
            try:
                total += os.lstat(Path(root) / name).st_blocks * 512
            except OSError:
                pass
    return total


def classify(path: Path, min_age_hours: int, refs: set[Path], now: float | None = None) -> tuple[bool, str]:
    try:
        if path.parent.resolve() != TMP_ROOT.resolve():
            return False, "outside_tmp_root"
        if not has_allowed_prefix(path.name, TMP_PREFIXES):
            return False, "prefix_not_allowed"
        if path.is_symlink() or not path.is_dir():
            return False, "not_real_directory"
        if (path / KEEP_MARKER).exists():
            return False, "keep_marker"
        if is_mount(path):
            return False, "mountpoint"
        if path_age_hours(path, now) < min_age_hours:
            return False, "within_grace_period"
        if contains_reference(path, refs):
            return False, "active_process_reference"
    except (FileNotFoundError, PermissionError, OSError) as exc:
        return False, f"inspection_error:{type(exc).__name__}"
    return True, "stale_allowlisted_worktree"


def disk_status(path: Path = Path("/opt/data")) -> dict[str, int]:
    usage = shutil.disk_usage(path)
    percent = round((usage.used * 100) / usage.total)
    return {"total": usage.total, "used": usage.used, "free": usage.free, "percent": percent}


def stale_high_memory_processes() -> list[dict]:
    """Report, but never kill, old development processes with unusually high RSS."""
    findings: list[dict] = []
    try:
        uptime = float(Path("/proc/uptime").read_text().split()[0])
        ticks = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
    except (OSError, ValueError):
        return findings
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            stat = (entry / "stat").read_text().split()
            age_hours = max(0.0, (uptime - (int(stat[21]) / ticks)) / 3600)
            status = (entry / "status").read_text()
            rss_kib = int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmRSS:")))
            cmdline = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
        except (FileNotFoundError, PermissionError, OSError, ValueError, StopIteration):
            continue
        lowered = cmdline.lower()
        if (
            rss_kib * 1024 >= HIGH_RSS_BYTES
            and age_hours >= STALE_PROCESS_HOURS
            and any(marker in lowered for marker in DEV_PROCESS_MARKERS)
        ):
            findings.append({
                "pid": int(entry.name),
                "rss_bytes": rss_kib * 1024,
                "age_hours": round(age_hours, 1),
                "command": cmdline[:300],
                "action": "alert_only",
            })
    return sorted(findings, key=lambda item: item["rss_bytes"], reverse=True)


def discover(root: Path, prefixes: tuple[str, ...]) -> list[Path]:
    try:
        return sorted(
            p for p in root.iterdir()
            if has_allowed_prefix(p.name, prefixes)
        )
    except FileNotFoundError:
        return []


def run(apply: bool, min_age_hours: int, now: float | None = None) -> dict:
    refs = proc_references()
    removed: list[dict] = []
    candidates: list[dict] = []
    skipped: list[dict] = []
    for path in discover(TMP_ROOT, TMP_PREFIXES):
        eligible, reason = classify(path, min_age_hours, refs, now)
        record = {"path": str(path), "reason": reason}
        if eligible:
            record["bytes"] = allocated_bytes(path)
            candidates.append(record)
            if apply:
                shutil.rmtree(path)
                removed.append(record)
        else:
            skipped.append(record)

    monitored_cache = []
    for path in discover(CACHE_ROOT, CACHE_PREFIXES):
        try:
            monitored_cache.append({
                "path": str(path),
                "bytes": allocated_bytes(path) if path.is_dir() and not path.is_symlink() else 0,
                "age_hours": round(path_age_hours(path), 1),
                "action": "monitor_only",
            })
        except OSError as exc:
            monitored_cache.append({"path": str(path), "error": type(exc).__name__, "action": "monitor_only"})

    return {
        "mode": "apply" if apply else "dry-run",
        "grace_hours": min_age_hours,
        "disk": disk_status(),
        "candidates": candidates,
        "removed": removed,
        "skipped": skipped,
        "persistent_cache_monitored": monitored_cache,
        "stale_high_memory_processes": stale_high_memory_processes(),
    }


def should_emit(result: dict) -> bool:
    return bool(
        result["removed"]
        or result["candidates"]
        or result["disk"]["percent"] >= 80
        or result["stale_high_memory_processes"]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="remove eligible paths")
    parser.add_argument("--min-age-hours", type=int, default=DEFAULT_MIN_AGE_HOURS)
    parser.add_argument("--verbose", action="store_true", help="print healthy/no-op results too")
    args = parser.parse_args()
    if args.min_age_hours < 24:
        parser.error("minimum grace period is 24 hours")

    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        result = run(args.apply, args.min_age_hours)

    if args.verbose or should_emit(result):
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
