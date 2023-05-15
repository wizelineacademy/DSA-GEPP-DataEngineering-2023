output "iam_arn_lambda" {
  value = aws_iam_role.iam_for_lambda.arn
}

output "iam_arn_step_function" {
  value = aws_iam_role.iam_for_step_function.arn
}