# title: wafv2-logging-enabled
# description: Detects WAFv2 Web ACLs with no logging configured. Equivalent to AWS Config FSBP WAF.11.
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_wafv2_web_acl, aws_wafv2_web_acl_logging_configuration
package terrifying

import rego.v1

deny contains msg if {
    acl := input.resources[_]
    acl.type == "aws_wafv2_web_acl"
    not _has_logging(input.resources, acl.name)
    msg := sprintf("Resource %v.%v: WAFv2 Web ACL does not have logging configured", [acl.type, acl.name])
}

_has_logging(resources, acl_name) if {
    r := resources[_]
    r.type == "aws_wafv2_web_acl_logging_configuration"
    r.attributes.resource_arn == acl_name
}
