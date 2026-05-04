# title: cloud-trail-encryption-enabled
# description: Detects CloudTrail trails without KMS encryption at rest.
# severity: Medium
# tags: control-tower, control-tower-mandatory, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_cloudtrail
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudtrail"
	not resource.attributes.kms_key_id
	msg := sprintf("Resource %v.%v: CloudTrail trail does not have KMS encryption enabled", [resource.type, resource.name])
}
