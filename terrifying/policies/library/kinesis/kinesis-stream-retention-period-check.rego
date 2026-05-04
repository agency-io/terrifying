# title: kinesis-stream-retention-period-check
# description: Detects Kinesis Data Streams with a retention period below 168 hours (7 days). Equivalent to AWS Config kinesis-stream-retention-period-check.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_kinesis_stream
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_kinesis_stream"
	resource.attributes.retention_period < 168
	msg := sprintf("Resource %v.%v: Kinesis stream retention period is %v hours (minimum: 168)", [resource.type, resource.name, resource.attributes.retention_period])
}
