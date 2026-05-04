# title: sns-topic-public-access-prohibited
# description: Detects SNS topics whose access policies grant public access via wildcard principal (*). Equivalent to AWS Config sns-topic-no-public-access.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_sns_topic, aws_sns_topic_policy
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sns_topic_policy"
    policy := json.unmarshal(resource.attributes.policy)
    stmt := policy.Statement[_]
    stmt.Effect == "Allow"
    _principal_is_public(stmt.Principal)
    not stmt.Condition
    msg := sprintf("Resource %v.%v: SNS topic policy grants public access via wildcard principal with no conditions", [resource.type, resource.name])
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
