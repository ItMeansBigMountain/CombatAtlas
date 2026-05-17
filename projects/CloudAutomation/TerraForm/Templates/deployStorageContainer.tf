# **********************************
# RENAME TO main.tf IN ORDER TO RUN
# **********************************




terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.27.0"
    }
  }
}




# NOTE: CREATE provider.tf AND DROP THIS IN THERE TO SAFE KEEP SENSITIVE DATA
#provider "azurerm" {
#  features {}
#  subscription_id   = "xxxx"
#  tenant_id         = "xxxx"
#  client_id         = "xxxx"
#  client_secret     = "xxxx"
#}
provider "azurerm" {
  features {}
}

# SINCE WE ARE LOGGED INTO CLI USING 'az login'
# WE CAN USE THIS OBJECT TO PULL VARIABLES  FROM OUR [CURRENT USER OBJECT]
data "azurerm_client_config" "current" {}







# # CREATE RESOURCE GROUP (errors out if already existing)
# resource "azurerm_resource_group" "rg" {
#   location = "centralus"
#   name     = "terraform-demo"
# }




# CREATE STORAGE ACCOUNT ( aws: s3 bucket)
resource "azurerm_storage_account" "terraform-storage-account" {
  # location            = azurerm_resource_group.rg.location
  # resource_group_name = azurerm_resource_group.rg.name
  name                     = "terraformdemo786" # needs to be unique and lowercase
  location                 = "centralus"
  resource_group_name      = "terraform-demo"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}




# CREATE STORAGE CONTAINER
resource "azurerm_storage_container" "terraform-container" {
  name                  = "terraform-container"
  storage_account_name  = azurerm_storage_account.terraform-storage-account.name
  container_access_type = "blob" #Meaning: 'publc'
  # container_access_type = "private"
}




# CREATE BLOB
resource "azurerm_storage_blob" "terraform-blob" {
  name                   = "DEMO-BLOB"
  type                   = "Block"
  storage_account_name   = azurerm_storage_account.terraform-storage-account.name
  storage_container_name = azurerm_storage_container.terraform-container.name
  source                 = "blobFile.txt"

  # BEST PRACTICES TO USE depends_on TO ENSURE THE CREATION / EXISTENCE
  # OF A RESOURCE BEFORE REFERENCE
  depends_on = [
    azurerm_storage_container.terraform-container
  ]
}
