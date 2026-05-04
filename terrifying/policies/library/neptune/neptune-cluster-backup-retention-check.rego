# title: neptune-cluster-backup-retention-check
# description: Detects Neptune DB clusters with backup retention period less than 7 days. Equivalent to AWS Config neptune-cluster-backup-retention-check.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_neptune_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_neptune_cluster"
    resource.attributes.backup_retention_period < 7
    msg := sprintf("Resource %v.%v: Neptune cluster backup retention period is less than 7 days", [resource.type, resource.name])
}
