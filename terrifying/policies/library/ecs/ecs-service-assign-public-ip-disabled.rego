# title: ecs-service-assign-public-ip-disabled
# description: Detects ECS services with assignPublicIp enabled in awsvpc network configuration, exposing tasks directly to the internet. Equivalent to AWS Config ecs-service-assign-public-ip-disabled. Maps to FSBP ECS.2 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_ecs_service
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecs_service"
	resource.attributes.network_configuration[_].assign_public_ip == true
	msg := sprintf("Resource %v.%v: ECS service has assign_public_ip enabled in its network configuration", [resource.type, resource.name])
}
