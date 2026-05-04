# title: rds-aurora-mysql-audit-logging-enabled
# description: Detects Aurora MySQL clusters that do not export audit logs to CloudWatch Logs. Equivalent to AWS Config rds-aurora-mysql-audit-logging-enabled.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_rds_cluster
package terrifying

import rego.v1

_aurora_mysql_engines := {"aurora", "aurora-mysql"}

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_rds_cluster"
    resource.attributes.engine in _aurora_mysql_engines
    not "audit" in resource.attributes.enabled_cloudwatch_logs_exports
    msg := sprintf("Resource %v.%v: Aurora MySQL cluster does not export audit logs to CloudWatch", [resource.type, resource.name])
}
