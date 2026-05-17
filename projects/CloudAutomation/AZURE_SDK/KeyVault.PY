# REQUIREMENTS

    # SERVICE PRINCIPLE AUTH
        # Create service principle
            # 'az ad sp create-for-rbac --name {SERVICE_PRINCIPAL_NAME} --role {ROLE_NAME} --scopes /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup1} > servicePrincipal.json'


    # CLI AUTH
        # Make sure you have AZ CLI installed
            # 'az login'
            # 'az account show'


    # pip install azure-keyvault-secrets
    # pip install azure-identity





from azure.identity import ClientSecretCredential

from azure.keyvault.secrets import SecretClient #Service Principle Auth
from azure.identity import AzureCliCredential   #CLI Auth







# INIT GLOBAL VARIABLES
KEYVAULT_NAME = "terraform-Demo-key-vault"
KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net"








# SERVICE PRINCIPLE AUTHORIZATION
# TENANT_ID = ""
# CLIENT_ID = ""
# CLIENT_SECRET = ""
# _credential = ClientSecretCredential(
    # SERVICE PRINCIPLE WITH PROPER SCOPE AND PERMISSIONS ENABLED
    # tenant_id = TENANT_ID,
    # client_id = CLIENT_ID,
    # client_secret = CLIENT_SECRET
# )






# CLI AUTHORIZATION
_credential = AzureCliCredential()






# KEY VAULT SECRETS OBJECT
_sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)





# DATA EXTRACTION
demo_secret = _sc.get_secret("secret").value
print(demo_secret)


