# title: elasticache-redis-cluster-automatic-backup-check
# description: Detects ElastiCache Redis replication groups where automatic backups are disabled (snapshot_retention_limit=0). Equivalent to AWS Config elasticache-redis-cluster-automatic-backup-check. Maps to FSBP ElastiCache.1 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_elasticache_replication_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	resource.attributes.snapshot_retention_limit == 0
	msg := sprintf("Resource %v.%v: ElastiCache Redis replication group has automatic backups disabled (snapshot_retention_limit=0)", [resource.type, resource.name])
}
