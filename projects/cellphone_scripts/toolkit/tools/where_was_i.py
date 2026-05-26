"""Personal "Where Was I?" location timeline for Pythonista.

Run manually, from a Siri Shortcut, or from a Shortcuts Automation. iOS does not
allow Pythonista to run permanently in the background, so reliable tracking is
best done by asking Shortcuts to open/run this script on triggers such as time of
day, CarPlay connect/disconnect, arrival/departure, or Focus changes.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from toolkit.lib.ios_runtime import get_current_location, local_now_label, notify, utc_now_iso
from toolkit.lib.storage import JsonStore, default_data_dir


class WhereWasITracker:
    def __init__(self, store: JsonStore | None = None):
        self.store = store or JsonStore(default_data_dir() / "where_was_i.json", [])

    def log_point(
        self,
        latitude: float,
        longitude: float,
        label: str = "",
        note: str = "",
        accuracy: float | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        entries = self.store.read()
        entry = {
            "id": f"loc-{len(entries) + 1}-{int(datetime.now().timestamp())}",
            "timestamp": timestamp or utc_now_iso(),
            "local_time": local_now_label(),
            "latitude": round(float(latitude), 7),
            "longitude": round(float(longitude), 7),
            "accuracy_m": accuracy,
            "label": label.strip() or "Quick check-in",
            "note": note.strip(),
            "maps_url": f"https://maps.apple.com/?ll={float(latitude)},{float(longitude)}",
        }
        entries.append(entry)
        self.store.write(entries)
        return entry

    def log_current_location(self, label: str = "", note: str = "") -> dict[str, Any]:
        fix = get_current_location()
        entry = self.log_point(
            latitude=fix["latitude"],
            longitude=fix["longitude"],
            accuracy=fix.get("horizontal_accuracy"),
            label=label,
            note=note,
        )
        notify("Where Was I", f"Saved {entry['label']} at {entry['local_time']}")
        return entry

    def timeline_for_date(self, date_prefix: str | None = None) -> list[dict[str, Any]]:
        date_prefix = date_prefix or datetime.now().strftime("%Y-%m-%d")
        return [entry for entry in self.store.read() if entry.get("local_time", "").startswith(date_prefix)]

    def daily_summary(self, date_prefix: str | None = None) -> str:
        entries = self.timeline_for_date(date_prefix)
        if not entries:
            return "No places logged yet today."
        lines = [f"{len(entries)} places logged:"]
        for entry in entries:
            lines.append(f"- {entry['local_time']}: {entry['label']} ({entry['latitude']}, {entry['longitude']})")
        return "\n".join(lines)


def main() -> None:
    tracker = WhereWasITracker()
    print("Where Was I?\n1. Log current location\n2. Today's summary")
    choice = input("Choose: ").strip()
    if choice == "1":
        label = input("Label, optional: ")
        note = input("Note, optional: ")
        entry = tracker.log_current_location(label=label, note=note)
        print("Saved:", entry["maps_url"])
    else:
        print(tracker.daily_summary())


if __name__ == "__main__":
    main()
