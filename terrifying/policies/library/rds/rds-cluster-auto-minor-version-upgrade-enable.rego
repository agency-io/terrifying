# title: rds-cluster-auto-minor-version-upgrade-enable
# description: Detects Aurora DB clusters where auto minor version upgrade is disabled. Equivalent to AWS Config rds-cluster-auto-minor-version-upgrade-enable.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    not resource.attributes.auto_minor_version_upgrade
    msg := sprintf("Resource %v.%v: RDS cluster does not have auto minor version upgrade enabled", [resource.type, resource.name])
}
