# title: s3-bucket-acl-prohibited
# description: Detects S3 buckets that do not have ACL ownership enforced (BucketOwnerEnforced). Equivalent to AWS Config s3-bucket-acl-prohibited.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    not _has_owner_enforced(resource)
    msg := sprintf("Resource %v.%v: S3 bucket does not enforce bucket owner for object ownership (ACLs should be disabled)", [resource.type, resource.name])
}

_has_owner_enforced(resource) if {
    resource.attributes.object_ownership == "BucketOwnerEnforced"
}
