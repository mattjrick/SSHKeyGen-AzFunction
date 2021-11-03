module "deploy-example" {
    source = "../Deploy-Example"
}

data "curl" "postSecrets" {
    http_method = "POST"
    uri = "https://${module.deploy-example.default_hostname}/api/SSHKeyGen?code=${module.deploy-example.default_function_key}&secretName=${var.secretName}"
}

locals {
  json_data = jsondecode(data.curl.postSecrets.response)
}

output "all_secrets" {
    value = local.json_data
}

output "private_key_secret_name" {
    value = local.json_data.privateKeySecretName
}

output "private_key_secret_url" {
    value = local.json_data.privateKeySecretURL
}

output "public_key_secret_name" {
    value = local.json_data.publicKeySecretName
}

output "public_key_secret_url" {
    value = local.json_data.publicKeySecretURL
}