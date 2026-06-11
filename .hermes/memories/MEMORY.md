User workspace repo is /opt/data/HeRmEz (GitHub ItMeansBigMountain/HeRmEz); create projects under /opt/data/HeRmEz/projects. Hermes Agent git install is /opt/data/hermes-agent with launcher /opt/data/.local/bin/hermes; /opt/hermes is legacy/root-owned.
§
A daily HeRmEz backup cron job exists: job_id cfcea697da5c, name "Daily HeRmEz GitHub backup", schedule "0 3 * * *", script backup_hermez.sh in /opt/data/scripts, no_agent true, backing up /opt/data into /opt/data/HeRmEz/.hermes and pushing to origin/main.
§
Hermes Kanban is consolidated to the canonical default board for the user's main workspace. DB path is /opt/data/kanban.db; current-board file is /opt/data/kanban/current with value "default". Use the default board for active HeRmEz project work; old hermez and nous-kanban-demo boards were removed after backup.
§
Email workflow: audit all 5 Google profiles via API; extract TLDR/Daily Stoic/Kinobody newsletters for video ideas, schedule drafts on Google Calendar, then delete. No tables in reports—use bold/italics/bullets. Morning report 8:30‑9 AM CST, concise, 14‑day challenge removed.
§
Cox Elementary PTA dynamic Django site is deployed at https://cox-elementary-pta.onrender.com from repo /opt/data/HeRmEz/projects/cox-elementary-pta.
§
Cox Elementary PTA project backup is stored as a Git bundle at /opt/data/HeRmEz/projects/_backups/cox-elementary-pta/cox-elementary-pta.bundle with restore notes in that folder's README.md.
§
Hermes external memory provider is configured as holographic in /opt/data/config.yaml, with plugin config under plugins.hermes-memory-store using $HERMES_HOME/memory_store.db, auto_extract false, default_trust 0.5, hrr_dim 1024.
§
stockNews and wutHappened are same project; stockNews deploys at https://stocknews-sentiment.vercel.app with API https://stocknews-api.vercel.app; wutHappened is source/archive material.
§
User has five Google Workspace email profiles: personal-main (primary personal), personal-secondary (backup/restricted), hermes-agent (Hermes automation/account-linked communications), burner (temporary/disposable sending), classicalechos (archive/curated content sending).