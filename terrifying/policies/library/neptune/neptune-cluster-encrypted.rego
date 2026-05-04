# title: neptune-cluster-encrypted
# description: Detects Neptune DB clusters where storage is not encrypted at rest. Equivalent to AWS Config neptune-cluster-encrypted.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_neptune_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_neptune_cluster"
    not resource.attributes.storage_encrypted
    msg := sprintf("Resource %v.%v: Neptune cluster storage is not encrypted at rest", [resource.type, resource.name])
}
