# title: redshift-cluster-audit-logging-enabled
# description: Detects Amazon Redshift clusters without audit logging enabled. Equivalent to AWS Config redshift-cluster-audit-logging-enabled.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    not _has_logging(resource)
    msg := sprintf("Resource %v.%v: Redshift cluster does not have audit logging enabled", [resource.type, resource.name])
}

_has_logging(resource) if {
    resource.attributes.logging[_].enable == true
}
