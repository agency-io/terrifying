# title: s3-event-notifications-enabled
# description: Detects S3 buckets without any event notification configuration. Equivalent to AWS Config s3-event-notifications-enabled.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    not _has_notifications(resource)
    msg := sprintf("Resource %v.%v: S3 bucket has no event notifications configured", [resource.type, resource.name])
}

_has_notifications(resource) if {
    count(resource.attributes.topic[_]) > 0
}

_has_notifications(resource) if {
    count(resource.attributes.queue[_]) > 0
}

_has_notifications(resource) if {
    count(resource.attributes.lambda_function[_]) > 0
}
