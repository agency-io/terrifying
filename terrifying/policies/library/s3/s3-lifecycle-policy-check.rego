# title: s3-lifecycle-policy-check
# description: Detects S3 buckets without a lifecycle configuration. Equivalent to AWS Config s3-lifecycle-policy-check.
# severity: Low
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_s3_bucket
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket"
    count(resource.attributes.lifecycle_rule) == 0
    msg := sprintf("Resource %v.%v: S3 bucket does not have a lifecycle policy configured", [resource.type, resource.name])
}
