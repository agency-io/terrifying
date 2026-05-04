# title: neptune-cluster-iam-auth-enabled
# description: Detects Neptune DB clusters where IAM database authentication is disabled. Equivalent to AWS Config neptune-cluster-iam-auth-enabled.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_neptune_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_neptune_cluster"
    not resource.attributes.iam_database_authentication_enabled
    msg := sprintf("Resource %v.%v: Neptune cluster does not have IAM database authentication enabled", [resource.type, resource.name])
}
