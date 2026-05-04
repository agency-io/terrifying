# title: dynamodb-autoscaling-enabled
# description: Detects DynamoDB tables using PROVISIONED billing mode without auto-scaling configured. Equivalent to AWS Config dynamodb-autoscaling-enabled. Maps to FSBP DynamoDB.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_dynamodb_table
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_dynamodb_table"
	is_provisioned(resource)
	not has_autoscaling(resource)
	msg := sprintf("Resource %v.%v: DynamoDB table uses PROVISIONED billing mode but does not have auto-scaling configured", [resource.type, resource.name])
}

is_provisioned(resource) if {
	resource.attributes.billing_mode == "PROVISIONED"
}

is_provisioned(resource) if {
	not resource.attributes.billing_mode
}

has_autoscaling(resource) if {
	resource.attributes.read_capacity_autoscaling_settings
	resource.attributes.write_capacity_autoscaling_settings
}
