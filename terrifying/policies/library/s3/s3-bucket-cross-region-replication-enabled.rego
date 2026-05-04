# title: s3-bucket-cross-region-replication-enabled
# description: Detects S3 buckets without cross-region replication configured. Equivalent to AWS Config s3-bucket-replication-enabled.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_replication_configuration
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_replication(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket does not have cross-region replication configured", [bucket.type, bucket.name])
}

_has_replication(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_replication_configuration"
    r.attributes.bucket == bucket_name
}
