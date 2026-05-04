# title: vpc-default-security-group-closed
# description: Detects VPC default security groups that allow inbound or outbound traffic.
# severity: High
# tags: control-tower, control-tower-mandatory, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_default_security_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_default_security_group"
	count(resource.attributes.ingress) > 0
	msg := sprintf("Resource %v.%v: default security group has inbound rules and should have no rules", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_default_security_group"
	count(resource.attributes.egress) > 0
	msg := sprintf("Resource %v.%v: default security group has outbound rules and should have no rules", [resource.type, resource.name])
}
