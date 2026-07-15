# Azure Static Web Apps managed API fallback

Use this when a near-free Azure service using Terraform/GitHub Actions hits Azure Functions/App Service Plan quota or wants to avoid a separate Function App for MVP.

## When to use

Signals:

- Terraform `azurerm_service_plan` with Functions Consumption `Y1` fails with:

```text
Operation cannot be completed without additional quota.
Current Limit (Total VMs): 0
Amount required for this deployment (Total VMs): 1
```

- The user wants a near-free public website + API and does not need long-running backend jobs yet.
- Static Web Apps Free is acceptable and the API can run as SWA managed Azure Functions.

## Fix pattern

Switch from separate Function App resources to Static Web Apps managed API:

- Remove `azurerm_service_plan` and `azurerm_linux_function_app` from Terraform.
- Keep Cosmos DB Free Tier and Static Web App Free.
- Deploy with `Azure/static-web-apps-deploy@v1` using:

```yaml
app_location: web
api_location: api
output_location: .
```

- Retrieve the SWA deployment token at deploy time using OIDC-authenticated Azure CLI instead of storing it as a long-lived secret:

```bash
token=$(az staticwebapp secrets list \
  --name "$AZURE_STATIC_WEB_APP_NAME" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --query "properties.apiKey" -o tsv)
```

Then pass it to `Azure/static-web-apps-deploy@v1`.

## Region pitfall

Static Web Apps does not support every Azure region. If Terraform fails with:

```text
LocationNotAvailableForResourceType: The provided location 'eastus' is not available for resource type 'Microsoft.Web/staticSites'
```

Use a separate variable such as `static_web_app_location`, with a supported value like `East US 2` (`eastus2`). Keep the main resource group/Cosmos region separate if needed.

## Minimal repo layout

```text
api/
  function_app.py
  host.json
web/
  index.html
staticwebapp.config.json
infra/terraform/
  main.tf
  variables.tf
  outputs.tf
.github/workflows/
  infra-terraform.yml
  app-deploy.yml
```

`api/host.json` should include a valid Functions v4 host config. `staticwebapp.config.json` can keep public routes read-only and set security headers.

## Verification

After app deploy, verify the website and managed API endpoints externally:

```bash
base="https://<default-hostname>"
curl -fsS "$base/"
curl -fsS "$base/api/health"
curl -fsS "$base/api/leaderboard"
```

For RuneLite telemetry/public analytics systems, keep website endpoints public/read-only and put all write/leader/telemetry paths behind plugin registration/auth/rate limits in later iterations.