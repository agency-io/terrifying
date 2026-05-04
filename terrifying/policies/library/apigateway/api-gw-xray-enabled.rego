# title: api-gw-xray-enabled
# description: Detects API Gateway REST stages without AWS X-Ray active tracing enabled. Equivalent to AWS Config api-gw-xray-enabled. Maps to FSBP APIGateway.3 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_stage
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_stage"
	not resource.attributes.xray_tracing_enabled
	msg := sprintf("Resource %v.%v: API Gateway stage does not have X-Ray tracing enabled", [resource.type, resource.name])
}
