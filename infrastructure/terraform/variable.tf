variable "aws_region" {
  default = "us-east-1"
}

variable "lambda_function_name" {
  default = "soc-remediation-function"
}

variable "dynamodb_table_name" {
  default = "soc-idempotency-table"
}