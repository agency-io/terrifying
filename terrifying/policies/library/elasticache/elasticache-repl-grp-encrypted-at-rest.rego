# title: elasticache-repl-grp-encrypted-at-rest
# description: Detects ElastiCache replication groups where at-rest encryption is not enabled. Equivalent to AWS Config elasticache-repl-grp-encrypted-at-rest. Maps to FSBP ElastiCache.5 (High).
# severity: High
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_elasticache_replication_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	not resource.attributes.at_rest_encryption_enabled
	msg := sprintf("Resource %v.%v: ElastiCache replication group does not have at-rest encryption enabled", [resource.type, resource.name])
}
