# title: ecr-private-tag-immutability-enabled
# description: Detects ECR private repositories with mutable image tags, allowing image overwrites. Equivalent to AWS Config ecr-private-tag-immutability-enabled. Maps to FSBP ECR.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecr_repository
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecr_repository"
	resource.attributes.image_tag_mutability != "IMMUTABLE"
	msg := sprintf("Resource %v.%v: ECR repository has mutable image tags enabled", [resource.type, resource.name])
}
