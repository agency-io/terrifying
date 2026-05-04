# title: neptune-cluster-deletion-protection
# description: Detects Neptune DB clusters where deletion protection is disabled. Equivalent to AWS Config neptune-cluster-deletion-protection.
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_neptune_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_neptune_cluster"
    not resource.attributes.deletion_protection
    msg := sprintf("Resource %v.%v: Neptune cluster does not have deletion protection enabled", [resource.type, resource.name])
}
