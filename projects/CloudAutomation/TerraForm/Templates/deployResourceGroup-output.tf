# ***********************************
# RENAME FILE TO output.tf
# ***********************************


# DISPLAY SPECIFIC DATA FROM RESOURCE TAG IN main.tf
output "resource_group_name" {
  value = azurerm_resource_group.example_rg.name
}
output "resource_group_name" {
  value = azurerm_resource_group.example_rg2.name
}
