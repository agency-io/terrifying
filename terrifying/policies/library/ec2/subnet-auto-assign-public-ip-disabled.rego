# title: subnet-auto-assign-public-ip-disabled
# description: Detects EC2 subnets with MapPublicIpOnLaunch enabled, which automatically assigns public IPs to instances.
# severity: Medium
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_subnet
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_subnet"
	resource.attributes.map_public_ip_on_launch == true
	msg := sprintf("Resource %v.%v: subnet auto-assigns public IPs", [resource.type, resource.name])
}
