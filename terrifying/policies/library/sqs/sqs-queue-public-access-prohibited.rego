# title: sqs-queue-public-access-prohibited
# description: Detects SQS queues whose access policies grant public access via wildcard principal (*). Equivalent to AWS Config sqs-queue-no-public-access.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_sqs_queue, aws_sqs_queue_policy
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sqs_queue_policy"
    policy := json.unmarshal(resource.attributes.policy)
    stmt := policy.Statement[_]
    stmt.Effect == "Allow"
    _principal_is_public(stmt.Principal)
    not stmt.Condition
    msg := sprintf("Resource %v.%v: SQS queue policy grants public access via wildcard principal with no conditions", [resource.type, resource.name])
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
