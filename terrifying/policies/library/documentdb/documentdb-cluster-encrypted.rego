# title: documentdb-cluster-encrypted
# description: Detects DocumentDB clusters without storage encryption enabled. Equivalent to AWS Config documentdb-cluster-encrypted. Maps to FSBP DocumentDB.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_docdb_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_docdb_cluster"
	resource.attributes.storage_encrypted == false
	msg := sprintf("Resource %v.%v: DocumentDB cluster does not have storage encryption enabled", [resource.type, resource.name])
}
