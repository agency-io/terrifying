# title: ec2-launch-template-public-ip-disabled
# description: Detects EC2 launch templates with AssociatePublicIpAddress enabled on any network interface. Equivalent to AWS Config ec2-launch-template-public-ip-disabled. Maps to FSBP EC2.25 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_launch_template
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_launch_template"
	ni := resource.attributes.network_interfaces[_]
	ni.associate_public_ip_address == true
	msg := sprintf("Resource %v.%v: EC2 launch template has associate_public_ip_address=true on a network interface", [resource.type, resource.name])
}
