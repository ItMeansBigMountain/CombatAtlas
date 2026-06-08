# Google OAuth Scope Status

Last checked: 2026-06-07

## Current multi-profile OAuth tokens

Profiles stored under `/opt/data/google_profiles/<profile>/google_token.json`:

- `hermes-agent` → `trapiistan@gmail.com`
- `personal-main` → `Affan.fareed@gmail.com`
- `personal-secondary` → `fareed320@gmail.com`
- `classicalechos` → `classicalechos@gmail.com`
- `burner` → `laflametoast@gmail.com`

## Current granted scopes

All five profiles currently have these Google Workspace scopes:

- Gmail readonly/send/modify
- Calendar
- Drive
- Contacts readonly
- Docs
- Sheets

## Live smoke-test result

Working across all five profiles:

- Gmail profile + labels
- Calendar list
- Drive list
- Docs API discovery
- Sheets API discovery
- People/Contacts connections probe

## Reauth guidance

No reauth needed for the current morning-review Workspace use cases: Gmail, Calendar, Drive, Docs, Sheets, Contacts.

Reauth IS needed before using new user-private APIs that were not in the original consent scope set, especially:

- YouTube channel uploads: `https://www.googleapis.com/auth/youtube.upload`
- YouTube private/channel management or analytics/reporting scopes
- Google Tasks
- Google Meet operations
- Classroom
- Cloud Search
- BigQuery / Cloud Storage user-level operations

Public API-key reads may not require OAuth, but private account/channel actions do.

## Account policy

- Personal accounts are read-first. Do not send emails on personal-main or personal-secondary unless the user explicitly approves the exact message.
- `hermes-agent` is the default on-behalf account for agent-owned Google/YouTube work.
- `classicalechos` requires review before content/account use.
- `burner` is for low-stakes miscellaneous signups/free trials.
