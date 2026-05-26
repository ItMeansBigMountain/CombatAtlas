# cellphone_scripts

## Overview

This repository contains Python scripts for Pythonista on iOS. It now includes a modern **Pythonista Pocket Toolkit** focused on daily iPhone automation.

## Source

- **Remote URL:** https://github.com/ItMeansBigMountain/cellphone_scripts.git
- **Default Branch:** main

## Current structure

- `toolkit/` — new Pythonista Pocket Toolkit.
  - `agent_tick.py` — one-shot automation runner for Shortcuts triggers.
  - `launcher.py` — manual menu for the toolkit.
  - `tools/where_was_i.py` — private location timeline.
  - `tools/clipboard_history.py` — private clipboard history/search.
  - `tools/location_reminders.py` — local location-based reminders.
  - `lib/` — shared storage and Pythonista/iOS wrappers.
- `health_apps/` — original mood/workout scripts.
- `business_tools/` — original email, file naming, review, and finance utilities.
- `requests_dataScience/` — original API playground demos.
- `networking/` — original networking/security demos; review before running.
- `algos/` — original algorithm learning scripts.
- `tests/` — desktop regression tests for the toolkit core.

## Important iOS background limitation

Pythonista cannot run as a silent always-on background daemon on iOS. Apple limits third-party background execution, location polling, and clipboard polling.

The practical 2026 pattern is **automation ticks**:

1. Siri Shortcuts triggers Pythonista at useful moments.
2. `toolkit/agent_tick.py` logs location, captures clipboard, checks reminders, then exits.
3. Local JSON files become your private history.

Recommended triggers:

- time-of-day automations,
- arrival/departure automations,
- CarPlay/Bluetooth connect or disconnect,
- Focus Mode changes,
- Action Button / Back Tap manual launch,
- Share Sheet captures.

## New daily-use tools

### Where Was I

Logs private location check-ins with timestamp, label, note, coordinates, and Apple Maps URL.

```text
toolkit/tools/where_was_i.py
```

### Clipboard History

Captures clipboard/share-sheet text, dedupes entries, classifies common text types, and supports search.

```text
toolkit/tools/clipboard_history.py
```

### Location Reminders

Stores local reminders tied to latitude/longitude/radius and checks nearby reminders during automation ticks.

```text
toolkit/tools/location_reminders.py
```

### Automation Tick

Runs all three together for Shortcuts-style background-ish behavior.

```text
toolkit/agent_tick.py
```

Pythonista URL examples:

```text
pythonista3://toolkit/agent_tick.py?action=run
pythonista3://toolkit/launcher.py?action=run
pythonista3://toolkit/tools/where_was_i.py?action=run
```

## Dependencies

- Python standard library for core logic and tests.
- Pythonista iOS modules when running on-device: `location`, `clipboard`, `notification`, `appex`.

## Tests

Run from this folder:

```bash
python3 -m unittest discover -s tests -v
```

## Project notes

See also:

- `PYTHONISTA_2026_SCOPE.md`
- `toolkit/README.md`
