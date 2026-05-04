# title: msk-cluster-unauthenticated-access-disabled
# description: Detects MSK clusters with unauthenticated client access enabled. Equivalent to AWS Config FSBP MSK.6.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_msk_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_msk_cluster"
    resource.attributes.client_authentication[_].unauthenticated[_].enabled == true
    msg := sprintf("Resource %v.%v: MSK cluster allows unauthenticated client access", [resource.type, resource.name])
}
