# title: autoscaling-launch-config-public-ip-disabled
# description: Detects Auto Scaling launch configurations with AssociatePublicIpAddress enabled, exposing instances directly to the internet. Equivalent to AWS Config autoscaling-launch-config-public-ip-disabled. Maps to FSBP AutoScaling.5 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_launch_configuration
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_launch_configuration"
	resource.attributes.associate_public_ip_address == true
	msg := sprintf("Resource %v.%v: Launch configuration has associate_public_ip_address=true", [resource.type, resource.name])
}
