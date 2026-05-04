# title: iam-no-inline-policy-check
# description: Detects IAM users with inline policies attached directly; inline policies should be replaced with managed policies attached via groups.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_iam_user_policy
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_user_policy"
	msg := sprintf("Resource %v.%v: inline IAM policy attached directly to user; replace with managed policies", [resource.type, resource.name])
}
