# title: no-unrestricted-route-to-igw
# description: Detects route tables with a 0.0.0.0/0 route pointing to an internet gateway, exposing all traffic to the internet. Maps to FSBP EC2.51 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_route
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_route"
	resource.attributes.destination_cidr_block == "0.0.0.0/0"
	startswith(resource.attributes.gateway_id, "igw-")
	msg := sprintf("Resource %v.%v: route has an unrestricted route (0.0.0.0/0) to an internet gateway", [resource.type, resource.name])
}
