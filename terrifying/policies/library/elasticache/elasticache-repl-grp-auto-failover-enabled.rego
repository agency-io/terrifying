# title: elasticache-repl-grp-auto-failover-enabled
# description: Detects ElastiCache replication groups where automatic failover is not enabled. Equivalent to AWS Config elasticache-repl-grp-auto-failover-enabled. Maps to FSBP ElastiCache.3 (High).
# severity: High
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_elasticache_replication_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	not resource.attributes.automatic_failover_enabled
	msg := sprintf("Resource %v.%v: ElastiCache replication group does not have automatic failover enabled", [resource.type, resource.name])
}
