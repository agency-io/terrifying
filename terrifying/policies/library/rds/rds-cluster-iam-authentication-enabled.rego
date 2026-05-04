# title: rds-cluster-iam-authentication-enabled
# description: Detects RDS DB clusters where IAM database authentication is disabled. Equivalent to AWS Config rds-cluster-iam-authentication-enabled.
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    not resource.attributes.iam_database_authentication_enabled
    msg := sprintf("Resource %v.%v: RDS cluster does not have IAM database authentication enabled", [resource.type, resource.name])
}
