# title: s3-bucket-blacklisted-actions-prohibited
# description: Detects S3 buckets with policies granting high-risk actions to all principals (*). Equivalent to AWS Config s3-bucket-blacklisted-actions-prohibited.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

_blacklisted_actions := {"s3:DeleteBucketPolicy", "s3:PutBucketAcl"}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    policy := json.unmarshal(resource.attributes.policy)
    stmt := policy.Statement[_]
    stmt.Effect == "Allow"
    _principal_is_public(stmt.Principal)
    action := stmt.Action[_]
    upper(action) in {upper(a) | a := _blacklisted_actions[_]}
    msg := sprintf("Resource %v.%v: S3 bucket policy allows blacklisted action '%v' to public principal", [resource.type, resource.name, action])
}

_principal_is_public(principal) if {
    principal == "*"
}

_principal_is_public(principal) if {
    principal.AWS == "*"
}

_principal_is_public(principal) if {
    principal.AWS[_] == "*"
}
