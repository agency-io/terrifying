# title: ec2-instance-no-public-ip
# description: Detects EC2 instances with a public IPv4 address assigned, exposing them directly to the internet.
# severity: High
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_instance
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_instance"
	resource.attributes.associate_public_ip_address == true
	msg := sprintf("Resource %v.%v: EC2 instance has a public IP address assigned", [resource.type, resource.name])
}
