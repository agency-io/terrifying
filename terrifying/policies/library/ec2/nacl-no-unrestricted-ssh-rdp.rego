# title: nacl-no-unrestricted-ssh-rdp
# description: Detects Network ACLs with ALLOW rules permitting ingress from 0.0.0.0/0 on SSH (22) or RDP (3389). Equivalent to AWS Config nacl-no-unrestricted-ssh-rdp. Maps to FSBP EC2.21 (Medium).
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_network_acl_rule
package terrifying

import rego.v1

sensitive_ports := {22, 3389}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_network_acl_rule"
	resource.attributes.rule_action == "allow"
	resource.attributes.egress == false
	some port in sensitive_ports
	resource.attributes.from_port <= port
	resource.attributes.to_port >= port
	resource.attributes.cidr_block == "0.0.0.0/0"
	msg := sprintf("Resource %v.%v: NACL rule allows unrestricted ingress on port %v from 0.0.0.0/0", [resource.type, resource.name, port])
}
