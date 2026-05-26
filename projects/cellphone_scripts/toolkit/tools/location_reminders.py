"""Location-based reminders for Pythonista.

This keeps a private local reminder list and checks nearby reminders whenever the
script is invoked. For background-ish behavior, create iOS Shortcuts automations
for arrival/departure/time-of-day that open this script.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from toolkit.lib.ios_runtime import get_current_location, local_now_label, notify, utc_now_iso
from toolkit.lib.storage import JsonStore, default_data_dir

EARTH_RADIUS_M = 6_371_000


def distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class LocationReminderStore:
    def __init__(self, store: JsonStore | None = None):
        self.store = store or JsonStore(default_data_dir() / "location_reminders.json", [])

    def add(
        self,
        text: str,
        latitude: float,
        longitude: float,
        radius_m: int = 200,
        place: str = "",
    ) -> dict[str, Any]:
        reminders = self.store.read()
        reminder = {
            "id": f"rem-{len(reminders) + 1}-{int(datetime.now().timestamp())}",
            "created_at": utc_now_iso(),
            "created_local": local_now_label(),
            "text": text.strip(),
            "place": place.strip() or "Saved place",
            "latitude": round(float(latitude), 7),
            "longitude": round(float(longitude), 7),
            "radius_m": int(radius_m),
            "completed": False,
        }
        reminders.append(reminder)
        self.store.write(reminders)
        return reminder

    def nearby(self, latitude: float, longitude: float) -> list[dict[str, Any]]:
        matches = []
        for reminder in self.store.read():
            if reminder.get("completed"):
                continue
            meters = distance_meters(latitude, longitude, reminder["latitude"], reminder["longitude"])
            if meters <= reminder.get("radius_m", 200):
                item = dict(reminder)
                item["distance_m"] = round(meters)
                matches.append(item)
        return sorted(matches, key=lambda item: item["distance_m"])

    def complete(self, reminder_id: str) -> bool:
        reminders = self.store.read()
        changed = False
        for reminder in reminders:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                reminder["completed_at"] = utc_now_iso()
                changed = True
        self.store.write(reminders)
        return changed

    def check_current_location(self) -> list[dict[str, Any]]:
        fix = get_current_location()
        matches = self.nearby(fix["latitude"], fix["longitude"])
        if matches:
            notify("Nearby reminder", matches[0]["text"])
        return matches


def main() -> None:
    store = LocationReminderStore()
    print("Location Reminders\n1. Add reminder at current location\n2. Check nearby reminders")
    choice = input("Choose: ").strip()
    if choice == "1":
        text = input("Reminder: ")
        place = input("Place label, optional: ")
        radius = input("Radius meters [200]: ").strip() or "200"
        fix = get_current_location()
        reminder = store.add(text, fix["latitude"], fix["longitude"], int(radius), place=place)
        print("Saved", reminder["text"])
    else:
        matches = store.check_current_location()
        if not matches:
            print("No nearby reminders.")
        for item in matches:
            print(f"{item['distance_m']}m: {item['text']} @ {item['place']}")


if __name__ == "__main__":
    main()
