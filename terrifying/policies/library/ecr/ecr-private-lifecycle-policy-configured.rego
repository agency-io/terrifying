# title: ecr-private-lifecycle-policy-configured
# description: Detects ECR private repositories without a lifecycle policy, risking unbounded image accumulation. Equivalent to AWS Config ecr-private-lifecycle-policy-configured. Maps to FSBP ECR.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecr_lifecycle_policy
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecr_repository"
	not has_lifecycle_policy(resource)
	msg := sprintf("Resource %v.%v: ECR repository does not have a lifecycle policy configured", [resource.type, resource.name])
}

has_lifecycle_policy(resource) if {
	lp := input.resources[_]
	lp.type == "aws_ecr_lifecycle_policy"
	lp.attributes.repository == resource.attributes.name
}
