# title: elbv2-acm-certificate-required
# description: Detects ALB/NLB HTTPS or TLS listeners using certificates not managed by ACM, risking expiry-related outages. Maps to NIST SP 800-53 SC-8 (Medium).
# severity: Medium
# tags: security-hub, nist-800-53
# terraform_resources: aws_lb_listener
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb_listener"
	resource.attributes.protocol in {"HTTPS", "TLS"}
	cert := resource.attributes.certificate_arn
	not startswith(cert, "arn:aws:acm:")
	msg := sprintf("Resource %v.%v: Load balancer listener uses a non-ACM certificate", [resource.type, resource.name])
}
