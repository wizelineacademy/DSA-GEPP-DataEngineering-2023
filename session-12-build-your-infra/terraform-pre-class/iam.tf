# =====================================================
# -------------------- LAMBDA ROLE --------------------
# =====================================================

# Allow AWS Lambda to Assume a Role
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Role for AWS Lambda with AssumeRole
resource "aws_iam_role" "iam_for_lambda" {
  name               = "${var.deb_session}_iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

# Attach the S3 Full Access Policy to the Lambda Role
resource "aws_iam_role_policy_attachment" "lambda-s3-full-access-attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Attach the Lambda Basic Role policy
resource "aws_iam_role_policy_attachment" "lambda-basic-exec-attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ======================================================
# ----------------- STEP FUNCTION ROLE -----------------
# ======================================================

# Allow AWS Step Functions to Assume a Role
data "aws_iam_policy_document" "step_function_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Role for AWS Lambda with AssumeRole
resource "aws_iam_role" "iam_for_step_function" {
  name               = "${var.deb_session}_iam_for_step_function"
  assume_role_policy = data.aws_iam_policy_document.step_function_assume_role.json
}

# Policy with Invoke Lambda permissions
resource "aws_iam_policy" "policy_invoke_lambda" {
  name        = "stepFunctionSampleLambdaFunctionInvocationPolicy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

# Attach Lambda invoke policy to IAM Role for Step Function
resource "aws_iam_role_policy_attachment" "iam_for_sfn_attach_policy_invoke_lambda" {
  role       = "${aws_iam_role.iam_for_step_function.name}"
  policy_arn = "${aws_iam_policy.policy_invoke_lambda.arn}"
}
