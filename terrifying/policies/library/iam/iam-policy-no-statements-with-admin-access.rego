# title: iam-policy-no-statements-with-admin-access
# description: Detects customer-managed IAM policies that grant full admin access via Action:* and Resource:* in an Allow statement.
# severity: High
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_iam_policy
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_policy"
	policy := json.unmarshal(resource.attributes.policy)
	stmt := policy.Statement[_]
	stmt.Effect == "Allow"
	stmt.Action == "*"
	stmt.Resource == "*"
	msg := sprintf("Resource %v.%v: IAM policy grants full admin access (*:*)", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_iam_policy"
	policy := json.unmarshal(resource.attributes.policy)
	stmt := policy.Statement[_]
	stmt.Effect == "Allow"
	"*" in stmt.Action
	"*" in stmt.Resource
	msg := sprintf("Resource %v.%v: IAM policy grants full admin access (*:*)", [resource.type, resource.name])
}
