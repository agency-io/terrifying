# title: elasticsearch-encrypted-at-rest
# description: Detects Elasticsearch domains with encryption at rest disabled. Equivalent to AWS Config elasticsearch-encrypted-at-rest. Maps to FSBP ES.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_elasticsearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticsearch_domain"
	not encrypt_at_rest_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: Elasticsearch domain does not have encryption at rest enabled", [resource.type, resource.name])
}

encrypt_at_rest_enabled(attrs) if {
	attrs.encrypt_at_rest[_].enabled == true
}
