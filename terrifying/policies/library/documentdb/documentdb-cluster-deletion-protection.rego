# title: documentdb-cluster-deletion-protection
# description: Detects DocumentDB clusters without deletion protection enabled. Equivalent to AWS Config documentdb-cluster-deletion-protection-enabled. Maps to FSBP DocumentDB.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_docdb_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_docdb_cluster"
	resource.attributes.deletion_protection == false
	msg := sprintf("Resource %v.%v: DocumentDB cluster does not have deletion protection enabled", [resource.type, resource.name])
}
