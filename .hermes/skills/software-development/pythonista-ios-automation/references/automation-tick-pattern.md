# Pythonista Automation Tick Pattern

Use this when a user asks for Pythonista software that is "always running", "constantly tracking", or "autonomous" on iPhone.

## Reality Check

Pythonista scripts cannot run as permanent background daemons on iOS. Do not promise a 24/7 process. iOS may suspend apps quickly and background execution is limited to system-approved capabilities.

## Durable Workaround

Build a **one-shot agent tick** script and have Siri Shortcuts / iOS Automations launch it at useful trigger points. Each run should:

1. Import iOS-only modules lazily so desktop tests still run.
2. Read local JSON state.
3. Capture quick context, e.g. location, clipboard, timestamp, battery/focus if available.
4. Evaluate reminders/rules/geofences.
5. Write local JSON state.
6. Notify only when useful.
7. Exit quickly.

Good trigger ideas:

- Time of day / hourly-ish schedule
- Arrive at or leave a location
- CarPlay/Bluetooth connect or disconnect
- Focus Mode changes
- Charger connect/disconnect
- Action Button, Back Tap, widget, or manual launcher
- Share Sheet captures for explicit user-provided input

## Recommended File Shape

```text
toolkit/
  agent_tick.py              # one-shot automation entrypoint
  launcher.py                # manual menu
  lib/
    storage.py               # JSON persistence
    ios_runtime.py           # lazy wrappers for location/clipboard/notification
  tools/
    where_was_i.py
    clipboard_history.py
    location_reminders.py
  data/
    *.json                   # local/private state; gitignored if personal
```

## Testing Pattern

Keep pure logic testable on desktop:

- Use dependency injection for providers such as current location, clipboard text, and current time.
- Lazy-import `location`, `clipboard`, and `notification` in wrapper functions instead of at module import time.
- Store state in local JSON files and allow test-specific temp storage paths.
- Unit-test deduplication, geofence distance, and state updates without requiring iOS.

## Pitfalls

- Do not frame the workaround as truly continuous background execution.
- Do not create infinite loops or sleep-based daemons for Pythonista; they will be unreliable and battery-hostile.
- Do not log secrets, tokens, or sensitive clipboard content to external services.
- Do not require non-stdlib packages unless the user confirms Pythonista has them installed.
