# title: lambda-function-public-access-prohibited
# description: Detects Lambda functions with resource-based policies that allow public access (Principal: "*").
# severity: Critical
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	policy := json.unmarshal(resource.attributes.policy)
	stmt := policy.Statement[_]
	is_public_principal(stmt.Principal)
	msg := sprintf("Resource %v.%v: Lambda function has a resource-based policy that allows public access", [resource.type, resource.name])
}

is_public_principal(principal) if {
	principal == "*"
}

is_public_principal(principal) if {
	principal.AWS == "*"
}

is_public_principal(principal) if {
	"*" in principal.AWS
}
