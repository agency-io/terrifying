# title: autoscaling-multiple-az
# description: Detects Auto Scaling groups configured with fewer than two Availability Zones, creating a single point of failure. Equivalent to AWS Config autoscaling-multiple-az. Maps to FSBP AutoScaling.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_autoscaling_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_autoscaling_group"
	count(resource.attributes.availability_zones) < 2
	msg := sprintf("Resource %v.%v: Auto Scaling group is deployed in only %v Availability Zone(s)", [resource.type, resource.name, count(resource.attributes.availability_zones)])
}
