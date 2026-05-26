"""One-shot automation runner for iOS Shortcuts.

This is the closest reliable pattern to "always-on" Pythonista software on iOS:
Shortcuts triggers open/run this script, and each invocation records location,
captures clipboard, and checks nearby reminders.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from toolkit.lib.ios_runtime import get_clipboard_text, get_current_location, notify
from toolkit.lib.storage import JsonStore, default_data_dir
from toolkit.tools.clipboard_history import ClipboardHistory
from toolkit.tools.location_reminders import LocationReminderStore
from toolkit.tools.where_was_i import WhereWasITracker

LocationProvider = Callable[[], dict[str, Any]]
ClipboardProvider = Callable[[], str]
NotifyFunc = Callable[[str, str], None]


def run_tick(
    data_dir: str | Path | None = None,
    location_provider: LocationProvider = get_current_location,
    clipboard_provider: ClipboardProvider = get_clipboard_text,
    notify_func: NotifyFunc = notify,
) -> dict[str, Any]:
    base = Path(data_dir) if data_dir is not None else default_data_dir()
    tracker = WhereWasITracker(JsonStore(base / "where_was_i.json", []))
    clips = ClipboardHistory(JsonStore(base / "clipboard_history.json", []))
    reminders = LocationReminderStore(JsonStore(base / "location_reminders.json", []))

    result: dict[str, Any] = {
        "location_logged": False,
        "clipboard_captured": None,
        "nearby_reminders": [],
        "errors": [],
    }

    current_fix = None
    try:
        current_fix = location_provider()
        tracker.log_point(
            latitude=current_fix["latitude"],
            longitude=current_fix["longitude"],
            accuracy=current_fix.get("horizontal_accuracy"),
            label="Automatic check-in",
        )
        result["location_logged"] = True
    except Exception as exc:  # pragma: no cover - depends on iOS permissions
        result["errors"].append(f"location: {exc}")

    try:
        captured = clips.capture(clipboard_provider(), source="automation_tick")
        result["clipboard_captured"] = captured
    except Exception as exc:  # pragma: no cover
        result["errors"].append(f"clipboard: {exc}")

    if current_fix:
        nearby = reminders.nearby(current_fix["latitude"], current_fix["longitude"])
        result["nearby_reminders"] = nearby
        if nearby:
            notify_func("Nearby reminder", nearby[0]["text"])

    return result


def main() -> None:
    result = run_tick()
    print("Pocket Toolkit tick complete")
    print("Location logged:", result["location_logged"])
    if result["clipboard_captured"]:
        print("Clipboard:", result["clipboard_captured"]["preview"])
    for item in result["nearby_reminders"][:5]:
        print(f"Nearby: {item['text']} ({item['distance_m']}m)")
    if result["errors"]:
        print("Errors:", "; ".join(result["errors"]))


if __name__ == "__main__":
    main()
