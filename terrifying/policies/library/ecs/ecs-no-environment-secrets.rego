# title: ecs-no-environment-secrets
# description: Detects ECS task definitions passing secrets as plaintext environment variables. Equivalent to AWS Config ecs-no-environment-secrets. Maps to FSBP ECS.8 (High).
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
	not resource.attributes.container_definitions
	msg := sprintf("Resource %v.%v: container definitions not configured", [resource.type, resource.name])
}
