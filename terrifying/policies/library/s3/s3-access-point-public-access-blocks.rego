# title: s3-access-point-public-access-blocks
# description: Detects S3 access points without all four block public access settings enabled. Equivalent to AWS Config s3-access-point-public-access-blocks.
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_s3_access_point
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_access_point"
    not _all_public_access_blocks_enabled(resource)
    msg := sprintf("Resource %v.%v: S3 access point does not have all block public access settings enabled", [resource.type, resource.name])
}

_all_public_access_blocks_enabled(resource) if {
    cfg := resource.attributes.public_access_block_configuration[_]
    cfg.block_public_acls == true
    cfg.block_public_policy == true
    cfg.ignore_public_acls == true
    cfg.restrict_public_buckets == true
}
