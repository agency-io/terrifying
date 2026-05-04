# title: elasticsearch-logs-to-cloudwatch
# description: Detects Elasticsearch domains with no CloudWatch log publishing configured. Equivalent to AWS Config elasticsearch-logs-to-cloudwatch. Maps to FSBP ES.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_elasticsearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticsearch_domain"
	not resource.attributes.log_publishing_options
	msg := sprintf("Resource %v.%v: Elasticsearch domain has no CloudWatch log publishing configured", [resource.type, resource.name])
}
