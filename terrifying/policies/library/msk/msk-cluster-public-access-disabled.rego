# title: msk-cluster-public-access-disabled
# description: Detects MSK clusters with public broker access enabled. Equivalent to AWS Config FSBP MSK.4.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_msk_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_msk_cluster"
    resource.attributes.broker_node_group_info[_].connectivity_info[_].public_access[_].type != "DISABLED"
    msg := sprintf("Resource %v.%v: MSK cluster has public broker access enabled", [resource.type, resource.name])
}
