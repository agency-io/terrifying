# title: elasticache-redis-auth-enabled
# description: Detects ElastiCache Redis replication groups where AUTH token is not enabled. Equivalent to AWS Config elasticache-redis-auth-enabled. Maps to FSBP ElastiCache.6 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_elasticache_replication_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	not resource.attributes.auth_token
	msg := sprintf("Resource %v.%v: ElastiCache Redis replication group does not have AUTH token enabled", [resource.type, resource.name])
}
