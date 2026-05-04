# title: rds-cluster-multi-az-enabled
# description: Detects RDS DB clusters not configured for multiple Availability Zones. Equivalent to AWS Config rds-cluster-multi-az-enabled.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    not resource.attributes.availability_zones
    msg := sprintf("Resource %v.%v: RDS cluster is not configured for multi-AZ deployment", [resource.type, resource.name])
}
