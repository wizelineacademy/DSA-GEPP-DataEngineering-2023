# Session 12 - Terraform for Lecturer

## Goal

The goal is to setup IAM roles for Lambdas and Step Functions to be created by the students. Having this separate from their exercise guarantees that they don't need IAM creation privileges.

The output of this Terraform configuration is required by the students. They will request it. 

## Study Terraform

Open, study and understand the Terraform configuration files in the following order:
1. `variables.tf`. Contains definitions for variables referenced in other files.
2. `terraform.tfvars`. Contains the key-value pairs of the variables defined. 
3. `main.tf`. Contains defaults for Terraform config.
4. `iam.tf`. Contains the definition of two IAM Roles. One for Lambdas and one for Step Functions.
5. `output.tf`. Defines Terraform Outputs of the ARNs values of the created IAM Roles.

## Execute

Initialze the Terraform environment in this directory.

```shell
terrafom init
```

### Plan

Execute and study the Terraform plan output. 

```shell
terrafom plan
```

Notice all resources to be created.

### Apply

Execute Terraform apply. 

```shell
terrafom apply
```

Wait until all resources are created. It will take a few seconds.

### Destroy

Once the students are done with their exercise, execute Terraform destroy.

```shell
terrafom destroy
```

Validate all resources to be destroyed. This might fail if the students have not destroyed their resources.