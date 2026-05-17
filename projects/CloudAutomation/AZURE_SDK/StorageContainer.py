# REQUIREMENTS
    # Make sure you have AZ CLI installed
        # 'az login'
        # 'az account show'

    # pip install azure-storage-blob
    # pip install azure-mgmt-storage
    # pip install azure-identity






# DOCUMENTATION
    # https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-visual-studio-codev






# *****************************************
# MAKE SURE TO ADD EMAIL TO ROLE TO "Storage Blob Data Contributor" WITHIN SERVICE ACCOUNT 
# *****************************************




from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential




# AUTHORIZATION
credential = AzureCliCredential()






# STORAGE ACCOUNT URL 
account_url = "https://terraformdemo786.blob.core.windows.net/"




# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=credential)






try:

    # List Containers in storage account
    for c in blob_service_client.list_containers():
        print('-----------------------------------')
        print("Container: ", c.name  )

        # List the blobs in the container
        container_client = blob_service_client.get_container_client(container= c.name)
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)


        # DOWNLOAD BLOBS
        with open(file=blob.name, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())



except Exception as ex:
    print('Exception:')
    print(ex)