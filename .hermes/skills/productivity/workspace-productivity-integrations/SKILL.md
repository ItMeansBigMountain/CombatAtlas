---
name: workspace-productivity-integrations
description: "Use when operating productivity/workspace systems such as Airtable, Notion, Obsidian, maps/geocoding, or Teams meeting pipelines. Umbrella for data, notes, location, and meeting automations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, airtable, notion, obsidian, maps, teams, automation]
    related_skills: [google-workspace, operator-morning-reports]
---

# Workspace Productivity Integrations

## Overview

Use this umbrella when the task is to read, write, synchronize, or summarize information in a productivity system. It consolidates workspace data tools, note systems, location utilities, and meeting-summary pipelines into one discoverable entry point.

## Choose the Integration

| User intent | Integration |
|---|---|
| CRUD structured records, filters, upserts | Airtable |
| Manage pages/databases/blocks | Notion |
| Search/create/edit local markdown notes | Obsidian |
| Geocode, find POIs, routes, time zones | Maps/OSM/OSRM |
| Operate Teams meeting summary pipeline | Teams meeting pipeline |

## Operating Rules

1. Identify the target workspace/database/vault/location/pipeline before writing.
2. Prefer read/preview operations before destructive updates.
3. Preserve source identifiers: record IDs, page IDs, note paths, coordinates, route endpoints, meeting IDs.
4. For writes, summarize the exact target and fields/content changed.
5. For recurring reports, make output delta-oriented and concise.

## Re-homed Playbooks

Former tool-specific skills are preserved as references:

- `references/airtable/original-skill.md` — Airtable REST CRUD, filtering, and upsert patterns.
- `references/notion/original-skill.md` plus block-type references for Notion pages/databases.
- `references/obsidian/original-skill.md` — Obsidian vault search, note creation, and edits.
- `references/maps/original-skill.md` plus map client script for geocoding, POI, routing, and time zones.
- `references/teams-meeting-pipeline/original-skill.md` — Teams meeting summary pipeline operation.

## Pitfalls

- Do not guess IDs for workspace writes; discover or ask when the target cannot be retrieved.
- Do not overwrite rich document structures when a block/record-level patch is safer.
- Do not treat geocoding/routing results as exact without noting provider/source and ambiguity.
- Do not expose credentials or tokens in reports.

## Verification Checklist

- [ ] Target workspace/object/location was resolved.
- [ ] Read-before-write was performed for stateful changes.
- [ ] Write operations report object IDs and changed fields/paths.
- [ ] Location results include enough coordinates/source detail to reproduce.
- [ ] Meeting/report outputs distinguish transcript facts from generated summaries.
