# title: s3-bucket-versioning-enabled
# description: Detects S3 buckets without versioning enabled or with versioning suspended.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_s3_bucket, aws_s3_bucket_versioning
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_versioning(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket versioning is not enabled", [bucket.type, bucket.name])
}

_has_versioning(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_versioning"
    r.attributes.bucket == bucket_name
    r.attributes.versioning_configuration[_].status == "Enabled"
}
