# HeRmEz

HeRmEz is the workspace repository for this Hermes Agent environment.
It is intended to be the home base for:

- backing up the local Hermes configuration/state in a sanitized form
- creating and organizing new project folders
- testing that GitHub push/pull works from this machine

## Repository location

Local path:

```text
/opt/data/HeRmEz
```

Remote:

```text
https://github.com/ItMeansBigMountain/HeRmEz.git
```

Hermes has been configured so future terminal work starts in this repo:

```text
terminal.cwd: /opt/data/HeRmEz
```

## Layout

```text
HeRmEz/
├── .hermes/              # Sanitized backup snapshot of the Hermes home
├── projects/             # New project folders should go here
├── .gitignore            # Prevents obvious secrets/runtime files from being committed
└── README.md             # This file
```

## Using this repo for projects

Create each new project as a subfolder under `projects/`:

```text
/opt/data/HeRmEz/projects/my-new-project
```

That keeps Hermes configuration backups and active project work in one GitHub-backed workspace.

## Hermes backup notes

The `.hermes/` folder is a sanitized snapshot of the local Hermes home at `/opt/data`.
It is meant for recoverability and visibility, not for publishing secrets.

The backup intentionally excludes common sensitive or volatile files, including:

- `.env`
- `.git-credentials`
- `auth.json`
- private keys
- files with `secret`, `token`, or `credential` in the filename
- lock files
- pid files
- nested `.git` directories

See `.hermes/BACKUP_MANIFEST.md` for details about the backup snapshot.

## Quick health check

From this repository, these commands should work:

```bash
git status --short --branch
git pull --ff-only
git push
```

If this README appears on GitHub, then clone, commit, and push are working.

## Current purpose

This README was updated by Hermes Agent as a simple end-to-end test that local file edits, git commits, and GitHub pushes are working correctly.
