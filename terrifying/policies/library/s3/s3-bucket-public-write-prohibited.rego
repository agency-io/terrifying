# title: s3-bucket-public-write-prohibited
# description: Detects S3 buckets with public write access via ACL grants to AllUsers or AuthenticatedUsers. Equivalent to AWS Config s3-bucket-public-write-prohibited.
# severity: Critical
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_s3_bucket, aws_s3_bucket_public_access_block
package terrifying

import rego.v1

deny contains msg if {
    bucket := input.resources[_]
    bucket.type == "aws_s3_bucket"
    not _has_write_block(input.resources, bucket.name)
    msg := sprintf("Resource %v.%v: S3 bucket does not block public write access", [bucket.type, bucket.name])
}

_has_write_block(resources, bucket_name) if {
    r := resources[_]
    r.type == "aws_s3_bucket_public_access_block"
    r.attributes.bucket == bucket_name
    r.attributes.block_public_acls == true
    r.attributes.block_public_policy == true
    r.attributes.restrict_public_buckets == true
}
