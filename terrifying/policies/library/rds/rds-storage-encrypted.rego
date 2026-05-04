# title: rds-storage-encrypted
# description: Detects RDS DB instances with storage encryption disabled.
# severity: High
# tags: control-tower, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.storage_encrypted
    msg := sprintf("Resource %v.%v: RDS instance storage encryption is disabled", [resource.type, resource.name])
}
