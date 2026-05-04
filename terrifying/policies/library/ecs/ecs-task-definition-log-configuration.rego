# title: ecs-task-definition-log-configuration
# description: Detects ECS task definitions where any container lacks a log configuration block. Equivalent to AWS Config ecs-task-definition-log-configuration. Maps to FSBP ECS.9 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_task_definition
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_task_definition"
	not resource.attributes.container_definitions
	msg := sprintf("Resource %v.%v: container definitions not configured", [resource.type, resource.name])
}
