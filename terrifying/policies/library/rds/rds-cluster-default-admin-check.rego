# title: rds-cluster-default-admin-check
# description: Detects RDS DB clusters using a default administrator username. Equivalent to AWS Config rds-cluster-default-admin-check.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

_default_usernames := {"admin", "root", "master", "masteruser", "postgres"}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    resource.attributes.master_username in _default_usernames
    msg := sprintf("Resource %v.%v: RDS cluster uses default admin username '%v'", [resource.type, resource.name, resource.attributes.master_username])
}
