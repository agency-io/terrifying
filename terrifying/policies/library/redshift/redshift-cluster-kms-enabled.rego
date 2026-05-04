# title: redshift-cluster-kms-enabled
# description: Detects Amazon Redshift clusters not encrypted at rest. Equivalent to AWS Config redshift-cluster-kms-enabled.
# severity: Medium
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    not resource.attributes.encrypted
    msg := sprintf("Resource %v.%v: Redshift cluster is not encrypted at rest", [resource.type, resource.name])
}
