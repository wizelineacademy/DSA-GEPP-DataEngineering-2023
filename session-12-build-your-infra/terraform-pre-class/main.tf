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
