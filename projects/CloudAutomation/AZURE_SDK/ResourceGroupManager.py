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



# DISPLAY ALL RESOURCE GROUPS AS OBJECTS
resource_group_list = resourceManagement_client.resource_groups.list()
for count , item in enumerate(resource_group_list):
    print(  count  )
    # print(  item  )
    print(  f'Name: {item.name}')
    print(  f'Location: {item.location}') 
    print(item.tags)
    print("------")


print("\n\n\n")


# DISPLAY ALL SERVICES (RESOURCES)
resources_list = resourceManagement_client.resources.list()
for count , item in enumerate(resources_list):
    print(  count  )
    # print(  item  )
    print(  item.name  )
    print(  item.id.split("/")[4]  )
    print(  item.location  )
    print(  item.type  )
    if item.sku : print(  item.sku.tier  )
    else: print(None)
    print()






