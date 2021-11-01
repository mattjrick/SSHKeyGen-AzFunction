variable "name" {
  type        = string
  default     = "sshkeygenexample"
  description = "Name for resources"
}

variable "location" {
  type        = string
  default     = "uksouth"
  description = "Azure Location of resources"
}

variable "functionapp" {
    type = string
    default = "../../Functions/published/v1-build.zip"
}