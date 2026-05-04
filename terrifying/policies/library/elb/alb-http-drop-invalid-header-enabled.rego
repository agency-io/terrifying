# title: alb-http-drop-invalid-header-enabled
# description: Detects Application Load Balancers where dropping invalid HTTP headers is not enabled. Equivalent to AWS Config alb-http-drop-invalid-header-enabled. Maps to FSBP ELB.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_lb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	not resource.attributes.drop_invalid_header_fields
	msg := sprintf("Resource %v.%v: ALB does not have HTTP invalid header dropping enabled", [resource.type, resource.name])
}
