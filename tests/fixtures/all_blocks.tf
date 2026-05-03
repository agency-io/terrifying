variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

output "bucket_arn" {
  description = "The bucket ARN"
  value       = "aws_s3_bucket.main.arn"
}

locals {
  env = "prod"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
}
