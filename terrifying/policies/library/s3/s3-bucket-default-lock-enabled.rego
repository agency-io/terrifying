# title: s3-bucket-default-lock-enabled
# description: Detects S3 buckets without S3 Object Lock enabled. Equivalent to AWS Config s3-bucket-default-lock-enabled.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    not resource.attributes.object_lock_enabled
    msg := sprintf("Resource %v.%v: S3 bucket does not have Object Lock enabled", [resource.type, resource.name])
}
