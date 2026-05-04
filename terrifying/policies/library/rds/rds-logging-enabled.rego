# title: rds-logging-enabled
# description: Detects RDS DB instances with no CloudWatch Logs exports configured.
# severity: Medium
# tags: control-tower, security-hub, fsbp, conformance-pack
# terraform_resources: aws_db_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    count(resource.attributes.enabled_cloudwatch_logs_exports) == 0
    msg := sprintf("Resource %v.%v: RDS instance has no CloudWatch Logs exports configured", [resource.type, resource.name])
}
