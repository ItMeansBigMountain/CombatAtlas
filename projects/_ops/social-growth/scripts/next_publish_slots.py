#!/usr/bin/env python3
"""Generate near-term viral-test publish windows in local time.

Default timezone is America/Chicago for the user's Texas/US audience assumption.
This script is intentionally dependency-free so content projects can call it from
cron/jobs without installing a scheduler library.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from zoneinfo import ZoneInfo

WINDOWS = {
    "youtube_shorts": [(14, 16), (20, 22)],
    "tiktok": [(19, 21), (7, 9)],
    "instagram_reels": [(11, 13), (19, 21)],
}

PREFERRED_DAYS = {
    "youtube_shorts": {1, 2, 3, 4, 5, 6, 7},
    "tiktok": {1, 2, 3, 4, 5, 6},
    "instagram_reels": {1, 2, 3, 4, 5, 6, 7},
}

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def next_slots(platform: str, count: int, tz_name: str, start: dt.datetime | None = None) -> list[dict]:
    tz = ZoneInfo(tz_name)
    now = start.astimezone(tz) if start else dt.datetime.now(tz)
    slots: list[dict] = []
    day = now.date()
    while len(slots) < count:
        weekday = day.isoweekday()
        if weekday in PREFERRED_DAYS[platform]:
            for start_hour, end_hour in WINDOWS[platform]:
                when = dt.datetime.combine(day, dt.time(start_hour, 0), tzinfo=tz)
                if when <= now:
                    continue
                slots.append({
                    "platform": platform,
                    "local_time": when.isoformat(),
                    "day": DAY_NAMES[weekday - 1],
                    "window": f"{start_hour:02d}:00-{end_hour:02d}:00",
                    "timezone": tz_name,
                    "cohort": f"{platform}:{DAY_NAMES[weekday - 1]}:{start_hour:02d}",
                })
                if len(slots) >= count:
                    break
        day += dt.timedelta(days=1)
    return slots


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--platform", choices=sorted(WINDOWS), default="youtube_shorts")
    p.add_argument("--count", type=int, default=7)
    p.add_argument("--timezone", default="America/Chicago")
    p.add_argument("--all", action="store_true", help="Emit slots for every platform")
    args = p.parse_args()

    if args.all:
        payload = {platform: next_slots(platform, args.count, args.timezone) for platform in sorted(WINDOWS)}
    else:
        payload = next_slots(args.platform, args.count, args.timezone)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
