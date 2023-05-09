variable "name" {
  description = "Name of MWAA Environment"
  default     = "MyAirflowEnvironmentGEPP"
  type        = string
}

variable "region" {
  description = "region"
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "Default tags"
  default     = {"env": "test", "dept": "AWS Developer Relations"}
  type        = map(string)
}

variable "vpc_cidr" {
  description = "VPC CIDR for MWAA"
  type        = string
  default     = "10.1.0.0/16"
}

variable "airflow_config_backend_kwargs" {
  type        = map(string)
  description = "It tells Airflow to look for the secret at the airflow/connections/* and airflow/variables/* path."
}
