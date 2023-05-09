# Configuration values
provider "aws" {
  region = var.region
}

# data sources 
data "aws_availability_zones" "available" {}

data "aws_caller_identity" "current" {}

# availability zones and bucket name
locals {
  azs         = slice(data.aws_availability_zones.available.names, 0, 2)
  # bucket_name = format("%s-%s", "aws-ia-mwaa", data.aws_caller_identity.current.account_id)
  bucket_name = "mwaa-gepp-bootcamp-terraform"
}

# Create an S3 bucket with appropiate permissions and upload sample DAG
resource "aws_s3_bucket" "this" {
  bucket = local.bucket_name
  tags   = var.tags
}

# Set ownership, it will force the ownership to one value that let acl resource be created
resource "aws_s3_bucket_acl" "this" {
  depends_on = [aws_s3_bucket_ownership_controls.this]

  bucket = aws_s3_bucket.this.id
  acl    = "private"
}

# Objects uploaded to the bucket change ownership to the bucket owner
resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Upload DAGS
resource "aws_s3_object" "object1" {
  for_each = fileset("dags/", "*")
  bucket   = aws_s3_bucket.this.id
  key      = "dags/${each.value}"
  source   = "dags/${each.value}"
  etag     = filemd5("dags/${each.value}")
}

# Upload plugins/requirements.txt
resource "aws_s3_object" "reqs" {
  for_each = fileset("mwaa/", "*")
  bucket   = aws_s3_bucket.this.id
  key      = each.value
  source   = "mwaa/${each.value}"
  etag     = filemd5("mwaa/${each.value}")
}

#-----------------------------------------------------------
# NOTE: MWAA Airflow environment takes minimum of 20 mins
#-----------------------------------------------------------
module "mwaa" {
  source            = "aws-ia/mwaa/aws"
  name              = var.name
  airflow_version   = "2.2.2"
  environment_class = "mw1.small"
  create_s3_bucket  = false
  source_bucket_arn = aws_s3_bucket.this.arn
  dag_s3_path       = "dags/"
  airflow_config_backend_kwargs = { "connections_prefix" : "airflow/connections/dev", "variables_prefix" : "airflow/variables/dev" }

  logging_configuration = {
    dag_processing_logs = {
      enabled   = true
      log_level = "INFO"
    }

    scheduler_logs = {
      enabled   = true
      log_level = "WARNING"
    }

    task_logs = {
      enabled   = true
      log_level = "DEBUG"
    }

    webserver_logs = {
      enabled   = true
      log_level = "INFO"
    }

    worker_logs = {
      enabled   = true
      log_level = "INFO"
    }
  }

  airflow_configuration_options = {
    "core.load_default_connections" = "false"
    "core.load_examples"            = "false"
    "webserver.dag_default_view"    = "tree"
    "webserver.dag_orientation"     = "LR"
    "secrets.backend"               = "airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend"
    "secrets.backend_kwargs"        = jsonencode(var.airflow_config_backend_kwargs)
    "logging.logging_level"         = "INFO"
  }

  min_workers        = 1
  max_workers        = 10
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnets

  webserver_access_mode = "PUBLIC_ONLY"   # Default PRIVATE_ONLY for production environments
  source_cidr           = ["10.1.0.0/16"] # Add your IP address to access Airflow UI

  tags = var.tags

}

#---------------------------------------------------------------
# Supporting Resources
#---------------------------------------------------------------
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = var.name
  cidr = var.vpc_cidr

  azs             = local.azs
  public_subnets  = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, 8, k)]
  private_subnets = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, 8, k + 10)]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  tags = var.tags
}
