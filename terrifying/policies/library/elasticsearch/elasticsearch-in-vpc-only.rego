# title: elasticsearch-in-vpc-only
# description: Detects Elasticsearch domains not deployed inside a VPC. Equivalent to AWS Config elasticsearch-in-vpc-only. Maps to FSBP ES.2 (Critical).
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_elasticsearch_domain
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elasticsearch_domain"
	not resource.attributes.vpc_options
	msg := sprintf("Resource %v.%v: Elasticsearch domain is not deployed inside a VPC", [resource.type, resource.name])
}
