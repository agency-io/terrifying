# title: lambda-vpc-multi-az-check
# description: Detects VPC-connected Lambda functions configured with fewer than 2 subnets, indicating single-AZ placement. Equivalent to AWS Config lambda-vpc-multi-az-check.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	vpc_config := resource.attributes.vpc_config[_]
	subnets := vpc_config.subnet_ids
	count(subnets) > 0
	count(subnets) < 2
	msg := sprintf("Resource %v.%v: Lambda function is configured with only %v subnet(s); at least 2 required for multi-AZ", [resource.type, resource.name, count(subnets)])
}
