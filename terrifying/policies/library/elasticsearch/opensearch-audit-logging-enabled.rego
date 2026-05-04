# title: opensearch-audit-logging-enabled
# description: Detects OpenSearch domains without audit logging enabled in log_publishing_options. Equivalent to AWS Config opensearch-audit-logging-enabled. Maps to FSBP Opensearch.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not audit_logging_enabled(resource)
	msg := sprintf("Resource %v.%v: OpenSearch domain does not have audit logging enabled", [resource.type, resource.name])
}

audit_logging_enabled(resource) if {
	some opt in resource.attributes.log_publishing_options
	opt.log_type == "AUDIT_LOGS"
	opt.enabled == true
}
