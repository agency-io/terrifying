# title: db-instance-backup-enabled
# description: Detects RDS DB instances with automated backups disabled (BackupRetentionPeriod=0). Equivalent to AWS Config db-instance-backup-enabled.
# severity: Medium
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    resource.attributes.backup_retention_period == 0
    msg := sprintf("Resource %v.%v: RDS instance has automated backups disabled (BackupRetentionPeriod=0)", [resource.type, resource.name])
}
