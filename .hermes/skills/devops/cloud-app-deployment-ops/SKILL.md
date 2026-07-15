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

For Vercel portfolio audits, first load `references/vercel-portfolio-audit-pattern.md`; the user cares about primary alias vs latest deployment health and end-user product readiness, not just HTTP 200.

For Azure near-free backend/service planning, load `references/azure-free-tier-service-planning.md`; the user prefers service-owned `infra/` directories and explicit cost/security guardrails before deployment.
For Azure Terraform + GitHub Actions deployment setup, load `references/azure-terraform-github-actions-oidc.md`; use OIDC + GitHub Environment approval gates instead of long-lived Azure deploy secrets. If the user says “pim up,” start `az login --use-device-code` and give them the code/link.
For Azure service-account/persistent-login setup, load `references/azure-service-principal-persistent-login.md`; use GitHub OIDC for pipelines, a local service-principal helper outside repos for Hermes CLI sessions, and verify no paid resources were created by identity bootstrap.
For Azure Static Web Apps managed API fallback / no-quota MVP deployment, load `references/azure-static-webapps-managed-api-fallback.md`; use it when a separate Azure Functions/App Service Plan hits quota or the MVP can run as Static Web Apps Free + managed API.
For public RuneLite/plugin telemetry APIs on Azure, load `references/azure-runelite-telemetry-api-security.md`; keep the website read-only, avoid static plugin secrets, batch telemetry, rate-limit aggressively, and use public static/sanitized snapshots for low-latency website analytics.

1. Identify provider/platform, target account/project, and deployment environment.
2. Verify CLI installation and authentication without printing secrets.
3. Inspect existing project configuration before changing build/output settings.
4. Deploy or redeploy with real command output.
5. Verify the live URL or provider status page after deployment.
6. Record blockers: missing credentials, paid marketplace constraints, app protection, alias drift, or unsupported runtime.

## Re-homed Playbooks

- `references/cloud-provider-cli-setup/original-skill.md` plus provider credential/setup references.
- `references/vercel-app-deployments/original-skill.md` plus Vercel deployment, OAuth, database, static shell, alias, and project-decommission references.
- `references/vercel-live-portfolio-audit-2026-06-29.md` — live Vercel portfolio audit pattern: compare primary aliases, configured aliases, and latest deployment URLs; distinguish alias drift from actual app breakage.
- `references/azure-near-free-serverless-backend.md` — Azure MVP pattern for low/near-free hosted services using Static Web Apps Free, Functions Consumption, and Cosmos DB Free Tier with budget/cost guardrails.
- `references/azure-near-free-serverless-backend.md` — Azure MVP pattern for low/near-free hosted services using Static Web Apps Free, Functions Consumption, and Cosmos DB Free Tier with budget/cost guardrails.
- `references/azure-terraform-github-actions-oidc.md` — service-owned Terraform layout, GitHub OIDC setup, environment-gated federated credentials, split infra/app workflows, and `pim up` Azure device-code login convention.
- `references/azure-service-principal-persistent-login.md` — service-principal deployer identity pattern for GitHub OIDC plus local Hermes CLI/Terraform persistent login, including secret-safe helper scripts and free/cost guardrails.
- `references/azure-static-webapps-managed-api-fallback.md` — fallback from separate Function App/App Service Plan to Static Web Apps Free managed API when Azure quota blocks Functions Consumption or a lower-quota MVP is preferred.

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

## Workflow Enhancement: Cross-Project Continuity

When Vercel deployment tasks are complete and no blockers exist, transition to the next project in the user's priority queue rather than waiting for new instructions. The Robinhood trading system is a natural next step when infrastructure work is done.

### Example transition path:
1. Complete all Vercel project deployments and verifications.
2. Confirm no credential/API blockers remain.
3. Identify next priority project (e.g., Agentic Robinhood trading system).
4. Run the relevant monitoring/cron job or fetch account/portfolio status to verify operational state.

This keeps momentum and provides immediate value without idle time.
