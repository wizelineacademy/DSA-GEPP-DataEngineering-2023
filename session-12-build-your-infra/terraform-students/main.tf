# ============================================================================
# ------------------------ GCP Provider Auth & Config ------------------------
# ============================================================================

terraform {
  required_version = "~> 1.4.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.39.0"
    }
  }
}

# No alias set, makes all Terraform resources use this provider by default
provider "aws" {
  allowed_account_ids = [var.aws_account]
  region              = var.aws_region
}

provider "archive" {}

# This automatically zips the Python files everytime they change
data "archive_file" "src_zip" {
  type        = "zip"
  source_dir = "${path.module}/src" 
  excludes    = ["${path.module}/src/.DS_Store"]
  output_path = "${path.module}/src_zip/simple_lambdas.zip"
}
