# title: rds-instance-iam-authentication-enabled
# description: Detects RDS DB instances where IAM database authentication is disabled. Equivalent to AWS Config rds-instance-iam-authentication-enabled.
# severity: Medium
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.iam_database_authentication_enabled
    msg := sprintf("Resource %v.%v: RDS instance does not have IAM database authentication enabled", [resource.type, resource.name])
}
