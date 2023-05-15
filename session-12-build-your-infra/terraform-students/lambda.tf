resource "aws_lambda_function" "load_lambda" {
  # Name as it appears on the UI
  function_name = "deb_load_by_${var.deb_student}"

  # Hardcoded AWS Role ARN this Lambda will require
  # Pre-created by ../terraform-pre-class/iam.tf
  # Make sure to confirm ARN when re-deploying
  role          = "arn:aws:iam::908781576184:role/deb_s12_iam_for_lambda"

  # Environment Setup
  runtime       = "python3.9"
  layers        = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:6"] 
  timeout       = 180

  # Code Deployed
  filename      = data.archive_file.src_zip.output_path
  handler       = "load.lambda_handler"

  # Trigger updates with hash changes
  source_code_hash = data.archive_file.src_zip.output_base64sha256
}


resource "aws_lambda_function" "transform_lambda" {
  # Name as it appears on the UI
  function_name = "deb_transform_by_${var.deb_student}"

  # Hardcoded AWS Role ARN this Lambda will require
  # Pre-created by ../terraform-pre-class/iam.tf
  # Make sure to confirm ARN when re-deploying
  role          = "arn:aws:iam::908781576184:role/deb_s12_iam_for_lambda"

  # Environment Setup
  runtime       = "python3.9"
  layers        = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:6"] 
  timeout       = 360
  # memory_size   = 512
  # memory_size   = 1024
  memory_size   = 2048

  # Code Deployed
  filename      = data.archive_file.src_zip.output_path
  handler       = "transform.lambda_handler"

  # Trigger updates with hash changes
  source_code_hash = data.archive_file.src_zip.output_base64sha256
}
