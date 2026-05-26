"""Tiny JSON persistence helpers for Pythonista-friendly scripts.

The code intentionally sticks to the Python standard library so it runs in
Pythonista without pip installs. Tests run on desktop Python too.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStore:
    """Read/write a JSON document at a stable path."""

    def __init__(self, path: str | Path, default: Any | None = None):
        self.path = Path(path)
        self.default = [] if default is None else default

    def read(self) -> Any:
        if not self.path.exists():
            return _copy_default(self.default)
        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write(self, value: Any) -> Any:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False, sort_keys=True)
        tmp.replace(self.path)
        return value


def _copy_default(value: Any) -> Any:
    return json.loads(json.dumps(value))


def default_data_dir() -> Path:
    """Return a local data directory that works in Pythonista and desktop tests."""
    return Path(__file__).resolve().parents[2] / "data"
