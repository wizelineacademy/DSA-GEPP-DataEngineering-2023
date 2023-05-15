# S12 - Build your own Infrastructure

This is a 100% practical session. Students will recall the exercise from `Session 4 - Data Pipelines`. In this exercise, they will re-deploy the same Python code to AWS Lambdas using Terraform instead of the AWS UI Console. 

## Setup

The terraform files for this Session are split in two. 

1. `terraform-pre-class`. Creates two IAM roles to be used by multiple students for AWS Lambda and AWS Step Functions. Outputs the ARN of those roles to be hardcoded into the other Terraform files.

2. `terraform-students`. Creates two executable AWS Lambda functions and one state machine in AWS Step Functions.

> NOTE: Before the exercise, the first one must be applied successfully. Confirm the names of the roles and hardcode them in `terraform-students/lambda.tf` and `terraform-students/step-function.tf`

To run `terraform-pre-class` you'll need permissions to create IAM Roles. Usually this will be executed by the lecturer or the GEPP SRE to avoid duplication issues.

## Exercises

This is a Terraform deployment of the same Python scripts from Session 4. You'll go back and forth between the AWS UI Console and the files in `terraform-students`

### Study the Python files

The files are located in `./terraform-students/src/`

These are the exact same files with a few added comments where you'll find insights, questions and complementing comments. Make sure to read them and feel free to add your own logs. Do not worry, adding prints or logs will not impact the exercise deploying and running successfully. 

If you wish to modify the behavior of the scripts, be extremely careful. You might need to add or alter more pieces of the Terraform code.

### Study and Apply Terraform Code

Make sure to read and follow the README within `./terraform-pre-class` and `./terraform-students`. The instructions will also guide you through the `destroy` phase.
