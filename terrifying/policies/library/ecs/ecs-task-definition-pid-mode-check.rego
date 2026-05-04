# title: ecs-task-definition-pid-mode-check
# description: Detects ECS task definitions with pidMode=host, sharing the host process namespace and breaking container isolation. Equivalent to AWS Config ecs-task-definition-pid-mode-check. Maps to FSBP ECS.3 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_task_definition
package terrifying

import rego.v1

# Note: Full container-level inspection requires parsing container_definitions JSON.
# This policy checks that container_definitions is configured.
deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_task_definition"
	resource.attributes.pid_mode == "host"
	msg := sprintf("Resource %v.%v: task definition uses host PID mode", [resource.type, resource.name])
}
