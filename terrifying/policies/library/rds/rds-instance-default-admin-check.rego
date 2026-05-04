# title: rds-instance-default-admin-check
# description: Detects RDS DB instances using a default administrator username. Equivalent to AWS Config rds-instance-default-admin-check.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

_default_usernames := {"admin", "root", "master", "masteruser", "postgres"}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    resource.attributes.username in _default_usernames
    msg := sprintf("Resource %v.%v: RDS instance uses default admin username '%v'", [resource.type, resource.name, resource.attributes.username])
}
