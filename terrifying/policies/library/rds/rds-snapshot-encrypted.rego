# title: rds-snapshot-encrypted
# description: Detects RDS DB snapshots where encryption is disabled.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark
# terraform_resources: aws_db_snapshot
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_snapshot"
    not resource.attributes.encrypted
    msg := sprintf("Resource %v.%v: RDS snapshot is not encrypted", [resource.type, resource.name])
}
