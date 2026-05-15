The user's primary Hermes workspace repo is /opt/data/HeRmEz, cloned from https://github.com/ItMeansBigMountain/HeRmEz.git. Future project folders should be created under /opt/data/HeRmEz/projects, and Hermes config terminal.cwd is set to /opt/data/HeRmEz.
§
A daily HeRmEz backup cron job exists: job_id cfcea697da5c, name "Daily HeRmEz GitHub backup", schedule "0 3 * * *", script backup_hermez.sh in /opt/data/scripts, no_agent true, backing up /opt/data into /opt/data/HeRmEz/.hermes and pushing to origin/main.
§
Hermes Kanban board for the user's main workspace is slug "hermez" (display name "HeRmEz Workspace"), DB path /opt/data/kanban/boards/hermez/kanban.db, active-board file /opt/data/kanban/current set to hermez. Current known assignee profile is default.