# title: cloud-trail-cloud-watch-logs-enabled
# description: Detects CloudTrail trails not integrated with CloudWatch Logs.
# severity: Medium
# tags: control-tower, control-tower-mandatory, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_cloudtrail
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudtrail"
	not resource.attributes.cloud_watch_logs_group_arn
	msg := sprintf("Resource %v.%v: CloudTrail trail is not integrated with CloudWatch Logs", [resource.type, resource.name])
}
