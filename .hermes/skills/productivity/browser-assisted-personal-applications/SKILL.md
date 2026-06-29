---
name: browser-assisted-personal-applications
description: "Use when helping the user find, evaluate, and apply to real-world personal services or programs via the browser: local clinics/programs, intake forms, appointments, memberships, applications, and similar web forms."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [browser, applications, forms, local-search, intake, appointments]
---

# Browser-Assisted Personal Applications

## Overview

Use this skill when the user asks Hermes to start, apply for, sign up for, schedule, or otherwise operate a personal real-world service through websites. The goal is to actively use browser/web tools to find the best official intake path, identify requirements, gather only needed information, and submit only after explicit confirmation.

## Workflow

1. **Localize first.** If the service depends on location, search using the user's current stated city/suburb and nearby metro. Do not assume old location context; accept mid-turn corrections immediately and pivot.
2. **Prefer official program/provider pages.** Use official application/intake pages over directory pages, SEO articles, or patient-facing pages meant for recipients rather than applicants.
3. **Compare nearby options briefly.** Capture the nearest credible option and one fallback, especially when one location is closer but has stricter eligibility or a weaker application flow.
4. **Open the application form before asking for data.** Inspect form fields/placeholders so the user only has to provide the exact required fields.
5. **Summarize requirements before submission.** List eligibility constraints, location/visit frequency, compensation/costs if shown, and contact info.
6. **Ask for explicit submit permission.** Filling fields may be okay after the user provides data, but do not submit personal, medical, financial, legal, or identity-related applications without a final confirmation.
7. **Protect sensitive data.** Do not save completed form contents or personal medical details in memory/skills. Store only reusable workflow notes or public provider quirks.

## Browser/Form Tactics

- If search-engine browser navigation hits bot detection, use `web_search` for discovery, then navigate directly to the official result.
- If button clicks do not visibly navigate, inspect anchors with browser console, e.g. list link text/hrefs, then navigate directly to the real URL.
- On forms where the accessibility tree hides labels, inspect `input`, `textarea`, and `select` placeholders/names/ids to derive the field list.
- If a page is for consumers/patients rather than applicants/donors/workers, keep searching for "become", "apply", "donor application", "intake", or "provider application" pages.

## Safety and Consent

- Treat medical, fertility, identity, financial, and employment-adjacent forms as sensitive.
- Never infer sensitive answers such as age, height, medical history, citizenship, sexual history, or health status.
- Never submit a form just because the user said "start"; collect the required fields and obtain explicit confirmation right before the submit click.
- If eligibility criteria may exclude the user, present them neutrally and let the user decide whether to proceed.

## References

- `references/sperm-donor-program-intake.md` — notes from a Chicago-suburbs sperm donor program search and form-inspection pattern.

## Verification Checklist

- [ ] Official/local provider page found.
- [ ] Eligibility and logistics summarized from the page.
- [ ] Form fields inspected rather than guessed.
- [ ] User supplied all required personal fields.
- [ ] Explicit final confirmation obtained before submitting.
- [ ] Contact info or application URL given if not submitted.
