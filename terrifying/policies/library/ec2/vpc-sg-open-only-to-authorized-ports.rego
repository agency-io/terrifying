# title: vpc-sg-open-only-to-authorized-ports
# description: Detects security groups with ingress rules permitting unrestricted access (0.0.0.0/0 or ::/0) on ports other than 80 and 443. Equivalent to FSBP EC2.18 (High).
# severity: High
# tags: security-hub, fsbp, pci-dss
# terraform_resources: aws_security_group
package terrifying

import rego.v1

authorized_ports := {80, 443}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	cidr := rule.cidr_blocks[_]
	cidr == "0.0.0.0/0"
	not only_authorized_ports(rule)
	msg := sprintf("Resource %v.%v: security group has an ingress rule allowing unrestricted access from 0.0.0.0/0 on non-authorized ports", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	cidr := rule.ipv6_cidr_blocks[_]
	cidr == "::/0"
	not only_authorized_ports(rule)
	msg := sprintf("Resource %v.%v: security group has an ingress rule allowing unrestricted access from ::/0 on non-authorized ports", [resource.type, resource.name])
}

only_authorized_ports(rule) if {
	rule.from_port in authorized_ports
	rule.to_port in authorized_ports
	rule.from_port == rule.to_port
}
