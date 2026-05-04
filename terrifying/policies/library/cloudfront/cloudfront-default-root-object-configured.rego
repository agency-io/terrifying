# title: cloudfront-default-root-object-configured
# description: Detects CloudFront distributions without a default root object configured. Equivalent to AWS Config cloudfront-default-root-object-configured. Maps to FSBP CloudFront.1 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	not resource.attributes.default_root_object
	msg := sprintf("Resource %v.%v: CloudFront distribution does not have a default root object configured", [resource.type, resource.name])
}
