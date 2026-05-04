# title: cognito-user-pool-mfa-enabled
# description: Detects Cognito user pools with MFA disabled. Equivalent to AWS Config cognito-user-pool-mfa-enabled. Maps to FSBP Cognito.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cognito_user_pool
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cognito_user_pool"
	resource.attributes.mfa_configuration == "OFF"
	msg := sprintf("Resource %v.%v: Cognito user pool has MFA disabled", [resource.type, resource.name])
}
