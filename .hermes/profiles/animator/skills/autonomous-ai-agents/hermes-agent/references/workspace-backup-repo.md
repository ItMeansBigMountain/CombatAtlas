# Workspace backup repo pattern

Use this when a user wants a GitHub repo to become the durable Hermes workspace/home for future projects and a backup location for Hermes state.

Pattern used successfully:

1. Clone the target repo under the Hermes home, e.g. `/opt/data/<RepoName>`.
2. Create a predictable layout:
   - `<repo>/.hermes/` for a sanitized snapshot of Hermes home/state.
   - `<repo>/projects/` for future project folders.
3. Add a repo-level `.gitignore` before staging anything. Exclude secrets and volatile runtime files:
   - `.env`, `.env.*` except templates/examples.
   - `.git-credentials`, `.gitconfig`.
   - `auth.json`, auth locks, OAuth/keyring files.
   - private keys (`*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, etc.).
   - names containing `secret`, `token`, or `credential`.
   - `*.lock`, `*.pid`, sockets, caches, nested `.git/`.
4. Sync Hermes home into `<repo>/.hermes/` with `rsync -a --delete`, excluding the repo itself to avoid recursion and applying the same secret/volatile excludes.
5. Add a small backup manifest inside `<repo>/.hermes/BACKUP_MANIFEST.md` describing source, destination, and exclusions.
6. Verify before commit:
   - `git status --short`
   - scan suspicious filenames and check whether they are ignored.
   - optional content grep for common key/token patterns; treat placeholder examples in skills/docs as non-secrets after inspection.
7. Set Hermes default terminal cwd to the repo if the user wants future work to happen there:
   - `hermes config set terminal.cwd /absolute/path/to/repo`
   - verify by reading the `terminal.cwd` line from config.
8. Commit and push.
9. If the user wants a simple end-to-end GitHub verification, expand/update the repo `README.md`, commit it with a docs commit, push, and verify `git ls-remote --heads origin main` matches local `git rev-parse HEAD`. This confirms local file edits, commits, and remote pushes are working without touching secrets or runtime state.
10. Save durable memory that future project folders belong under `<repo>/projects`.
11. If the user wants recurring backups, create a deterministic backup script under the Hermes scripts directory (e.g. `/opt/data/scripts/backup_<repo>.sh`, which corresponds to `~/.hermes/scripts/` when `HERMES_HOME=/opt/data`). The script should:
    - sync the sanitized Hermes home into `<repo>/.hermes/` with the same exclusions,
    - update `<repo>/.hermes/BACKUP_MANIFEST.md` with a UTC timestamp,
    - copy itself into `<repo>/scripts/` so the automation is visible in GitHub,
    - commit only if `git diff --cached` is non-empty,
    - push to `origin main`, then compare `git rev-parse HEAD` with `git ls-remote --heads origin main`.
12. Schedule the recurring backup with Hermes cron using a relative script name, not an absolute path, e.g. `cronjob(action="create", schedule="0 3 * * *", script="backup_<repo>.sh", no_agent=true, deliver="origin")`. Run the script once immediately before relying on the schedule.

Pitfalls:

- Do not blindly commit `.env`, `auth.json`, `.git-credentials`, private keys, or runtime locks/pids.
- Exclude the destination repo from the backup sync; otherwise the backup recursively copies itself.
- Empty GitHub repos may show `origin/main [gone]` after clone; an initial commit and push establishes `main` normally.
- If Python `yaml` is missing, verify simple config values by reading/grepping the YAML text instead of adding a dependency just for verification.
- Hermes cron script paths must be relative to `~/.hermes/scripts/`; absolute paths are rejected. Put the runnable script in the Hermes scripts directory and pass only the filename.
- Prefer `rsync -a --delete` for the sync, but include a Python fallback in committed/scheduled backup scripts so the job works in minimal containers where `rsync` is not installed.
