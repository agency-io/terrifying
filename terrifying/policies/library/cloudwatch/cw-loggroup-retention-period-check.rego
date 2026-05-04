# title: cw-loggroup-retention-period-check
# description: Detects CloudWatch Logs log groups with no retention policy set, retaining logs indefinitely. Equivalent to AWS Config cw-loggroup-retention-period-check. Maps to FSBP CloudWatch.16 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudwatch_log_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudwatch_log_group"
	not resource.attributes.retention_in_days
	msg := sprintf("Resource %v.%v: CloudWatch log group has no retention policy set (logs retained indefinitely)", [resource.type, resource.name])
}
