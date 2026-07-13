# Clan War Board Service

Backend API and static leaderboard service for the Clan War Board RuneLite plugin.

This project is intentionally separate from the Plugin Hub-facing RuneLite plugin. The plugin stays in `projects/osrs-plugins/in-progress/CompetitionOverlay` for now, while this service owns its own app code, docs, and Azure infrastructure.

## Goals

- Keep hosting free or near-free on Azure.
- Provide a backend API for Clan War Board.
- Start with static clan leaderboards so clans can compete for the top.
- Later add war proposals, leader acceptance, verified clans, and completed-war summaries.
- Explore Wise Old Man clan/group import when a clan already exists on WOM.
- Design security up front because public PvP/clan tools will attract abuse.

## Layout

```text
api/       Azure Functions HTTP API and pure Python service code
infra/     Azure Bicep IaC for free-tier Azure resources
docs/      Cost, organization, security, and plugin-contract docs
tests/     Unit tests for API/service behavior
```

## MVP API

Current scaffold:

```text
GET /api/health
GET /api/leaderboard
GET /api/clans/{clanId}
```

The leaderboard is static/sample-backed until Cosmos DB is provisioned and connected.

## Free-tier Azure target

```text
Azure Static Web Apps Free
Azure Functions Consumption
Azure Cosmos DB Free Tier
```

Cosmos DB must be created with `enableFreeTier=true`; it cannot be toggled later.

## Local validation

The core service logic has no cloud dependency and can be tested locally:

```bash
python3 -m unittest discover -s tests -v
```

Azure Functions wiring is intentionally thin and wraps the pure Python API module.
