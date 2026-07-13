# Azure Infra

Bicep IaC for the Clan War Board service.

## Free-tier requirements

- Cosmos DB account uses `enableFreeTier: true`.
- Cosmos database shared throughput defaults to `400` RU/s and is capped by parameter validation at `1000` RU/s.
- Static Web App SKU is `Free`.
- Function App is Linux consumption-style; do not switch to Premium/App Service plan for MVP.

## Deploy later

Do not deploy until Azure auth/subscription is selected and a budget alert strategy is confirmed.

```bash
az group create --name rg-clan-war-board-dev --location eastus
az deployment group create \
  --resource-group rg-clan-war-board-dev \
  --template-file infra/main.bicep \
  --parameters @infra/parameters.dev.json
```

After deployment, verify in the Azure Portal:

1. Cosmos DB says free tier is enabled.
2. Cosmos DB throughput is <= 1000 RU/s.
3. Static Web App is Free.
4. No VM/App Service plan/Premium Functions was created.
5. Budget alerts exist before public traffic.
