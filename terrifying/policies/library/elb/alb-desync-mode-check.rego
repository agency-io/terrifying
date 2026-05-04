# title: alb-desync-mode-check
# description: Detects Application Load Balancers where HTTP desync mitigation mode is not set to defensive or strictest. Equivalent to AWS Config alb-desync-mode-check. Maps to FSBP ELB.12 (Medium).
# severity: Medium
# tags: security-hub, fsbp, pci-dss, conformance-pack
# terraform_resources: aws_lb
package terrifying

import rego.v1

approved_modes := {"defensive", "strictest"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	desync_mode := resource.attributes.desync_mitigation_mode
	not desync_mode in approved_modes
	msg := sprintf("Resource %v.%v: ALB has desync mitigation mode set to '%v' instead of defensive or strictest", [resource.type, resource.name, desync_mode])
}
