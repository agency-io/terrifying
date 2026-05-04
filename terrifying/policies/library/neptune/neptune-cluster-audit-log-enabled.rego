# title: neptune-cluster-audit-log-enabled
# description: Detects Neptune DB clusters not exporting audit logs to CloudWatch Logs. Equivalent to AWS Config neptune-cluster-audit-log-enabled.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_neptune_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_neptune_cluster"
    not _has_audit_log(resource)
    msg := sprintf("Resource %v.%v: Neptune cluster does not export audit logs to CloudWatch", [resource.type, resource.name])
}

_has_audit_log(resource) if {
    "audit" in resource.attributes.enable_cloudwatch_logs_exports
}
