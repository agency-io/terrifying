# title: opensearch-https-required
# description: Detects OpenSearch domains with HTTPS enforcement disabled on the domain endpoint. Equivalent to AWS Config opensearch-https-required. Maps to FSBP Opensearch.8 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not enforce_https_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: OpenSearch domain does not enforce HTTPS on its endpoint", [resource.type, resource.name])
}

enforce_https_enabled(attrs) if {
	attrs.domain_endpoint_options[_].enforce_https == true
}
