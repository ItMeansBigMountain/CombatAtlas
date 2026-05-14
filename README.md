# HeRmEz

This repo is the working home for Hermes-managed projects on this machine.

Local layout:

- `.hermes/` - sanitized backup snapshot of the Hermes home at `/opt/data`.
- `projects/` - place new project folders here going forward.

Security note: local secrets and credentials are intentionally excluded from git by `.gitignore` and by the backup sync rules. Examples: `.env`, `auth.json`, `.git-credentials`, private keys, tokens, lock files, and runtime pids.
