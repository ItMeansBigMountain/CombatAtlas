# **********************************
# RENAME TO main.tf IN ORDER TO RUN

# MAKE SURE TO PURGE DELETED VAULTS USING
# - az keyvault list-deleted
# - az keyvault purge --name my-fancy-key-vault


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







# CREATE RESOURCE GROUP
resource "azurerm_resource_group" "rg" {
  location = "centralus"
  name     = "terraform-demo"
}





resource "azurerm_key_vault" "key-vault" {
  name                = "terraform-Demo-key-vault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id # user allowed to use keys

  enabled_for_disk_encryption = true
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false


  # CREATING ACCESS POLICY METHOD 1
  # access_policy {
  #   tenant_id = data.azurerm_client_config.current.tenant_id
  #   object_id = data.azurerm_client_config.current.object_id


  #   key_permissions = [
  #     "Get", "Create", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify"
  #   ]

  #   secret_permissions = [
  #     "Get", "Create", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify"
  #   ]

  #   storage_permissions = [
  #     "Get", "Create", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify"
  #   ]
  # }


}



# CREATING ACCESS POLICY METHOD 2
resource "azurerm_key_vault_access_policy" "key-vault-access-policy" {
  key_vault_id = azurerm_key_vault.key-vault.id

  tenant_id = data.azurerm_client_config.current.tenant_id
  object_id = data.azurerm_client_config.current.object_id


  key_permissions = [
    "Get", "Create", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify"
  ]

  secret_permissions = ["Get", "Delete", "List", "Set", "Backup", "Purge", "Recover"]
}





# CREATE SECRET KEY-VALUE PAIR (sometimes youll need to run this twice to create secret)
resource "azurerm_key_vault_secret" "secret" {
  key_vault_id = azurerm_key_vault.key-vault.id
  name         = "secret"
  value        = "53cr3t"
}
