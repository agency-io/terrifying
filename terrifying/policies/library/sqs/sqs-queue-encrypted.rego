# title: sqs-queue-encrypted
# description: Detects SQS queues not encrypted at rest; a queue is compliant if it uses a customer KMS key or SQS-managed SSE.
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_sqs_queue
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sqs_queue"
    not resource.attributes.kms_master_key_id
    not resource.attributes.sqs_managed_sse_enabled
    msg := sprintf("Resource %v.%v: SQS queue is not encrypted at rest (no KMS key or SQS-managed SSE)", [resource.type, resource.name])
}
