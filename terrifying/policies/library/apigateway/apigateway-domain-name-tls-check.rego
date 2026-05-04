# title: apigateway-domain-name-tls-check
# description: Detects API Gateway custom domain names not using TLS 1.2 security policy. Equivalent to AWS Config apigateway-domain-name-tls-check. Maps to FSBP APIGateway.11 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_domain_name
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_domain_name"
	resource.attributes.security_policy != "TLS_1_2"
	msg := sprintf("Resource %v.%v: API Gateway domain name uses security policy '%v' instead of TLS_1_2", [resource.type, resource.name, resource.attributes.security_policy])
}
