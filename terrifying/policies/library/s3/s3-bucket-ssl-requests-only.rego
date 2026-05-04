# title: s3-bucket-ssl-requests-only
# description: Detects S3 buckets without a bucket policy that explicitly denies non-SSL requests. Equivalent to AWS Config s3-bucket-ssl-requests-only.
# severity: High
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    not _has_ssl_deny(resource)
    msg := sprintf("Resource %v.%v: S3 bucket does not have a policy denying non-SSL requests", [resource.type, resource.name])
}

_has_ssl_deny(resource) if {
    policy := json.unmarshal(resource.attributes.policy)
    stmt := policy.Statement[_]
    stmt.Effect == "Deny"
    cond := stmt.Condition
    _ssl_false_condition(cond)
}

_ssl_false_condition(cond) if {
    cond.Bool["aws:SecureTransport"] == "false"
}

_ssl_false_condition(cond) if {
    cond.Bool["aws:securetransport"] == "false"
}
