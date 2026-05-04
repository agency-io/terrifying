# title: cmk-backing-key-rotation-enabled
# description: Detects customer-managed KMS keys (CMKs) that do not have automatic key rotation enabled.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_kms_key
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_kms_key"
	not resource.attributes.enable_key_rotation
	msg := sprintf("Resource %v.%v: KMS key rotation is not enabled", [resource.type, resource.name])
}
