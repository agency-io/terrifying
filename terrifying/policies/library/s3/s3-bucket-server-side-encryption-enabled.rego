# title: s3-bucket-server-side-encryption-enabled
# description: Detects S3 buckets without default server-side encryption configured. Equivalent to AWS Config s3-bucket-server-side-encryption-enabled.
# severity: Medium
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_server_side_encryption_configuration
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_sse_config(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket server-side encryption is not configured", [bucket.type, bucket.name])
}

_has_sse_config(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_server_side_encryption_configuration"
    r.attributes.bucket == bucket_name
}
