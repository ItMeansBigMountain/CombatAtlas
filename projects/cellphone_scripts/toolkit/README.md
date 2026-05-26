# Pythonista Pocket Toolkit

This folder turns `cellphone_scripts` into a small iPhone automation toolkit for Pythonista.

## Important iOS reality

Pythonista cannot run as a silent, permanent background daemon on iOS. Apple limits third-party background execution and clipboard/location access. The reliable pattern is:

1. Keep tiny scripts that do useful work fast.
2. Trigger them with Siri Shortcuts automations.
3. Let each run record a snapshot, then exit.

That gives you "background-ish" personal software without fighting iOS.

## New tools

### `toolkit/agent_tick.py`

One-shot automation runner. It:

- logs current location to the Where Was I timeline,
- captures current clipboard into private history,
- checks nearby location reminders,
- sends a notification if a reminder is nearby.

Use this for Shortcuts automations.

### `toolkit/tools/where_was_i.py`

Private location timeline. Great for:

- "Where was I today?"
- remembering errands, parking, visits, job sites,
- building a personal location diary without a social app.

Data file: `toolkit/data/where_was_i.json`

### `toolkit/tools/clipboard_history.py`

Private clipboard history. Great for:

- saving useful links/text you copied,
- searching prior clipboard items,
- classifying URLs, JSON-like text, emails, and tracking-number-like strings.

Data file: `toolkit/data/clipboard_history.json`

### `toolkit/tools/location_reminders.py`

Private geofence-style reminders. Great for:

- "when I am at the store, remind me to buy X",
- "when I get near school, remind me about PTA item",
- "when I am near home, remind me to bring something inside."

Data file: `toolkit/data/location_reminders.json`

### `toolkit/launcher.py`

Manual menu launcher for all tools.

## Shortcuts setup ideas

Create iOS Shortcuts automations that run/open Pythonista scripts:

- **Time of Day**: run `agent_tick.py` every morning, lunch, afternoon, evening.
- **CarPlay/Bluetooth disconnect**: run `where_was_i.py` or `agent_tick.py` to remember parking/context.
- **Arrive/Leave**: run `agent_tick.py` when arriving/leaving home, school, work, gym, store.
- **Focus Mode starts/stops**: run `agent_tick.py` during work, sleep, driving, or family routines.
- **Action Button / Back Tap**: run `launcher.py` or `where_was_i.py` manually.
- **Share Sheet**: send selected text/URLs into `clipboard_history.py`.

If using Pythonista URL schemes, the shape is usually:

```text
pythonista3://toolkit/agent_tick.py?action=run
pythonista3://toolkit/launcher.py?action=run
pythonista3://toolkit/tools/where_was_i.py?action=run
```

You can also use Shortcuts' "Open App" / "Open URLs" actions depending on your Pythonista setup.

## Privacy posture

Everything is local JSON by default. No cloud sync, no external API, and no account required.

## Desktop test command

From `cellphone_scripts/`:

```bash
python3 -m unittest discover -s tests -v
```
