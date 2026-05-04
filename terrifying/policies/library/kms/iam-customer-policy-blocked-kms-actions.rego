# title: iam-customer-policy-blocked-kms-actions
# description: Detects customer-managed IAM policies that allow kms:Decrypt or kms:ReEncryptFrom on all resources. Equivalent to AWS Config iam-customer-policy-blocked-kms-actions.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_iam_policy
package terrifying

import rego.v1

blocked_actions := {"kms:Decrypt", "kms:ReEncryptFrom", "kms:decrypt", "kms:reencryptfrom"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_policy"
	policy := json.unmarshal(resource.attributes.policy)
	stmt := policy.Statement[_]
	stmt.Effect == "Allow"
	resource_entry := stmt.Resource[_]
	resource_entry == "*"
	action := stmt.Action[_]
	lower(action) in {"kms:decrypt", "kms:reencryptfrom"}
	msg := sprintf("Resource %v.%v: IAM policy allows blocked KMS action '%v' on all resources", [resource.type, resource.name, action])
}
