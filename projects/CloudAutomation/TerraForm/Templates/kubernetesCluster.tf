# ***********************************************************************************
#STEPS TO CREATE AN AZURE KUBERNETES SYSTEM

# - create azure container regristry
# - create a resource group
# - tag image with azure container uri:v1
# - push to azure container registry
# - add image name into yaml config files
# - PROVISION!


# - docker image build -t music-ai .
# - docker push sosaioyama.azurecr.io/music-ai:v1




# YOU NEED THESE TO DEPLOY A KUBERNETES CLUSTERS
# - Docker Images
# - Azure Container Registry
# - Linking the two 
# -  yaml config files, modified to kuber params


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









# DEPLOY A RESOURCE GROUP
resource "azurerm_resource_group" "rg" {
  name     = "terraform-demo"
  location = "centralus"
}







# DEPLOY A CONTAINER REGISTRY
resource "azurerm_container_registry" "acr" {
  name                = "registrytfdemo"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}






# DEPLOY A CLUSTER
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "music-ai-cluster"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  dns_prefix          = "music-ai-k8s"

  default_node_pool {
    name            = "default"
    node_count      = 2
    vm_size         = "Standard_D2_v2"
    os_disk_size_gb = 30
  }


  identity {
    type = "SystemAssigned"
  }


}



# ATTATCH CONTAINER REGRISTRY TO CLUSTER via roles
resource "azurerm_role_assignment" "example" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}



