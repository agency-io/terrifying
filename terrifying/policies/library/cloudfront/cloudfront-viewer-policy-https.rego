# title: cloudfront-viewer-policy-https
# description: Detects CloudFront distributions whose default cache behavior allows unencrypted HTTP from viewers. Equivalent to AWS Config cloudfront-viewer-policy-https. Maps to FSBP CloudFront.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	cache_behavior := resource.attributes.default_cache_behavior[_]
	cache_behavior.viewer_protocol_policy == "allow-all"
	msg := sprintf("Resource %v.%v: CloudFront distribution default cache behavior allows HTTP (viewer_protocol_policy: allow-all)", [resource.type, resource.name])
}
