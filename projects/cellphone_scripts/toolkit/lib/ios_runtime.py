"""Shared iOS/Pythonista compatibility helpers.

Pythonista modules are imported lazily so this project can still be tested on a
normal computer. When running on iPhone, these wrappers use Pythonista's native
clipboard, location, notifications, reminders, and app-extension APIs.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def local_now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_clipboard_text() -> str:
    try:
        import clipboard  # type: ignore

        value = clipboard.get()
        return value if isinstance(value, str) else ""
    except Exception:
        return ""


def set_clipboard_text(text: str) -> None:
    try:
        import clipboard  # type: ignore

        clipboard.set(text)
    except Exception:
        pass


def get_current_location() -> dict[str, Any]:
    """Return current GPS fix in Pythonista; raises with a helpful message elsewhere."""
    try:
        import location  # type: ignore

        location.start_updates()
        try:
            fix = location.get_location() or {}
        finally:
            location.stop_updates()
        if not fix:
            raise RuntimeError("No location fix returned")
        return fix
    except Exception as exc:
        raise RuntimeError(
            "Current location requires Pythonista on iOS with Location permission enabled."
        ) from exc


def notify(title: str, message: str) -> None:
    try:
        import notification  # type: ignore

        notification.schedule(message=message, title=title, delay=0)
    except Exception:
        print(f"{title}: {message}")


def get_share_text() -> str:
    try:
        import appex  # type: ignore

        if appex.is_running_extension():
            text = appex.get_text()
            if text:
                return text
            url = appex.get_url()
            if url:
                return str(url)
    except Exception:
        pass
    return get_clipboard_text()
