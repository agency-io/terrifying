# title: rds-instance-deletion-protection-enabled
# description: Detects RDS DB instances with deletion protection disabled, allowing accidental or unauthorized deletion.
# severity: High
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.deletion_protection
    msg := sprintf("Resource %v.%v: RDS instance does not have deletion protection enabled", [resource.type, resource.name])
}
