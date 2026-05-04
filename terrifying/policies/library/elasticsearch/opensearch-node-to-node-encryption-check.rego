# title: opensearch-node-to-node-encryption-check
# description: Detects OpenSearch domains with node-to-node encryption disabled. Equivalent to AWS Config opensearch-node-to-node-encryption-check. Maps to FSBP Opensearch.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not node_to_node_encryption_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: OpenSearch domain does not have node-to-node encryption enabled", [resource.type, resource.name])
}

node_to_node_encryption_enabled(attrs) if {
	attrs.node_to_node_encryption[_].enabled == true
}
