# Backup cache history cleanup for oversized Git pushes

Use this when a backup/workspace repo starts tracking generated caches or SDK installs, and GitHub rejects a push even after adding `.gitignore` and `git rm --cached`.

## Trigger symptoms

- `remote: warning: File ... is larger than GitHub's recommended maximum file size of 50.00 MB`
- `remote: error: File ... exceeds GitHub's file size limit of 100.00 MB`
- Large files appear in local commits that have not successfully pushed yet.

## Safe sequence for unpublished local commits

1. Add or tighten `.gitignore` for the generated/runtime paths.
2. Update the backup script's copy/exclude logic so the paths do not reappear on the next cron run.
3. Remove already-tracked generated files from the index, preserving local files on disk:

   ```bash
   git rm -r --cached --ignore-unmatch \
     .hermes/.gradle .hermes/.local .hermes/.expo .hermes/jdks .hermes/tmp \
     .hermes/bin .hermes/cache .hermes/lsp .hermes/logs .hermes/sessions \
     .hermes/audio_cache .hermes/state-snapshots .hermes/ibmcloud-cli \
     .hermes/hermes-agent .hermes/credentials .hermes/secrets \
     .hermes/models_dev_cache.json
   ```

4. Commit the ignore/script cleanup.
5. If push is still rejected, the large blobs are in earlier unpushed commits. Preserve a local backup branch first:

   ```bash
   git branch backup/pre-ignore-cleanup-$(date +%Y%m%d%H%M%S) HEAD
   ```

6. Rewrite only the local range that is ahead of the remote, removing the generated paths from every unpublished commit:

   ```bash
   export FILTER_BRANCH_SQUELCH_WARNING=1
   git filter-branch --force --index-filter '
     git rm -r --cached --ignore-unmatch \
       .hermes/.gradle .hermes/.local .hermes/.expo .hermes/jdks .hermes/tmp \
       .hermes/bin .hermes/cache .hermes/lsp .hermes/logs .hermes/sessions \
       .hermes/audio_cache .hermes/state-snapshots .hermes/ibmcloud-cli \
       .hermes/hermes-agent .hermes/credentials .hermes/secrets \
       .hermes/models_dev_cache.json >/dev/null 2>&1 || true
   ' --prune-empty origin/main..main
   ```

7. Verify no large objects remain in the unpushed range:

   ```bash
   python3 - <<'PY'
   import subprocess
   objs = subprocess.check_output(['git','rev-list','--objects','origin/main..HEAD']).decode('utf-8','ignore').splitlines()
   large = []
   for line in objs:
       oid = line.split()[0]
       path = ' '.join(line.split()[1:]) if ' ' in line else ''
       try:
           size = int(subprocess.check_output(['git','cat-file','-s',oid]).decode())
       except Exception:
           continue
       if size > 50 * 1024 * 1024:
           large.append((size, path, oid))
   for size, path, oid in sorted(large, reverse=True):
       print(f'{size/1024/1024:.1f} MiB {oid} {path}')
   print('large_count', len(large))
   PY
   ```

8. Push and verify remote head:

   ```bash
   git push origin main
   git ls-remote --heads origin main
   ```

9. Run the backup script once manually and verify it does not re-add ignored paths:

   ```bash
   /opt/data/scripts/backup_hermez.sh
   git check-ignore -v .hermes/sessions/x .hermes/jdks/temurin11.tar.gz
   git ls-files -z .hermes | xargs -0 -r du -ch | tail -1
   ```

## Pitfalls

- `.gitignore` only prevents future additions; it does not remove blobs already in commits.
- `git rm --cached` in the latest commit can still leave rejected blobs in earlier unpublished commits.
- Rewrite only unpublished local commits such as `origin/main..main`; do not rewrite shared remote history unless the user explicitly accepts the risk.
- Preserve a local branch before history rewriting so recovery is easy.
- After fixing ignore rules, update the backup script too, or the next backup run may recreate the bloat.
