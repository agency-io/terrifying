# title: elb-acm-certificate-required
# description: Detects Classic Load Balancers with HTTPS/SSL listeners using non-ACM certificates. Equivalent to AWS Config elb-acm-certificate-required. Maps to FSBP ELB.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_elb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elb"
	listener := resource.attributes.listener[_]
	listener.lb_protocol in {"HTTPS", "SSL"}
	not startswith(listener.ssl_certificate_id, "arn:aws:acm:")
	msg := sprintf("Resource %v.%v: Classic Load Balancer has a HTTPS/SSL listener using a non-ACM certificate", [resource.type, resource.name])
}
