resource "azurerm_resource_group" "rg-main" {
  name = var.name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet"
  location            = var.location
  address_space       = ["10.0.0.0/16"]
  resource_group_name = data.azurerm_resource_group.rg-main.name 
  dns_servers         = []
}
