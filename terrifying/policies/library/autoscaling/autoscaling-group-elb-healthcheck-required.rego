# title: autoscaling-group-elb-healthcheck-required
# description: Detects Auto Scaling groups associated with a load balancer but not using ELB health checks. Equivalent to AWS Config autoscaling-group-elb-healthcheck-required. Maps to FSBP AutoScaling.1 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_autoscaling_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_autoscaling_group"
	has_load_balancer(resource)
	resource.attributes.health_check_type != "ELB"
	msg := sprintf("Resource %v.%v: Auto Scaling group has load balancers attached but health check type is '%v' instead of ELB", [resource.type, resource.name, resource.attributes.health_check_type])
}

has_load_balancer(resource) if {
	count(resource.attributes.load_balancers) > 0
}

has_load_balancer(resource) if {
	count(resource.attributes.target_group_arns) > 0
}
