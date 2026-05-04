# title: restricted-common-ports
# description: Detects security groups allowing unrestricted inbound access on high-risk ports (3389/RDP, 3306/MySQL, 5432/PostgreSQL) from 0.0.0.0/0.
# severity: High
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_security_group
package terrifying

import rego.v1

restricted_ports := {3389, 3306, 5432}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	some port in restricted_ports
	rule.from_port <= port
	rule.to_port >= port
	cidr := rule.cidr_blocks[_]
	cidr == "0.0.0.0/0"
	msg := sprintf("Resource %v.%v: port %v is open to 0.0.0.0/0", [resource.type, resource.name, port])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_security_group"
	rule := resource.attributes.ingress[_]
	some port in restricted_ports
	rule.from_port <= port
	rule.to_port >= port
	cidr := rule.ipv6_cidr_blocks[_]
	cidr == "::/0"
	msg := sprintf("Resource %v.%v: port %v is open to ::/0", [resource.type, resource.name, port])
}
