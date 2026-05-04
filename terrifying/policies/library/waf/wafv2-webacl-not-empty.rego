# title: wafv2-webacl-not-empty
# description: Detects WAFv2 Web ACLs with no rules configured, providing no protection. Equivalent to AWS Config FSBP WAF.10.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_wafv2_web_acl
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_wafv2_web_acl"
    count(resource.attributes.rule) == 0
    msg := sprintf("Resource %v.%v: WAFv2 Web ACL has no rules configured", [resource.type, resource.name])
}
