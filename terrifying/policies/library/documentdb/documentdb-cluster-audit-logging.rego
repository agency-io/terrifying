# title: documentdb-cluster-audit-logging
# description: Detects DocumentDB clusters not publishing audit logs to CloudWatch Logs. Equivalent to AWS Config documentdb-cluster-audit-logging-enabled. Maps to FSBP DocumentDB.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_docdb_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_docdb_cluster"
	not "audit" in resource.attributes.enabled_cloudwatch_logs_exports
	msg := sprintf("Resource %v.%v: DocumentDB cluster is not publishing audit logs to CloudWatch Logs", [resource.type, resource.name])
}
