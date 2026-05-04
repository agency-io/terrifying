# title: documentdb-cluster-backup-retention
# description: Detects DocumentDB clusters where backup retention period is less than 7 days. Equivalent to AWS Config documentdb-cluster-backup-retention-check. Maps to FSBP DocumentDB.2 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_docdb_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_docdb_cluster"
	resource.attributes.backup_retention_period < 7
	msg := sprintf("Resource %v.%v: DocumentDB cluster has backup retention less than 7 days", [resource.type, resource.name])
}
