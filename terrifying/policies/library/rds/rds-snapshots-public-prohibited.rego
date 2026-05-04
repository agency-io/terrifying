# title: rds-snapshots-public-prohibited
# description: Detects RDS DB snapshots shared publicly (restore attribute includes 'all').
# severity: Critical
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_db_snapshot, aws_db_cluster_snapshot
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_snapshot"
    resource.attributes.shared_accounts[_] == "all"
    msg := sprintf("Resource %v.%v: RDS snapshot is publicly accessible (restore permission granted to 'all')", [resource.type, resource.name])
}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_cluster_snapshot"
    resource.attributes.shared_accounts[_] == "all"
    msg := sprintf("Resource %v.%v: RDS cluster snapshot is publicly accessible (restore permission granted to 'all')", [resource.type, resource.name])
}
