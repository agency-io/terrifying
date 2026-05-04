# title: rds-cluster-encrypted-at-rest
# description: Detects RDS DB clusters where storage is not encrypted at rest. Equivalent to AWS Config rds-cluster-encrypted-at-rest.
# severity: High
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    not resource.attributes.storage_encrypted
    msg := sprintf("Resource %v.%v: RDS cluster storage is not encrypted at rest", [resource.type, resource.name])
}
