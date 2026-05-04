# title: ssm-document-not-public
# description: Detects SSM documents shared publicly with all AWS accounts. Equivalent to AWS Config ssm-document-not-public.
# severity: Critical
# tags: security-hub, fsbp, cis-benchmark, nist-800-53
# terraform_resources: aws_ssm_document
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_ssm_document"
    resource.attributes.permissions.account_ids[_] == "all"
    msg := sprintf("Resource %v.%v: SSM document is shared publicly with all AWS accounts", [resource.type, resource.name])
}
