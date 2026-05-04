# title: cloud-trail-log-file-validation-enabled
# description: Detects CloudTrail trails with log file validation disabled. Without validation, tampered or deleted log files cannot be detected. Equivalent to AWS Config cloud-trail-log-file-validation-enabled. Maps to CT Mandatory, FSBP CloudTrail.4, CIS 3.2, PCI DSS.
# severity: High
# tags: control-tower, control-tower-mandatory, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_cloudtrail
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudtrail"
	not resource.attributes.enable_log_file_validation
	msg := sprintf("Resource %v.%v: CloudTrail trail does not have log file validation enabled", [resource.type, resource.name])
}
