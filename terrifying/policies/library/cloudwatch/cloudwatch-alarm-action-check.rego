# title: cloudwatch-alarm-action-check
# description: Detects CloudWatch alarms with no actions configured on AlarmActions, OKActions, or InsufficientDataActions. Equivalent to AWS Config cloudwatch-alarm-action-check. Maps to FSBP CloudWatch.15 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_cloudwatch_metric_alarm
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudwatch_metric_alarm"
	count(object.get(resource.attributes, "alarm_actions", [])) == 0
	count(object.get(resource.attributes, "ok_actions", [])) == 0
	count(object.get(resource.attributes, "insufficient_data_actions", [])) == 0
	msg := sprintf("Resource %v.%v: CloudWatch alarm has no actions configured for any state", [resource.type, resource.name])
}
