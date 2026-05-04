# title: lambda-function-xray-enabled
# description: Detects Lambda functions that do not have AWS X-Ray active tracing enabled.
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	not resource.attributes.tracing_config
	msg := sprintf("Resource %v.%v: Lambda function does not have X-Ray active tracing enabled", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	tracing := resource.attributes.tracing_config[_]
	tracing.mode != "Active"
	msg := sprintf("Resource %v.%v: Lambda function does not have X-Ray active tracing enabled (mode: %v)", [resource.type, resource.name, tracing.mode])
}
