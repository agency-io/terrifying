# title: rds-db-security-group-not-allowed
# description: Detects RDS instances using legacy EC2-Classic DB security groups instead of VPC security groups. Equivalent to AWS Config rds-db-security-group-not-allowed.
# severity: Medium
# tags: cis-benchmark, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    count(resource.attributes.db_security_groups) > 0
    msg := sprintf("Resource %v.%v: RDS instance uses legacy DB security groups; VPC security groups should be used instead", [resource.type, resource.name])
}
