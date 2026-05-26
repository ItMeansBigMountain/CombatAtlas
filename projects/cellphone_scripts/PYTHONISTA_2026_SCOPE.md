# Pythonista iOS 2026 Scope — cellphone_scripts

## Current inventory

- `requests_dataScience/` — 10 small API/demo scripts: NASA, air quality, recipes, Pokémon, VIN, memes, advice, FBI, COVID.
- `business_tools/` — 5 utility scripts: email read/send, Google reviews, interest calculator, file naming.
- `health_apps/` — 3 personal tracking scripts: mood chart, workout extraction, workout planning.
- `networking/` — 3 network/security scripts: IP geolocation, MD5 cracking, DDoS demo.
- `algos/` — 5 learning/demo scripts: sorting, distance, slope, magic squares, animation.

## Reality check

This repo is a good Pythonista-era script collection, but many scripts are still terminal-input demos. For 2026, the value is turning them into iPhone-native mini tools using Pythonista strengths: Share Sheet actions, Shortcuts launch URLs, clipboard workflows, camera/photo input, local files/iCloud, widgets-style quick launch, and small `ui` panels.

Research notes checked:

- Pythonista still exposes iOS-specific modules including `appex`, `clipboard`, `contacts`, `location`, `photos`, `reminders`, `speech`, `ui`, `scene`, `notification`, `objc_util`, and `shortcuts` in its docs.
- GitHub activity around Pythonista centers on Shortcuts integration, Markdown/share-sheet workflows, photo collage tools, local shells, backups, and iOS automation scripts.

## Best modernization direction

Build a **Pythonista Pocket Toolkit**: a folder of clean, tap-friendly scripts that run directly on iPhone/iPad and pair with Siri Shortcuts.

### Core product principles

1. One script = one obvious phone task.
2. Prefer Share Sheet input over typing.
3. Prefer local/private storage over cloud accounts.
4. Use simple `ui` screens for repeatable tools.
5. Use Shortcuts launchers for daily-use automations.
6. Remove or quarantine unsafe scripts like DDoS demos.
7. Replace hardcoded secrets with `.env.example` plus iOS Keychain guidance.

## Cool 2026 Pythonista ideas

### 1. Share Sheet AI/Text Cleanup

Take selected text from Safari, Notes, Messages, or email via Pythonista extension; clean it into summary, action items, reply draft, or markdown.

### 2. Receipt Scanner Lite

Use Share Sheet/photo input, OCR via an API or local fallback, then save merchant, total, category, and date to CSV/JSON.

### 3. Personal CRM Quick Log

From a contact or clipboard text, log follow-up notes, last-touch dates, reminders, and relationship context locally.

### 4. Mood + Habit Micro Dashboard

Modernize `DailyMoodChart.py` into a tap-first tracker with local charts, streaks, notes, and weekly reflection prompts.

### 5. Workout Companion

Modernize workout scripts into a timer, plan generator, progress tracker, and simple visual history for iPhone workouts.

### 6. Photo Batch Utility

Resize, rename, watermark, compress, strip metadata, or build collages from selected Photos via Share Sheet.

### 7. Clipboard Command Center

Detect clipboard type: URL, address, phone, text, image; offer useful actions like summarize, QR code, save, clean, or lookup.

### 8. Local Meeting Notes

Share transcript/audio text into Pythonista; produce meeting summary, tasks, names, deadlines, and local archive.

### 9. Smart File Renamer

Modernize `file_naming_convention.py` for iCloud files/photos: normalize names, dates, project tags, and client folders.

### 10. API Playground for iPhone

Turn current API demos into reusable mini cards with saved endpoints, headers, response preview, and export-to-Notes.

### 11. Meme/Microcontent Generator

Modernize meme scripts into a phone-first UI: pick template/photo, type caption, save/share immediately.

### 12. Location Context Logger

Use location module for private mileage, place notes, parking reminders, or field-work check-ins.

### 13. Personal Safety Shortcut

One-tap script logs location, timestamp, optional note/photo, and prepares a prewritten message without auto-sending.

### 14. iOS Dev Scratchpad

Small Pythonista shell/tools: JSON formatter, regex tester, hash generator, base64 encode/decode, URL parser.

### 15. Web-to-Markdown Clipper

Share a webpage into Pythonista; extract title, URL, selected text, summary, tags, and append to a markdown vault.

## Implemented first sprint: daily automation core

Created `toolkit/` with shared JSON storage, Pythonista runtime wrappers, tests, and these daily-use tools:

1. `toolkit/agent_tick.py` — Shortcuts-friendly one-shot automation runner.
2. `toolkit/launcher.py` — manual toolkit menu.
3. `toolkit/tools/where_was_i.py` — private location timeline.
4. `toolkit/tools/clipboard_history.py` — local clipboard history/search.
5. `toolkit/tools/location_reminders.py` — private geofence-style reminders.

### Next sprint candidates

1. `DailyMoodChart.py` → `mood_tracker.py`
2. `file_naming_convention.py` → `smart_renamer.py`
3. `memeGenerator.py` → `meme_studio.py`
4. Quarantine unsafe/outdated networking demos into `archive/unsafe_or_obsolete/`.

## Candidate folder structure

```text
cellphone_scripts/
  toolkit/
    launcher.py
    lib/
      storage.py
      ios_input.py
      simple_ui.py
      config.py
    tools/
      mood_tracker.py
      smart_renamer.py
      meme_studio.py
      clipboard_center.py
      receipt_logger.py
  archive/
    original_scripts/
    unsafe_or_obsolete/
  docs/
    shortcuts_setup.md
    pythonista_setup.md
```

## Priority call

The strongest customer-facing angle is not “random Python scripts.” It is: **iPhone automations you can actually run from Share Sheet, clipboard, photos, and Siri Shortcuts.**
