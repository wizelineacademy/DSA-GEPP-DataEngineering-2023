# ============================================================================
# -------------------------- Wizemesh Basic TF Vars --------------------------
# ============================================================================

variable "aws_account" {
  description = "The AWS account_id used to provision resources"
  type        = string
}

variable "aws_region" {
  description = "The AWS default region to be used in resources"
  type        = string
}

variable "deb_session" {
  description = "Short name of the session. To be used for IAM role creation"
  type        = string
}
