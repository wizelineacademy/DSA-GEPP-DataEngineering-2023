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
  type          = string
  default       = "my-s3-bucket-john"
  description   = "The name of the S3 bucket to create."
}

variable "region" {
  type          = string
  default       = "us-east-1"
  description   = "The region in which to create the S3 bucket."
}

variable "profile" {
  type          = string
  default       = "dsa-gepp"
  description   = "The Profile you will use to interact with AWS account."
}