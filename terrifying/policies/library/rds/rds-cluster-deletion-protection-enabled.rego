# title: rds-cluster-deletion-protection-enabled
# description: Detects RDS DB clusters with deletion protection disabled. Equivalent to AWS Config rds-cluster-deletion-protection-enabled.
# severity: High
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    not resource.attributes.deletion_protection
    msg := sprintf("Resource %v.%v: RDS cluster does not have deletion protection enabled", [resource.type, resource.name])
}
