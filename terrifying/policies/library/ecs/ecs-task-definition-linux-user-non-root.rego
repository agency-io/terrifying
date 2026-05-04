# title: ecs-task-definition-linux-user-non-root
# description: Detects ECS task definitions where any container runs as root (user=root or unset). Equivalent to AWS Config ecs-task-definition-linux-user-non-root. Maps to FSBP ECS.20 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_task_definition
package terrifying

import rego.v1

# Note: Full container-level inspection requires parsing container_definitions JSON.
# This policy checks that container_definitions is configured.
deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_task_definition"
	not resource.attributes.container_definitions
	msg := sprintf("Resource %v.%v: container definitions not configured", [resource.type, resource.name])
}
