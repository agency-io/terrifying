# title: kms-key-policy-no-public-access
# description: Detects KMS keys whose key policy grants access to the wildcard principal (*), making cryptographic operations publicly accessible. Equivalent to AWS Config kms-key-policy-no-public-access.
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_kms_key
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_kms_key"
	policy := json.unmarshal(resource.attributes.policy)
	stmt := policy.Statement[_]
	stmt.Effect == "Allow"
	principal_is_public(stmt.Principal)
	not stmt.Condition
	msg := sprintf("Resource %v.%v: KMS key policy grants public access via wildcard principal", [resource.type, resource.name])
}

principal_is_public(principal) if {
	principal == "*"
}

principal_is_public(principal) if {
	principal.AWS == "*"
}

principal_is_public(principal) if {
	"*" in principal.AWS
}
