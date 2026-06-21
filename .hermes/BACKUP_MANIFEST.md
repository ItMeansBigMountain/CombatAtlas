# Hermes home backup manifest

Last backup: 2026-06-21T03:00:31Z
Source: /opt/data
Destination: /opt/data/HeRmEz/.hermes

This is a sanitized snapshot. Excluded intentionally:

- /opt/data/HeRmEz itself, to avoid recursive backups
- .env, .git-credentials, .gitconfig
- auth.json and auth.lock
- OAuth/keyring files
- files whose names contain secret, token, or credential
- private key material (*.pem, *.key, *.p12, *.pfx, id_rsa*, id_ed25519*)
- runtime locks, pids, sockets, common cache/build directories, session logs, local SDKs/CLIs, and generated installs
- nested .git directories

Future project folders should live under /opt/data/HeRmEz/projects.
