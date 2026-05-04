# title: kinesis-stream-encrypted
# description: Detects Kinesis Data Streams not encrypted at rest with KMS. Equivalent to AWS Config kinesis-stream-encrypted.
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_kinesis_stream
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_kinesis_stream"
	not resource.attributes.encryption_type
	msg := sprintf("Resource %v.%v: Kinesis stream is not encrypted with KMS", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_kinesis_stream"
	resource.attributes.encryption_type != "KMS"
	msg := sprintf("Resource %v.%v: Kinesis stream is not encrypted with KMS (encryption_type: %v)", [resource.type, resource.name, resource.attributes.encryption_type])
}
