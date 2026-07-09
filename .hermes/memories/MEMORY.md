Daily HeRmEz backup cron: cfcea697da5c, 03:00, /opt/data/scripts/backup_hermez.sh, no_agent, backs up /opt/data into /opt/data/HeRmEz/.hermes and pushes origin/main.
§
Hermes Kanban is consolidated to the canonical default board for the user's main workspace. DB path is /opt/data/kanban.db; current-board file is /opt/data/kanban/current with value "default". Use the default board for active HeRmEz project work; old hermez and nous-kanban-demo boards were removed after backup.
§
Email/YT rules: faceless/newsletters→Trapiistan/Sosai; Viral Radar→Classical Echos first, then Trapiistan/Sosai + fareed320 if rate-limited. Use Hermes/HeRmEz Google OAuth client. Delete source emails only after verified correct-channel upload. Viral Radar: strict watchlist, 10–50 real clips/source, no filler; queue failed uploads.
§
Cox Elementary PTA dynamic Django site is deployed at https://cox-elementary-pta.onrender.com from repo /opt/data/HeRmEz/projects/cox-elementary-pta.
§
Hermes external memory provider is configured as holographic in /opt/data/config.yaml, with plugin config under plugins.hermes-memory-store using $HERMES_HOME/memory_store.db, auto_extract false, default_trust 0.5, hrr_dim 1024.
§
User has five Google Workspace email profiles: personal-main (primary personal), personal-secondary (backup/restricted), hermes-agent (Hermes automation/account-linked communications), burner (temporary/disposable sending), classicalechos (archive/curated content sending). Faceless YouTube channel processes fareed320 newsletters (TLDR/Daily Stoic/Kino) into daily videos, with cleanup and email deletion post-upload.
§
User wants Agentic Robinhood auto-trading: monitor/manage cron, high deployment; Venice/redteam pentest.
§
Google Workspace policy: affan.fareed@gmail.com and fareed320@gmail.com have user-approved full read/write Workspace permissions, incl. Gmail read/modify/send.
§
WhosGrindingClanPanel Windows run command is `gradlew.bat run --no-daemon --console=plain` (or `./gradlew.bat run`); `runClient` is not the working task for this repo.