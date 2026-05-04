# title: elbv2-multiple-az
# description: Detects Application and Network Load Balancers deployed in fewer than two Availability Zones. Equivalent to AWS Config elbv2-multiple-az. Maps to FSBP ELB.13 (Medium).
# severity: Medium
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_lb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	subnets := resource.attributes.subnets
	count(subnets) < 2
	msg := sprintf("Resource %v.%v: Load balancer is configured with fewer than 2 subnets (Availability Zones)", [resource.type, resource.name])
}
