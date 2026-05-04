# title: api-gw-cache-encrypted
# description: Detects API Gateway REST stages with caching enabled but cache data not encrypted. Equivalent to AWS Config api-gw-cache-encrypted. Maps to FSBP APIGateway.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_api_gateway_stage
package terrifying

import rego.v1

# In Terraform, per-method cache encryption is configured via method_settings blocks.
# This policy flags any stage where cache_cluster_enabled is true and a method_settings
# block explicitly sets cache_data_encrypted to false.
deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_api_gateway_stage"
	resource.attributes.cache_cluster_enabled == true
	settings := resource.attributes.method_settings[_]
	settings.cache_data_encrypted == false
	msg := sprintf("Resource %v.%v: API Gateway stage has caching enabled but cache data is not encrypted", [resource.type, resource.name])
}
