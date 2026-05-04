# title: opensearch-in-vpc-only
# description: Detects OpenSearch domains not deployed inside a VPC. Equivalent to AWS Config opensearch-in-vpc-only. Maps to FSBP Opensearch.2 (Critical).
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_opensearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_opensearch_domain"
	not resource.attributes.vpc_options
	msg := sprintf("Resource %v.%v: OpenSearch domain is not deployed inside a VPC", [resource.type, resource.name])
}
