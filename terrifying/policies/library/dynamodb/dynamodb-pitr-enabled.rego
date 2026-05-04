# title: dynamodb-pitr-enabled
# description: Detects DynamoDB tables without point-in-time recovery enabled. Equivalent to AWS Config dynamodb-pitr-enabled. Maps to FSBP DynamoDB.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_dynamodb_table
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_dynamodb_table"
	not pitr_enabled(resource)
	msg := sprintf("Resource %v.%v: DynamoDB table does not have point-in-time recovery enabled", [resource.type, resource.name])
}

pitr_enabled(resource) if {
	resource.attributes.point_in_time_recovery[_].enabled == true
}
