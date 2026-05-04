# title: s3-bucket-mfa-delete-enabled
# description: Detects S3 buckets where MFA Delete is not enabled on the versioning configuration. Equivalent to AWS Config s3-bucket-mfa-delete-enabled.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_versioning
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_mfa_delete(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket does not have MFA Delete enabled", [bucket.type, bucket.name])
}

_has_mfa_delete(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_versioning"
    r.attributes.bucket == bucket_name
    r.attributes.versioning_configuration[_].mfa_delete == "Enabled"
}
