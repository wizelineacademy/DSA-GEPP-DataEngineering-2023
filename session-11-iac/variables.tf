terraform {
  required_version = ">= 1.4.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

variable "bucket_name" {
  type        = string
  description = "The name of the S3 bucket to create."
}

variable "region" {
  type        = string
  description = "The region in which to create the S3 bucket."
}

variable "profile" {
  type        = string
  description = "The Profile you will use to interact with AWS account."
}