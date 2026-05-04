# title: elb-cross-zone-load-balancing-enabled
# description: Detects Classic Load Balancers without cross-zone load balancing enabled. Equivalent to AWS Config elb-cross-zone-load-balancing-enabled. Maps to FSBP ELB.9 (Medium).
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_elb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elb"
	not resource.attributes.cross_zone_load_balancing
	msg := sprintf("Resource %v.%v: Classic Load Balancer does not have cross-zone load balancing enabled", [resource.type, resource.name])
}
