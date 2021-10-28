import logging
import json
import re
import os
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def main(req: func.HttpRequest) -> func.HttpResponse:
    vaultName = os.getenv('KEY_VAULT')
    secretName = req.params.get('secretName')

    if not secretName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            secretName = req_body.get('secretName')
    logging.info(vaultName+" "+secretName)
    if secretName and vaultName:
        logging.info('Entered the function')
        logging.info('Set variables')
        KVUri = f"https://{vaultName}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        pubkeyname = secretName + "pub"
        privkeyname = secretName + "priv"
        https_regex = "((\w+:\/\/)[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\`#|]+)"

        logging.info("Generate keypair")
        keypair = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

        logging.info("Generate public and private key")
        public_key = keypair.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        private_key = keypair.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())

        logging.info("Decode the public and private key")
        public_key_str = public_key.decode('utf-8')
        private_key_str = private_key.decode('utf-8')

        logging.info("Send the public and private key to the secret store")
        public_key_return = client.set_secret(pubkeyname, public_key_str)
        private_key_return = client.set_secret(privkeyname, private_key_str)

        logging.info("Filter out the junk that Azure sends back to get the URL")
        public_key_url = re.findall(https_regex, str(public_key_return))
        private_key_url = re.findall(https_regex, str(private_key_return))

        logging.info("Return the response URLs in JSON format")
        return func.HttpResponse(json.dumps({'publicKeySecretName': pubkeyname, 'publicKeySecretURL': public_key_url[0][0], 'privateKeySecretName': privkeyname, 'privateKeySecretURL': private_key_url[0][0]}))
    else:
        return func.HttpResponse(
             '''Bad request. Maybe you didn't set your vault name, or sent an incorrectly formatted secret name. Try and POST {"secretName": "test"} or check your application settings''',
             status_code=400
        )
