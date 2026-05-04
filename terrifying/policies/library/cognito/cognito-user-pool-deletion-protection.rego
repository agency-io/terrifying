# title: cognito-user-pool-deletion-protection
# description: Detects Cognito user pools without deletion protection enabled. Equivalent to AWS Config cognito-user-pool-deletion-protection. Maps to FSBP Cognito.6 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cognito_user_pool
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cognito_user_pool"
	resource.attributes.deletion_protection != "ACTIVE"
	msg := sprintf("Resource %v.%v: Cognito user pool does not have deletion protection enabled", [resource.type, resource.name])
}
