# title: cognito-user-pool-password-policy
# description: Detects Cognito user pools with weak password policies (minimum length < 14 or missing character type requirements). Maps to FSBP Cognito.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cognito_user_pool
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cognito_user_pool"
	weak_password_policy(resource)
	msg := sprintf("Resource %v.%v: Cognito user pool has a weak password policy", [resource.type, resource.name])
}

weak_password_policy(resource) if {
	resource.attributes.password_policy[_].minimum_length < 14
}

weak_password_policy(resource) if {
	resource.attributes.password_policy[_].require_uppercase == false
}

weak_password_policy(resource) if {
	resource.attributes.password_policy[_].require_lowercase == false
}

weak_password_policy(resource) if {
	resource.attributes.password_policy[_].require_numbers == false
}

weak_password_policy(resource) if {
	resource.attributes.password_policy[_].require_symbols == false
}
