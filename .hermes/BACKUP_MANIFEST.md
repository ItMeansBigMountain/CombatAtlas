# Hermes home backup manifest

Created: 2026-05-14T06:07:59.306018+00:00
Source: /opt/data
Destination: /opt/data/HeRmEz/.hermes

This is a sanitized snapshot. Excluded intentionally:

- /opt/data/HeRmEz itself, to avoid recursive backups
- .env, .git-credentials, .gitconfig
- auth.json and auth.lock
- files whose names contain secret, token, or credential
- private key material (*.pem, *.key, id_rsa*, id_ed25519*)
- runtime locks, pids, and Python cache directories

Future project folders should live under /opt/data/HeRmEz/projects.
