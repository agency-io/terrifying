# title: elb-deletion-protection-enabled
# description: Detects Application and Network Load Balancers without deletion protection enabled. Equivalent to AWS Config elb-deletion-protection-enabled. Maps to FSBP ELB.6 (Medium).
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_lb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	not resource.attributes.enable_deletion_protection
	msg := sprintf("Resource %v.%v: Load balancer does not have deletion protection enabled", [resource.type, resource.name])
}
