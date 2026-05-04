# title: api-gw-ssl-enabled
# description: Detects API Gateway REST stages without an SSL client certificate for backend authentication. Equivalent to AWS Config api-gw-ssl-enabled. Maps to FSBP APIGateway.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_stage
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_stage"
	not resource.attributes.client_certificate_id
	msg := sprintf("Resource %v.%v: API Gateway stage does not have an SSL client certificate configured", [resource.type, resource.name])
}
