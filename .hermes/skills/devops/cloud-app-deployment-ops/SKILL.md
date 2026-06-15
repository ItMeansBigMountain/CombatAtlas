---
name: cloud-app-deployment-ops
description: "Use when setting up cloud provider CLIs, credentials, or deploying/troubleshooting hosted apps such as Vercel/static/Flask/Django projects."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [devops, cloud, cli, vercel, deployment, credentials, hosting]
    related_skills: [github-pr-workflow, software-quality-workflows]
---

# Cloud App Deployment Ops

## Overview

Use this umbrella for application delivery work that crosses local code, cloud provider CLIs, credentials, and hosted deployment platforms. It consolidates provider CLI setup and Vercel-oriented deployment/triage playbooks.

## Workflow

1. Identify provider/platform, target account/project, and deployment environment.
2. Verify CLI installation and authentication without printing secrets.
3. Inspect existing project configuration before changing build/output settings.
4. Deploy or redeploy with real command output.
5. Verify the live URL or provider status page after deployment.
6. Record blockers: missing credentials, paid marketplace constraints, app protection, alias drift, or unsupported runtime.

## Re-homed Playbooks

- `references/cloud-provider-cli-setup/original-skill.md` plus provider credential/setup references.
- `references/vercel-app-deployments/original-skill.md` plus Vercel deployment, OAuth, database, static shell, alias, and project-decommission references.

## Pitfalls

- Do not install cloud CLIs globally when a user-local install is safer.
- Do not print tokens, API keys, or credential file contents.
- Do not claim deployment success until the live app or provider deployment status is checked.
- Do not assume Vercel marketplace databases are free or available; verify current plan constraints.

## Verification Checklist

- [ ] CLI installed/authenticated or blocker reported.
- [ ] Project/build settings inspected.
- [ ] Deployment command output captured.
- [ ] Live URL/provider status verified.
- [ ] Credential handling was secret-safe.
