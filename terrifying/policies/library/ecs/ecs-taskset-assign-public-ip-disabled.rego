# title: ecs-taskset-assign-public-ip-disabled
# description: Detects ECS services using an EXTERNAL deployment controller with assign_public_ip enabled, exposing task sets to the internet. Maps to FSBP ECS.16 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_service
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_service"
	resource.attributes.deployment_controller[_].type == "EXTERNAL"
	resource.attributes.network_configuration[_].assign_public_ip == true
	msg := sprintf("Resource %v.%v: ECS service uses EXTERNAL deployment controller with assign_public_ip enabled", [resource.type, resource.name])
}
