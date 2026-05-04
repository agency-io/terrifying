# title: rds-multi-az-support
# description: Detects RDS DB instances with Multi-AZ disabled, reducing high availability.
# severity: Medium
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.multi_az
    msg := sprintf("Resource %v.%v: RDS instance does not have Multi-AZ enabled", [resource.type, resource.name])
}
