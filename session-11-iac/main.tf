resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name

  tags = {
    Name        = "My S3 Bucket for DSE-GEPP Bootcamp 2023"
    Environment = "dev"
  }
}
