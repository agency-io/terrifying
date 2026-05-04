# title: iam-user-group-membership-check
# description: Detects IAM users not assigned to at least one IAM group. Equivalent to AWS Config iam-user-group-membership-check.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_iam_user
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_user"
	not resource.attributes.groups
	msg := sprintf("Resource %v.%v: IAM user is not a member of any IAM group", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_user"
	count(resource.attributes.groups) == 0
	msg := sprintf("Resource %v.%v: IAM user is not a member of any IAM group", [resource.type, resource.name])
}
