# title: rds-automatic-minor-version-upgrade-enabled
# description: Detects RDS DB instances with automatic minor version upgrade disabled.
# severity: High
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.auto_minor_version_upgrade
    msg := sprintf("Resource %v.%v: RDS instance does not have automatic minor version upgrade enabled", [resource.type, resource.name])
}
