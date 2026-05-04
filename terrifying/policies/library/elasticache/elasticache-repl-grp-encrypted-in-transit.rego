# title: elasticache-repl-grp-encrypted-in-transit
# description: Detects ElastiCache replication groups where in-transit encryption is not enabled. Equivalent to AWS Config elasticache-repl-grp-encrypted-in-transit. Maps to FSBP ElastiCache.3 (High).
# severity: High
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_elasticache_replication_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	not resource.attributes.transit_encryption_enabled
	msg := sprintf("Resource %v.%v: ElastiCache replication group does not have in-transit encryption enabled", [resource.type, resource.name])
}
