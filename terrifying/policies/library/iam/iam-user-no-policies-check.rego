# title: iam-user-no-policies-check
# description: Detects IAM users with directly attached managed or inline policies; users should receive permissions via groups only.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_iam_user_policy
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_user_policy"
	msg := sprintf("Resource %v.%v: inline IAM policy attached directly to user; use groups instead", [resource.type, resource.name])
}
