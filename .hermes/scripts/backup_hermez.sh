#!/usr/bin/env bash
set -euo pipefail

REPO="/opt/data/HeRmEz"
SRC="/opt/data"
BACKUP_DIR="$REPO/.hermes"
PROJECTS_DIR="$REPO/projects"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ ! -d "$REPO/.git" ]; then
  echo "ERROR: $REPO is not a git repository" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR" "$PROJECTS_DIR"

git -C "$REPO" fetch origin --prune >/dev/null 2>&1 || true
if git -C "$REPO" rev-parse --verify origin/main >/dev/null 2>&1; then
  git -C "$REPO" merge --ff-only origin/main >/dev/null 2>&1 || true
fi

# Sanitize Hermes home into the repo. This intentionally excludes secrets,
# credentials, runtime locks/pids, nested git metadata, and the repo itself to
# avoid recursive backups. Prefer rsync when available; otherwise use a Python
# fallback so the cron job works on minimal containers.
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude='/HeRmEz/***' \
    --exclude='/.env' \
    --exclude='/.env.*' \
    --include='/.env.*.template' \
    --exclude='/.git-credentials' \
    --exclude='/.gitconfig' \
    --exclude='/auth.json' \
    --exclude='/auth.lock' \
    --exclude='**/*secret*' \
    --exclude='**/*token*' \
    --exclude='**/*credential*' \
    --exclude='**/oauth*.json' \
    --exclude='**/keyring*' \
    --exclude='**/*.pem' \
    --exclude='**/*.key' \
    --exclude='**/*.p12' \
    --exclude='**/*.pfx' \
    --exclude='**/id_rsa*' \
    --exclude='**/id_ed25519*' \
    --exclude='*.lock' \
    --exclude='*.pid' \
    --exclude='*.sock' \
    --exclude='**/.tick.lock' \
    --exclude='**/__pycache__/***' \
    --exclude='**/.pytest_cache/***' \
    --exclude='**/.mypy_cache/***' \
    --exclude='**/.ruff_cache/***' \
    --exclude='**/node_modules/***' \
    --exclude='**/.git/***' \
    "$SRC/" "$BACKUP_DIR/"
else
  python3 - <<'PY'
import fnmatch
import os
import shutil
from pathlib import Path

src = Path('/opt/data')
dst = Path('/opt/data/HeRmEz/.hermes')

exclude_exact = {'.env', '.git-credentials', '.gitconfig', 'auth.json', 'auth.lock'}
exclude_dir_names = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'node_modules'}
exclude_file_globs = [
    '.env.*', '*secret*', '*token*', '*credential*', 'oauth*.json', 'keyring*',
    '*.pem', '*.key', '*.p12', '*.pfx', 'id_rsa*', 'id_ed25519*',
    '*.lock', '*.pid', '*.sock', '.tick.lock',
]
include_names = {'.env.discord.template'}

if dst.exists():
    shutil.rmtree(dst)
dst.mkdir(parents=True, exist_ok=True)

for root, dirs, files in os.walk(src):
    rootp = Path(root)
    rel = rootp.relative_to(src)
    if rel.parts and rel.parts[0] == 'HeRmEz':
        dirs[:] = []
        continue
    dirs[:] = [d for d in dirs if d not in exclude_dir_names]
    target_dir = dst / rel
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        if name in include_names:
            pass
        elif name in exclude_exact or any(fnmatch.fnmatch(name, pat) for pat in exclude_file_globs):
            continue
        source = rootp / name
        target = target_dir / name
        try:
            if source.is_symlink():
                linkto = os.readlink(source)
                if target.exists() or target.is_symlink():
                    target.unlink()
                os.symlink(linkto, target)
            else:
                shutil.copy2(source, target)
        except FileNotFoundError:
            # File changed/disappeared during backup; skip it.
            continue
PY
fi

cat > "$BACKUP_DIR/BACKUP_MANIFEST.md" <<EOF
# Hermes home backup manifest

Last backup: $STAMP
Source: /opt/data
Destination: /opt/data/HeRmEz/.hermes

This is a sanitized snapshot. Excluded intentionally:

- /opt/data/HeRmEz itself, to avoid recursive backups
- .env, .git-credentials, .gitconfig
- auth.json and auth.lock
- OAuth/keyring files
- files whose names contain secret, token, or credential
- private key material (*.pem, *.key, *.p12, *.pfx, id_rsa*, id_ed25519*)
- runtime locks, pids, sockets, and common cache/build directories
- nested .git directories

Future project folders should live under /opt/data/HeRmEz/projects.
EOF

mkdir -p "$REPO/scripts"
cp -p "$0" "$REPO/scripts/backup_hermez.sh"

if ! git -C "$REPO" config user.email >/dev/null; then
  git -C "$REPO" config user.email 'hermes-agent@local'
fi
if ! git -C "$REPO" config user.name >/dev/null; then
  git -C "$REPO" config user.name 'Hermes Agent'
fi

cd "$REPO"

git add .gitignore README.md .hermes projects scripts/backup_hermez.sh

if git diff --cached --quiet; then
  echo "HeRmEz backup complete: no changes to commit at $STAMP"
  exit 0
fi

COMMIT_MSG="chore: automated HeRmEz backup $STAMP"
git commit -m "$COMMIT_MSG" >/dev/null

git push origin main >/dev/null

HEAD_SHA="$(git rev-parse HEAD)"
REMOTE_SHA="$(git ls-remote --heads origin main | awk '{print $1}')"
if [ "$HEAD_SHA" != "$REMOTE_SHA" ]; then
  echo "ERROR: pushed backup but remote SHA mismatch" >&2
  echo "local=$HEAD_SHA" >&2
  echo "remote=$REMOTE_SHA" >&2
  exit 1
fi

echo "HeRmEz backup complete and pushed: $HEAD_SHA at $STAMP"
