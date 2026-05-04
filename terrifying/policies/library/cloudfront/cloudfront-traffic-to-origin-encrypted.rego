# title: cloudfront-traffic-to-origin-encrypted
# description: Detects CloudFront distributions with custom origins using http-only protocol, allowing unencrypted traffic between CloudFront and the origin. Equivalent to FSBP CloudFront.9 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	origin := resource.attributes.origin[_]
	custom_config := origin.custom_origin_config[_]
	custom_config.origin_protocol_policy == "http-only"
	msg := sprintf("Resource %v.%v: CloudFront distribution has an origin using http-only protocol (unencrypted traffic to origin)", [resource.type, resource.name])
}
