# title: ecs-fargate-latest-platform-version
# description: Detects ECS Fargate services not running on the latest platform version. Equivalent to AWS Config ecs-fargate-latest-platform-version. Maps to FSBP ECS.10 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_service
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_service"
	resource.attributes.launch_type == "FARGATE"
	resource.attributes.platform_version != "LATEST"
	msg := sprintf("Resource %v.%v: ECS Fargate service is not using the latest platform version (current: %v)", [resource.type, resource.name, resource.attributes.platform_version])
}
