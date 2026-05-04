# title: opensearch-logs-to-cloudwatch
# description: Detects OpenSearch domains with no CloudWatch log publishing configured. Equivalent to AWS Config opensearch-logs-to-cloudwatch. Maps to FSBP Opensearch.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not resource.attributes.log_publishing_options
	msg := sprintf("Resource %v.%v: OpenSearch domain has no CloudWatch log publishing configured", [resource.type, resource.name])
}
