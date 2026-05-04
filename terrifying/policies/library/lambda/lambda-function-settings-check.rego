# title: lambda-function-settings-check
# description: Detects Lambda functions using deprecated or end-of-life runtimes. Equivalent to AWS Config lambda-function-settings-check.
# severity: High
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_lambda_function
package terrifying

import rego.v1

deprecated_runtimes := {
	"python2.7",
	"python3.6",
	"python3.7",
	"nodejs10.x",
	"nodejs12.x",
	"nodejs14.x",
	"ruby2.5",
	"java8",
	"go1.x",
	"dotnet5.0",
	"dotnet3.1",
	"dotnetcore2.1",
	"dotnetcore3.1",
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lambda_function"
	resource.attributes.runtime in deprecated_runtimes
	msg := sprintf("Resource %v.%v: Lambda function uses deprecated runtime '%v'", [resource.type, resource.name, resource.attributes.runtime])
}
