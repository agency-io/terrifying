# title: opensearch-access-control-enabled
# description: Detects OpenSearch domains with fine-grained access control (advanced_security_options) disabled. Equivalent to AWS Config opensearch-access-control-enabled. Maps to FSBP Opensearch.7 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not advanced_security_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: OpenSearch domain does not have fine-grained access control enabled", [resource.type, resource.name])
}

advanced_security_enabled(attrs) if {
	attrs.advanced_security_options[_].enabled == true
}
