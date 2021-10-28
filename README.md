# SSHKeyGen-AzFunction
An Azure Function that generates an SSH keypair and stores it in Azure Key Vault.
I'm using it to generate an SSH keypair in Terraform, so that the private key is not visible in the tfstate (see Example Usage).

# Function Usage
This function requires:
- ['SET' access policy permissions to 'Secrets' in a Key Vault instance.](https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=dotnet)
- [An Application Setting key-value pair 'KEY_VAULT':'yourkeyvaultname'](https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings)
- [Generate a Function Key (or use the default) in order to access the API](https://docs.microsoft.com/en-us/azure/azure-functions/security-concepts#function-access-keys) 

# Expected output
## 200 Success
A successful POST response will look like this
        {
            "publicKeySecretName": "examplenamepub",
            "publicKeySecretURL": "https://examplevault.vault.azure.net/secrets/examplenamepub/c42b7f6e48424407b9849c73b9fdd3a7",
            "privateKeySecretName": "examplenamepriv",
            "privateKeySecretURL": "https://examplevault.vault.azure.net/secrets/examplenamepriv/75f97cd2889e4a698ceeb4b2f34ad434"
        }
## 400 Error
If a configuration error has occured i.e. you did not set the KEY_VAULT app config OR/AND you did not send a valid secret name you will receive a 400 error. Refer back to Function Usage section.

## 500 Error
Something has gone terribly wrong and hasn't been caught properly. It is most likely that the correct Access Policy has not been applied to allow Functions to SET Key Vault secrets. Refer back to Function Usage section.