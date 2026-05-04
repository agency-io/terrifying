# title: lambda-dlq-check
# description: Detects Lambda functions without a Dead Letter Queue (DLQ) configured; failed async invocations are silently discarded without one.
# severity: Low
# tags: conformance-pack
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	not resource.attributes.dead_letter_config
	msg := sprintf("Resource %v.%v: Lambda function does not have a Dead Letter Queue configured", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	dlq := resource.attributes.dead_letter_config[_]
	count(dlq.target_arn) == 0
	msg := sprintf("Resource %v.%v: Lambda function does not have a Dead Letter Queue configured", [resource.type, resource.name])
}
