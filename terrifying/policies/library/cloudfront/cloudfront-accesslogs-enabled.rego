# title: cloudfront-accesslogs-enabled
# description: Detects CloudFront distributions without access logging enabled. Equivalent to AWS Config cloudfront-accesslogs-enabled. Maps to FSBP CloudFront.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	not resource.attributes.logging_config
	msg := sprintf("Resource %v.%v: CloudFront distribution does not have access logging enabled", [resource.type, resource.name])
}
