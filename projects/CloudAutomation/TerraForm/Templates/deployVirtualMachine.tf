# ***********************************************************************************
#STEPS TO CREATE AN AZURE VIRTUAL MACHINE

# create a resource group
# create a virtual network
# create a subnet
# create a network interface card
# create a virtual machine (we can also create disks etc as a separate step)

# NOTE: VM USERNAME CANNOT BE "admin"
#  PASSWORD MUST BE 8-123 CHARACTERS W/UPPERCASE,LOWERCASE,NUMERICAL, & SPECIAL
# ***********************************************************************************





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






# CREATE RESOURCE GROUP
resource "azurerm_resource_group" "rg" {
  location = "eastus"
  name     = "terraformDemo"
}




# CREATE VIRTUAL NETWORK
resource "azurerm_virtual_network" "azvnet" {
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  name                = "terraformDemoVNet"
  resource_group_name = azurerm_resource_group.rg.name
}





# CREATE SUBNET
resource "azurerm_subnet" "azsubnet1" {
  name                 = "terraformDemoSubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.azvnet.name
  address_prefixes     = ["10.0.0.0/24"]
}






# CREATE NETWORK INTERFACE CARD
resource "azurerm_network_interface" "aznetworkinterface" {
  location            = azurerm_resource_group.rg.location
  name                = "terraformDemoNetworkInterface"
  resource_group_name = azurerm_resource_group.rg.name
  ip_configuration {
    name                          = "terraformDemoNetworkInterfaceIp"
    subnet_id                     = azurerm_subnet.azsubnet1.id
    private_ip_address_allocation = "Dynamic"
  }
}




# CREATE VIRTUAL MACHINE
resource "azurerm_windows_virtual_machine" "winvm1" {
  admin_username        = "tfDemoAdmin"
  admin_password        = "YOUR_VM_ADMIN_PASSWORD"
  location              = azurerm_resource_group.rg.location
  name                  = "terraformDemoVM"
  network_interface_ids = [azurerm_network_interface.aznetworkinterface.id]
  resource_group_name   = azurerm_resource_group.rg.name
  size                  = "standard_f2"
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2008-R2-SP1"
    version   = "latest"
  }
}
