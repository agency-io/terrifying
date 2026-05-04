# title: lambda-concurrency-check
# description: Detects Lambda functions without reserved concurrency configured. Equivalent to AWS Config lambda-concurrency-check.
# severity: Medium
# tags: conformance-pack
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	not resource.attributes.reserved_concurrent_executions
	msg := sprintf("Resource %v.%v: Lambda function has no reserved concurrency configured", [resource.type, resource.name])
}
