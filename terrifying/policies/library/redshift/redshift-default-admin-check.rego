# title: redshift-default-admin-check
# description: Detects Amazon Redshift clusters using a default administrator username. Equivalent to AWS Config redshift-default-admin-check.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

_default_usernames := {"admin", "awsuser", "master"}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    resource.attributes.master_username in _default_usernames
    msg := sprintf("Resource %v.%v: Redshift cluster uses default admin username '%v'", [resource.type, resource.name, resource.attributes.master_username])
}
