# title: iam-password-policy
# description: Detects accounts with a weak IAM password policy. Equivalent to AWS Config iam-password-policy.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_iam_account_password_policy
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_account_password_policy"
	resource.attributes.minimum_password_length < 14
	msg := sprintf("Resource %v.%v: password policy minimum length is %v (required: 14)", [resource.type, resource.name, resource.attributes.minimum_password_length])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_account_password_policy"
	not resource.attributes.require_uppercase_characters
	msg := sprintf("Resource %v.%v: password policy does not require uppercase characters", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_account_password_policy"
	not resource.attributes.require_lowercase_characters
	msg := sprintf("Resource %v.%v: password policy does not require lowercase characters", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_account_password_policy"
	not resource.attributes.require_symbols
	msg := sprintf("Resource %v.%v: password policy does not require symbols", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_account_password_policy"
	not resource.attributes.require_numbers
	msg := sprintf("Resource %v.%v: password policy does not require numbers", [resource.type, resource.name])
}
