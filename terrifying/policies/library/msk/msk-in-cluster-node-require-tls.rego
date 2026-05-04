# title: msk-in-cluster-node-require-tls
# description: Detects MSK clusters without TLS-only client-broker encryption. Equivalent to AWS Config FSBP MSK.1.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_msk_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_msk_cluster"
    resource.attributes.encryption_info[_].encryption_in_transit[_].client_broker != "TLS"
    msg := sprintf("Resource %v.%v: MSK cluster client-broker encryption is not set to TLS", [resource.type, resource.name])
}
