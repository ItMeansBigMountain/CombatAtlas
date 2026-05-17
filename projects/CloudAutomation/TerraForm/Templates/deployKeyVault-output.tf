# ***********************************
# RENAME FILE TO output.tf
# ***********************************


# DISPLAY SPECIFIC DATA FROM RESOURCE TAG IN main.tf
output "key-vault-id" {
  value = azurerm_key_vault.key-vault.id
}
output "key-vault-url" {
  value = azurerm_key_vault.key-vault.vault_uri
}