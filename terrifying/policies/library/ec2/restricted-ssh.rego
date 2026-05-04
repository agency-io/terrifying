# title: restricted-ssh
# description: Detects security groups allowing unrestricted SSH (port 22) inbound from 0.0.0.0/0 or ::/0.
# severity: High
# tags: control-tower, control-tower-strongly-recommended, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_security_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	rule.from_port <= 22
	rule.to_port >= 22
	cidr := rule.cidr_blocks[_]
	cidr == "0.0.0.0/0"
	msg := sprintf("Resource %v.%v: SSH port 22 is open to 0.0.0.0/0", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	rule.from_port <= 22
	rule.to_port >= 22
	cidr := rule.ipv6_cidr_blocks[_]
	cidr == "::/0"
	msg := sprintf("Resource %v.%v: SSH port 22 is open to ::/0", [resource.type, resource.name])
}
