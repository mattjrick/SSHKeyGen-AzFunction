# SSHKeyGen-AzFunction
An Azure Function that generates an SSH keypair and stores it in Azure Key Vault.
I'm using it to generate an SSH keypair in Terraform, so that the private key is not visible in the tfstate (see Example Usage).

# Function Usage
This function requires:
- ['SET' access policy permissions to 'Secrets' in a Key Vault instance.](https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=dotnet)
- [An Application Setting key-value pair 'KEY_VAULT':'yourkeyvaultname'](https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings)
- [Generate a Function Key (or use the default) in order to access the API](https://docs.microsoft.com/en-us/azure/azure-functions/security-concepts#function-access-keys) 
