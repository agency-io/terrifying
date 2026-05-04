# title: secretsmanager-using-cmk
# description: Detects Secrets Manager secrets not encrypted with a customer-managed KMS key. Equivalent to AWS Config secretsmanager-using-cmk.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, pci-dss
# terraform_resources: aws_secretsmanager_secret
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_secretsmanager_secret"
    not resource.attributes.kms_key_id
    msg := sprintf("Resource %v.%v: Secrets Manager secret is not encrypted with a customer-managed KMS key", [resource.type, resource.name])
}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_secretsmanager_secret"
    resource.attributes.kms_key_id
    contains(resource.attributes.kms_key_id, "alias/aws/secretsmanager")
    msg := sprintf("Resource %v.%v: Secrets Manager secret is encrypted with the default aws/secretsmanager key, not a CMK", [resource.type, resource.name])
}
