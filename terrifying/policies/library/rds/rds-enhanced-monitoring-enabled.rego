# title: rds-enhanced-monitoring-enabled
# description: Detects RDS DB instances where enhanced monitoring is disabled (MonitoringInterval=0). Equivalent to AWS Config rds-enhanced-monitoring-enabled.
# severity: Low
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    resource.attributes.monitoring_interval == 0
    msg := sprintf("Resource %v.%v: RDS instance does not have enhanced monitoring enabled", [resource.type, resource.name])
}
