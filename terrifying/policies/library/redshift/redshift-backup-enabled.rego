# title: redshift-backup-enabled
# description: Detects Amazon Redshift clusters with automated snapshots disabled (retention period = 0). Equivalent to AWS Config redshift-backup-enabled.
# severity: High
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    resource.attributes.automated_snapshot_retention_period == 0
    msg := sprintf("Resource %v.%v: Redshift cluster has automated snapshots disabled", [resource.type, resource.name])
}
