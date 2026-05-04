# title: elasticache-subnet-group-check
# description: Detects ElastiCache clusters using the default subnet group, which may place clusters in publicly accessible subnets. Equivalent to AWS Config elasticache-subnet-group-check. Maps to FSBP ElastiCache.7 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_elasticache_subnet_group
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticache_replication_group"
	resource.attributes.subnet_group_name == "default"
	msg := sprintf("Resource %v.%v: ElastiCache cluster uses the default subnet group", [resource.type, resource.name])
}
