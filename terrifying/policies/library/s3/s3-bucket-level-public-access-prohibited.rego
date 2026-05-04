# title: s3-bucket-level-public-access-prohibited
# description: Detects S3 buckets missing bucket-level Block Public Access settings.
# severity: Critical
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_s3_bucket, aws_s3_bucket_public_access_block
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_public_access_block(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket does not have all Block Public Access settings enabled", [bucket.type, bucket.name])
}

_has_public_access_block(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_public_access_block"
    r.attributes.bucket == bucket_name
    r.attributes.block_public_acls == true
    r.attributes.block_public_policy == true
}
