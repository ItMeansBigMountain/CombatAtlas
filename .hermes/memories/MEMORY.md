Workspace repo: /opt/data/HeRmEz (GitHub ItMeansBigMountain/HeRmEz); create projects under /opt/data/HeRmEz/projects. Hermes git install /opt/data/hermes-agent; launcher /opt/data/.local/bin/hermes; /opt/hermes is legacy/root-owned.
§
A daily HeRmEz backup cron job exists: job_id cfcea697da5c, name "Daily HeRmEz GitHub backup", schedule "0 3 * * *", script backup_hermez.sh in /opt/data/scripts, no_agent true, backing up /opt/data into /opt/data/HeRmEz/.hermes and pushing to origin/main.
§
Hermes Kanban is consolidated to the canonical default board for the user's main workspace. DB path is /opt/data/kanban.db; current-board file is /opt/data/kanban/current with value "default". Use the default board for active HeRmEz project work; old hermez and nous-kanban-demo boards were removed after backup.
§
Email/YT: fareed320 newsletters→Trapiistan/Sosai; trash only after verified upload. YT metrics use same OAuth upload token/account; API enabled. Viral Radar sources include Huberman, Chris Williamson, Kinobody/Greg, Tate, Zerkaa, GG33, Belmars, Hormozi, Hamza. TTS ElevenLabsKey; stock Pexels/Pixabay.
§
Cox Elementary PTA dynamic Django site is deployed at https://cox-elementary-pta.onrender.com from repo /opt/data/HeRmEz/projects/cox-elementary-pta.
§
Hermes external memory provider is configured as holographic in /opt/data/config.yaml, with plugin config under plugins.hermes-memory-store using $HERMES_HOME/memory_store.db, auto_extract false, default_trust 0.5, hrr_dim 1024.
§
User has five Google Workspace email profiles: personal-main (primary personal), personal-secondary (backup/restricted), hermes-agent (Hermes automation/account-linked communications), burner (temporary/disposable sending), classicalechos (archive/curated content sending). Faceless YouTube channel processes fareed320 newsletters (TLDR/Daily Stoic/Kino) into daily videos, with cleanup and email deletion post-upload.
§
User wants Agentic Robinhood auto-trading: monitor/manage cron, high deployment; Venice/redteam pentest.
§
Google Workspace policy: personal-main / affan.fareed@gmail.com should use Gmail read-only scopes, but full/admin Calendar, Drive, Docs, Sheets, and Contacts scopes.