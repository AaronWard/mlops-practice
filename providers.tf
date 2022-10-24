terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=2.99.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

