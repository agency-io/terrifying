# title: s3-bucket-logging-enabled
# description: Detects S3 buckets without server access logging enabled.
# severity: Medium
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_logging
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_logging(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket does not have server access logging enabled", [bucket.type, bucket.name])
}

_has_logging(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_logging"
    r.attributes.bucket == bucket_name
}
