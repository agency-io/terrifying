# title: ec2-ebs-encryption-by-default
# description: Detects AWS accounts where EBS default encryption is not enabled, allowing unencrypted volumes. Equivalent to AWS Config ec2-ebs-encryption-by-default. Maps to FSBP EC2.7 (Medium).
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_ebs_encryption_by_default
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ebs_encryption_by_default"
	not resource.attributes.enabled
	msg := sprintf("Resource %v.%v: EBS encryption by default is not enabled", [resource.type, resource.name])
}
