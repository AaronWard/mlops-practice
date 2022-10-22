# mlops-practice
Practice repo for MLOps on Azure using terraform. 

### Terraform



**Basic commands:**
- `terraform init`
- `terraform plan`
- `terraform apply`
- `terraform destroy`

**Resources:**


```terraform
resource "<type>: "<name>" {
    ...
}
```

```terraform
resource "azurerm_resource_group" "rg" {
  name      = "${var.resource_group_name}_${var.environment}"
  location  = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet"
  location            = var.location
  address_space       = ["10.0.0.0/16"]
  resource_group_name = azurerm_resource_group.rg.name
  dns_servers         = []
}
```

variables can be cross refences by `resource_type.resource_name.key` pr `resource_type.resource_name.id` (some use IDs)



**Data blocks:**

If a resource already exists in the statefile, or if you want to reference that exists but your didn't create you can do that in a data block.



**Providers:**

- `providers.tf`

Helper functions the terraform uses to interact with external sercices/resouces. IE: local docker server, Cloud provider (Azure). 

```terraform
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}
```

**Variables:**
variables are common values that can be references elsewhere

- `variables.tf`

```
variable "location" { }
```

**terraform.tfvars:**
terraform.tfvars holds the common values, is referrenced in variables.tf

```
location = "centralus"
```

**Backend:**


### Azure CLI

- `az login --use-device-code`
- `az account set --subscription ""` if on more than 1 subscription



---
### Links

- [IaC Overview](https://www.crowdstrike.com/cybersecurity-101/infrastructure-as-code-iac/?utm_campaign=cloudsecurity&utm_content=c4c_cloud_us_en_nb_low&utm_medium=sem&utm_source=goog&utm_term=iac&gclid=Cj0KCQjwxveXBhDDARIsAI0Q0x2p_z69E8H4h6dUhC9OM7I3SePsfCxyifrOuoHKY-bx7iw3WYReaFQaApVdEALw_wcB)
- 
