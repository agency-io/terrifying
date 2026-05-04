# title: dynamodb-table-deletion-protection-enabled
# description: Detects DynamoDB tables without deletion protection enabled. Maps to FSBP DynamoDB.6 (Medium).
# severity: Medium
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_dynamodb_table
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_dynamodb_table"
	not resource.attributes.deletion_protection_enabled
	msg := sprintf("Resource %v.%v: DynamoDB table does not have deletion protection enabled", [resource.type, resource.name])
}
