# mlops-practice
Practice repo for MLOps on Azure using terraform. 

<<<<<<< HEAD
[![Terraform](https://github.com/AaronWard/mlops-practice/actions/workflows/terraform.yml/badge.svg?event=workflow_dispatch)](https://github.com/AaronWard/mlops-practice/actions/workflows/terraform.yml)


=======
### Basic Terraform Cheatsheet
>>>>>>> 952e25e4490126ced98feb7d8c16644ac792935c

### Terraform Concepts:

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
Variables are common values that can be declared and referenced elsewhere

- `variables.tf`

```
variable "location" { }
```

**terraform.tfvars:**
terraform.tfvars holds the common values, is referrenced in variables.tf

```
location = "centralus"
```

**Statefile:**

- Terraform statefile only keeps readings of what it did last time.
- `terraform.tfstate` (Make sure it's kept in the `.gitignore`)
- `terraform destroy` can only destroy resources it created, by looking in the statefile. 


- `terraform.tfstate.backup` is a backup of the statefile, you can use this to undo a `destroy`-
<!-- **Backend:** -->

**Terraform Modules:**
- Way to package up terraform code to be used by other people.
- Directory with tf files in it.

```
module "name" {
  source = "./some_path"
  servers = 5
}
```

**Terraform graph:**

-  `terraform graph | dot -Tsvg > graph.svg`


---

# How-To':


### Azure CLI

- `az login --use-device-code`
- `az account set --subscription ""` if on more than 1 subscription
- `az ad sp create-for-rbac --name aw-sp-1 --role Admin --scopes /subscriptions/df854c79-25cc-463f-9b9d-b5c918678a91`
  - Take the output and add it as secrets in the github repo. This will be references in the workflow file.

### Github Setup
- Add Terraform Workflow in actions
- From your Terraform Cloud User Settings, click on Tokens and generate an API token named GitHub Actions.
- Add the token to your Github repository as a secret. Name the secret `TF_API_TOKEN.`
- set `on` to `workload_dispatch`
- run to check connectivity and provisioning of resources to your Azure subscription.





### Terraform Docs

- `terraform-docs markdown table   --output-file terraform_docs.md   --output-mode inject .`



---
### Links

- [IaC Overview](https://www.crowdstrike.com/cybersecurity-101/infrastructure-as-code-iac/?utm_campaign=cloudsecurity&utm_content=c4c_cloud_us_en_nb_low&utm_medium=sem&utm_source=goog&utm_term=iac&gclid=Cj0KCQjwxveXBhDDARIsAI0Q0x2p_z69E8H4h6dUhC9OM7I3SePsfCxyifrOuoHKY-bx7iw3WYReaFQaApVdEALw_wcB)
- [terraform-docs](https://terraform-docs.io/user-guide/introduction/)
- [Managing your machine learning infrastructure as code with Terraform](https://www.jeremyjordan.me/terraform/)
