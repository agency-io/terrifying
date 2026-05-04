# title: rds-instance-public-access-check
# description: Detects RDS DB instances with PubliclyAccessible=true, exposing the database to the internet.
# severity: High
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    resource.attributes.publicly_accessible == true
    msg := sprintf("Resource %v.%v: RDS instance is publicly accessible", [resource.type, resource.name])
}
