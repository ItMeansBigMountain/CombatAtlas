# Cox Elementary PTA project backup

This directory contains a Git bundle backup of the Cox Elementary PTA website project.

- Project path: `/opt/data/HeRmEz/projects/cox-elementary-pta`
- Live URL: https://cox-elementary-pta.onrender.com/
- Admin URL: https://cox-elementary-pta.onrender.com/admin/
- Source remote at backup time: `https://github.com/ItMeansBigMountain/cox-elementary-pta.git`
- Branch at backup time: `main`
- Latest commit at backup time: `8fec5f35b0772c1074adc9a56323a1151e94e59d`
- Backup file: `cox-elementary-pta.bundle`

## Restore/check commands

```bash
# Inspect bundle
git bundle verify .hermes/project-backups/cox-elementary-pta.bundle

# Restore into a fresh folder
git clone .hermes/project-backups/cox-elementary-pta.bundle restored-cox-elementary-pta
cd restored-cox-elementary-pta
git log -1 --oneline
```

The bundle stores the Git history and source code. Runtime files such as local SQLite DBs, media uploads, caches, and nested .git internals are not tracked as separate parent-repo files.
