# Session 12 - Terraform for Students

## Goal

The goal is to deploy the python files in `./src` as two AWS Lambda functions and control their execution through a Step Function. 

This configuration requires the output from `../terraform-pre-class/`. To avoid IAM role duplication errors, it is preferable that the GEPP SRE or Lecturer execute them prior to your exercise. 

## Study Terraform

Open, study and understand the Terraform configuration files in the following order:
1. `variables.tf`. Contains definitions for variables referenced in other files.
2. `terraform.tfvars`. Contains the key-value pairs of the variables defined. 
3. `main.tf`. Contains defaults for Terraform config and the creation of a local zip file.
4. `s3.tf`. Creates two buckets to act as bronze and silver storage layers. Notice the reference to `deb_student`.
5. `lambda.tf`. Creates two AWS Lambda functions and reference the locally created zip file.
6. `step-function.tf`. Creates one AWS Step Function with simple execution of lambdas.

## Execute

First you'll need to update `deb_student` within `terraform.tfvars` with your own value.

Second, open the Python files within `./src/`. The `smontiel` string value is also present in them. Make sure to replace them accordingly with the value you used for `deb_student`.

Third, ask your Lecturer or GEPP SRE for the ARNs output by the Terraform code in `../terraform-pre-class/`. You'll need to validate the values are hardcoded correctly in `./lambda.tf` and `./step-function.tf`

Fourth, initialze the Terraform environment in this directory.

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

Wait until all resources are created. It will take a few minutes.

### Destroy

Once you're done experimenting the AWS UI Console, execute Terraform destroy.

```shell
terrafom destroy
```

Notice all resources to be destroyed. It might take a few minutes longer than creation.