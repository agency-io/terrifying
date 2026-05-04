# title: alb-waf-enabled
# description: Detects Application Load Balancers not associated with a WAFv2 web ACL. Equivalent to AWS Config alb-waf-enabled. Maps to FSBP ELB.16 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_lb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	not resource.attributes.web_acl_arn
	msg := sprintf("Resource %v.%v: ALB is not associated with a WAF Web ACL", [resource.type, resource.name])
}
