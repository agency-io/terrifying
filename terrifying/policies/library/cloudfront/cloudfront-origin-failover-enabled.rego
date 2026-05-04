# title: cloudfront-origin-failover-enabled
# description: Detects CloudFront distributions with no origin groups configured for automatic failover. Equivalent to AWS Config cloudfront-origin-failover-enabled. Maps to FSBP CloudFront.4 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	not resource.attributes.origin_group
	msg := sprintf("Resource %v.%v: CloudFront distribution has no origin groups configured for failover", [resource.type, resource.name])
}
