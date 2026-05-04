# title: msk-enhanced-monitoring-check
# description: Detects MSK clusters using DEFAULT monitoring level instead of PER_BROKER or higher. Equivalent to AWS Config FSBP MSK.2.
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_msk_cluster
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_msk_cluster"
    resource.attributes.enhanced_monitoring == "DEFAULT"
    msg := sprintf("Resource %v.%v: MSK cluster uses DEFAULT monitoring level; PER_BROKER or higher is required", [resource.type, resource.name])
}
