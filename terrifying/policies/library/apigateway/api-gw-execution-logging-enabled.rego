# title: api-gw-execution-logging-enabled
# description: Detects API Gateway REST stages with execution logging disabled or not configured. Equivalent to AWS Config api-gw-execution-logging-enabled. Maps to FSBP APIGateway.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_stage
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_stage"
	not resource.attributes.access_log_settings
	msg := sprintf("Resource %v.%v: API Gateway stage does not have execution logging enabled", [resource.type, resource.name])
}
