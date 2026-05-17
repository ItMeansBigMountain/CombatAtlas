# **********************************
# RENAME TO main.tf IN ORDER TO RUN
# **********************************



# Specify the version of the AzureRM Provider to use
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.27.0"
    }
  }
}




# Configure Azure RESOURCE MANAGEMENT provider
provider "azurerm" {
  features {}

  # **AZURE SERVICE PRINCIPAL CREDENTIALS HERE**
  subscription_id = "azure_subscription_id"
  tenant_id       = "azure_subscription_tenant_id"
  client_id       = "service_principal_appid"
  client_secret   = "service_principal_password"
}





# DEPLOY  RESOURCE GROUPs
resource "azurerm_resource_group" "example_rg" {
  name     = "terraform-demo"
  location = "centralus"
}

resource "azurerm_resource_group" "example_rg2" {
  name     = "terraform-demo2"
  location = "centralus"
}
