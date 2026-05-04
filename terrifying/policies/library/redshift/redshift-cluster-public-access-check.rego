# title: redshift-cluster-public-access-check
# description: Detects Amazon Redshift clusters with public accessibility enabled. Equivalent to AWS Config redshift-cluster-public-access-check.
# severity: Critical
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    resource.attributes.publicly_accessible == true
    msg := sprintf("Resource %v.%v: Redshift cluster is publicly accessible", [resource.type, resource.name])
}
