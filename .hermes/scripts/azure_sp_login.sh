#!/usr/bin/env bash
set -euo pipefail
AZ=(/opt/data/home/.local/share/uv/tools/azure-cli/bin/python -m azure.cli)
SECRET_FILE="/opt/data/secrets/hermes-azure-terraform-deployer.env"
if [ ! -f "$SECRET_FILE" ]; then
  echo "Missing $SECRET_FILE" >&2
  exit 1
fi
set -a
source "$SECRET_FILE"
set +a
"${AZ[@]}" login --service-principal \
  --username "$AZURE_CLIENT_ID" \
  --password "$AZURE_CLIENT_SECRET" \
  --tenant "$AZURE_TENANT_ID" \
  -o none
"${AZ[@]}" account set --subscription "$AZURE_SUBSCRIPTION_ID"
"${AZ[@]}" account show --query '{subscription:id,tenant:tenantId,user:user.name}' -o json
