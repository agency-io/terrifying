# title: lambda-inside-vpc
# description: Detects Lambda functions that are not configured to run inside a VPC.
# severity: Medium
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	not resource.attributes.vpc_config
	msg := sprintf("Resource %v.%v: Lambda function is not configured inside a VPC", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	vpc_config := resource.attributes.vpc_config[_]
	not vpc_config.subnet_ids
	msg := sprintf("Resource %v.%v: Lambda function is not configured inside a VPC", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	vpc_config := resource.attributes.vpc_config[_]
	count(vpc_config.subnet_ids) == 0
	msg := sprintf("Resource %v.%v: Lambda function is not configured inside a VPC", [resource.type, resource.name])
}
