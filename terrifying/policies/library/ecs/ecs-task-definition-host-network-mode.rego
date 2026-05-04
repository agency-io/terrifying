# title: ecs-task-definition-host-network-mode
# description: Detects ECS task definitions using host network mode, which bypasses container network isolation. Equivalent to AWS Config ecs-task-definition-host-network-mode. Maps to FSBP ECS.17 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_task_definition
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_task_definition"
	resource.attributes.network_mode == "host"
	msg := sprintf("Resource %v.%v: ECS task definition uses host network mode", [resource.type, resource.name])
}
