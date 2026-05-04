# title: sns-encrypted-kms
# description: Detects SNS topics not encrypted at rest using AWS KMS.
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_sns_topic
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sns_topic"
    not resource.attributes.kms_master_key_id
    msg := sprintf("Resource %v.%v: SNS topic is not encrypted with KMS", [resource.type, resource.name])
}
