# title: redshift-enhanced-vpc-routing-enabled
# description: Detects Amazon Redshift clusters with enhanced VPC routing disabled. Equivalent to AWS Config redshift-enhanced-vpc-routing-enabled.
# severity: Medium
# tags: security-hub, fsbp, nist-800-53
# terraform_resources: aws_redshift_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_redshift_cluster"
    not resource.attributes.enhanced_vpc_routing
    msg := sprintf("Resource %v.%v: Redshift cluster does not have enhanced VPC routing enabled", [resource.type, resource.name])
}
