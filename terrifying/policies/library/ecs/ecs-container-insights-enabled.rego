# title: ecs-container-insights-enabled
# description: Detects ECS clusters where Container Insights is not enabled. Equivalent to AWS Config ecs-container-insights-enabled. Maps to FSBP ECS.12 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_cluster"
	not container_insights_enabled(resource)
	msg := sprintf("Resource %v.%v: ECS cluster does not have Container Insights enabled", [resource.type, resource.name])
}

container_insights_enabled(resource) if {
	some setting in resource.attributes.setting
	setting.name == "containerInsights"
	setting.value == "enabled"
}
