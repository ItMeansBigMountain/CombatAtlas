# Clan War Board Azure Infrastructure Plan

## Goal

Create a separate Azure-hosted service for the Clan War Board RuneLite plugin. The RuneLite plugin remains a Plugin Hub project; the backend/infra lives separately under `projects/osrs-plugins/infra/` so Plugin Hub PR work stays clean.

## Recommended organization

```text
projects/osrs-plugins/
  in-progress/CompetitionOverlay/          # RuneLite plugin repo, Plugin Hub-facing only
  infra/
    clan-war-board-azure-plan.md           # this planning doc
    clan-war-board-service/                # future backend app repo/submodule
      api/                                 # Azure Functions API
      web/                                 # optional Azure Static Web Apps frontend
      infra/                               # Bicep/Terraform IaC
      docs/                                # API/privacy/deployment docs
```

The backend should become a **new project/repo** rather than living inside the RuneLite plugin repo. Suggested repo name:

```text
clan-war-board-service
```

The RuneLite plugin should consume the service over HTTPS through a small client class, with an explicit online-sync warning.

## Near-free Azure stack options

### Option A — preferred MVP: Azure Static Web Apps + Azure Functions + Azure Cosmos DB Free Tier

Use when we want a complete hosted API plus optional public site with very low cost.

Components:

- **Azure Static Web Apps Free** for public pages/admin frontend.
- **Azure Functions Consumption** for HTTPS API endpoints.
- **Azure Cosmos DB Free Tier** for persisted war data.

Why:

- Serverless; no always-on VM.
- Cosmos DB free tier can cover the first chunk of usage if created with free-tier enabled.
- Functions Consumption has a monthly free grant.
- Static Web Apps free tier is suitable for a simple public board/admin UI.

Cautions:

- Cosmos DB free tier must be explicitly enabled when the account is created.
- Only one Cosmos DB free-tier account per subscription.
- Use budgets/alerts and avoid provisioned resources outside free limits.
- Do not store live PvP locations publicly.

### Option B — simplest relational MVP: Azure Functions + Azure SQL free database

Use when relational queries matter more than NoSQL simplicity.

Components:

- Azure Functions Consumption API.
- Azure SQL Database free offer.
- Static Web Apps optional frontend.

Why:

- SQL schema fits clans/wars/participants/acceptances well.
- Easier joins and reporting.

Cautions:

- Verify the current Azure SQL free offer during deployment; make sure the free database option is selected, not a paid default tier.
- SQL connection/auth adds more setup than Cosmos DB.

### Option C — ultra-simple prototype: Static Web Apps + Functions + Azure Table Storage

Use only for early prototype if we want minimal database complexity and can tolerate basic queries.

Components:

- Static Web Apps.
- Functions.
- Azure Storage Table/Blob.

Why:

- Cheap and simple.

Cautions:

- Less suitable for leader verification, war status history, and leaderboards.
- May become limiting quickly.

## Recommended MVP choice

Use **Option A**:

```text
Azure Static Web Apps Free
Azure Functions Consumption
Azure Cosmos DB Free Tier
```

Data is document-shaped enough for v1:

- clan records
- war proposals
- acceptances
- member-visible war cards
- completed summaries

Cosmos DB can store each war as a document and use partition keys such as `clanId` or `warId`.

## Privacy / visibility rules

Upcoming war details are PvP intel. Default privacy must be conservative.

Public before war:

- clan names
- status: proposed/confirmed
- broad war category

Clan/member-only before war:

- exact time
- world
- hotspot/location
- rules/rally notes

Leader-only:

- draft wars
- proposals needing acceptance
- edit/cancel controls
- acceptance history

Public after war:

- completed/sanitized summary if leaders mark it public
- no future rally info

## Leader agreement model

The service should manage agreement, not local codes.

War lifecycle:

```text
DRAFT -> PROPOSED -> ACCEPTED/CONFIRMED -> COMPLETED/CANCELLED
```

Agreement fields:

```text
warId
creatorClanId
opponentClanId
termsHash
proposedByPlayer
proposedAt
acceptedByPlayer
acceptedAt
status
```

`termsHash` covers:

```text
creator clan
opponent clan
war name
start time
duration
world
hotspot
rules
visibility
```

If any term changes after acceptance, set:

```text
status = RECONFIRM_REQUIRED
```

## Auth / verification stance

RuneLite can detect clan rank locally, but the backend cannot perfectly prove it at first.

V1:

- Plugin sends player name, clan name, and locally observed clan rank.
- Backend records actions as plugin-submitted and marks clans as unverified unless claimed.
- Leader actions require rank >= configured threshold in the plugin.

V2:

- Add clan claiming.
- Add Discord OAuth/bot verification for clan leader roles.
- Add verified-clan badge and stricter leader permissions.

## Proposed API endpoints

```text
GET  /api/health
POST /api/players/session
GET  /api/clans/{clanId}/wars
POST /api/wars
PATCH /api/wars/{warId}
POST /api/wars/{warId}/propose
POST /api/wars/{warId}/accept
POST /api/wars/{warId}/cancel
POST /api/wars/{warId}/complete
GET  /api/public/wars
GET  /api/public/leaderboard
```

## Suggested Cosmos containers

```text
clans          partition: normalizedClanName
players        partition: normalizedClanName
wars           partition: clanPairKey or creatorClanId
war_actions    partition: warId
summaries      partition: warId
```

For v1, one `wars` container plus one `clans` container may be enough.

## Repo / deployment layout

Future service repo:

```text
clan-war-board-service/
  api/
    package.json or requirements.txt
    src/functions/*.ts or *.py
  web/
    package.json
    src/
  infra/
    main.bicep
    parameters.dev.json
    parameters.prod.json
  docs/
    privacy.md
    api.md
    plugin-contract.md
  README.md
```

Use Bicep for Azure IaC unless we decide Terraform is needed.

## RuneLite plugin boundary

The Plugin Hub-facing plugin repo should contain only:

- RuneLite UI
- rank detection
- API client
- config and privacy warning
- tests/mocks for service responses

It should not contain Azure IaC or deployment secrets.

Add plugin config later:

```text
Enable Online Sync
Service URL
Send player/clan/rank warning
```

Warning text should clearly say:

```text
Online Sync sends your player name, clan name, observed clan rank, and war actions to the Clan War Board service so clan leaders and members can share war schedules.
```

## Cost controls

- Create a dedicated resource group, e.g. `rg-clan-war-board-dev`.
- Enable Azure budget alerts at a very low monthly cap.
- Prefer serverless/free tiers only.
- Do not create always-on App Service plans, VMs, Application Gateway, Front Door, or paid database tiers for MVP.
- Log lightly; high-volume Application Insights can create cost.

## Next steps

1. Decide backend stack: recommended Azure Static Web Apps + Functions + Cosmos DB Free Tier.
2. Create new service repo under `projects/osrs-plugins/infra/clan-war-board-service` or as a child GitHub repo/submodule.
3. Add Bicep skeleton with budget/resource group notes.
4. Implement `GET /api/health` and local emulator/dev config.
5. Implement core data model: clan, war, acceptance, visibility.
6. Add plugin `Online Sync` config and a mocked API client.
7. Wire plugin to list/create wars only after privacy warning is in place.
