# REQUIREMENTS
    # Make sure you have AZ CLI installed
        # 'az login'
        # 'az account show'

    # pip install azure-mgmt-resource
    # pip install azure-identity





from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient



# AUTHORIZATION
credential = AzureCliCredential()
subscription_id =  "44ad0ad0-6513-43de-a596-0b293e83e53c"


# INIT RESOURCE MANAGER CLIENT
resourceManagement_client = ResourceManagementClient(credential, subscription_id)









# CREATE/UPDATE PARAMS 
resource_name = input("Please enter Resource Group Title: ")
resource_params = {
    "managedBy" : None ,  #The ID of the resource that manages this resource group.
    "location" : "centralus" ,
    "tags" : {} ,
}









# # CREATE resource group
# resourceManagement_client.resource_groups.create_or_update(
#     resource_name  ,
#     resource_params
# )





# READ resource group
# found = False
# for resource in resourceManagement_client.resource_groups.list():
#     if resource.name == resource_name:
#         found = True
# if found:
#     print("RG '" + resource_name + "' found!")
# else:
#     print("RG \'" + resource_name + "\' NOT found!")





# UPDATE resource group
# resourceManagement_client.resource_groups.create_or_update(
#     resource_name  ,
#     resource_params
# )





# DELETE resource group
deletion_operation = resourceManagement_client.resource_groups.begin_delete(resource_name)
print("deleting \'" + resource_name + "\' ...")
deletion_operation.wait()
print("done!")