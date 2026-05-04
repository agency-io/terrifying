# title: opensearch-encrypted-at-rest
# description: Detects OpenSearch domains with encryption at rest disabled. Equivalent to AWS Config opensearch-encrypted-at-rest. Maps to FSBP Opensearch.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not encrypt_at_rest_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: OpenSearch domain does not have encryption at rest enabled", [resource.type, resource.name])
}

encrypt_at_rest_enabled(attrs) if {
	attrs.encrypt_at_rest[_].enabled == true
}
