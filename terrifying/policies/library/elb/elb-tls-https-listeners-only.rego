# title: elb-tls-https-listeners-only
# description: Detects Classic Load Balancers with HTTP or TCP listeners that lack TLS encryption. Equivalent to AWS Config elb-tls-https-listeners-only. Maps to FSBP ELB.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_elb
package terrifying

import rego.v1

insecure_protocols := {"HTTP", "TCP"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elb"
	listener := resource.attributes.listener[_]
	listener.lb_protocol in insecure_protocols
	msg := sprintf("Resource %v.%v: Classic Load Balancer has an unencrypted %v listener", [resource.type, resource.name, listener.lb_protocol])
}
