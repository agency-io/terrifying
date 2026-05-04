# title: s3-default-encryption-kms
# description: Detects S3 buckets not encrypted with AWS KMS; flags buckets with no encryption or AES256 encryption.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_server_side_encryption_configuration
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_kms_encryption(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket is not encrypted with AWS KMS", [bucket.type, bucket.name])
}

_has_kms_encryption(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_server_side_encryption_configuration"
    r.attributes.bucket == bucket_name
    rule := r.attributes.rule[_]
    rule.apply_server_side_encryption_by_default[_].sse_algorithm == "aws:kms"
}
