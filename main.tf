resource "azurerm_resource_group" "rg" {
  name     = "${var.resource_group_name}-${var.environment}"
  location = var.location
}

resource "azurerm_resource_group" "aw-rg-2-dev" {
  name     = "aw-rg-2-dev"
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet"
  location            = var.location
  address_space       = ["10.0.0.0/16"]
  resource_group_name = azurerm_resource_group.rg.name
  dns_servers         = []
}

resource "azurerm_network_security_group" "aw-nsg" {
  name                = "nsg"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
}

resource "azurerm_storage_account" "storage" {
  name                     = "appstorage${var.environment}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


resource "azurerm_service_plan" "app_service_plan" {
  name                = "appserviceplan-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "P1v2"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "functionapp-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_service_plan.id

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  site_config {
    application_stack {
      python_version = "3.8"
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_key_vault" "key_vault" {
  name                        = "kv-${var.resource_group_name}-${var.environment}"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 90
  purge_protection_enabled    = false

  sku_name = "standard"

  network_acls {
    default_action             = "Allow"
    bypass                     = "AzureServices"
  }
}

resource "azurerm_application_insights" "app_insights" {
  name                = "appinsights-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

resource "azurerm_log_analytics_workspace" "la_workspace" {
  name                = "example-workspace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
}

resource "azurerm_monitor_diagnostic_setting" "app_insights_diag" {
  name                       = "diagsetting-${var.environment}"
  target_resource_id         = azurerm_linux_function_app.function_app.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.la_workspace.id

  enabled_log {
    category = "FunctionAppLogs"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

data "azurerm_client_config" "current" {}