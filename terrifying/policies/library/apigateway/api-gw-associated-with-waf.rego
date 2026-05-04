# title: api-gw-associated-with-waf
# description: Detects REST API Gateway stages not associated with a WAF Web ACL. Equivalent to AWS Config api-gw-associated-with-waf. Maps to FSBP APIGateway.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_stage
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_stage"
	not resource.attributes.web_acl_arn
	msg := sprintf("Resource %v.%v: API Gateway stage is not associated with a WAF Web ACL", [resource.type, resource.name])
}
