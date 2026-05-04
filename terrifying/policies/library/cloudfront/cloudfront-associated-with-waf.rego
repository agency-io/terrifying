# title: cloudfront-associated-with-waf
# description: Detects CloudFront distributions without a WAF Web ACL associated. Equivalent to AWS Config cloudfront-associated-with-waf. Maps to FSBP CloudFront.6 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	not resource.attributes.web_acl_id
	msg := sprintf("Resource %v.%v: CloudFront distribution is not associated with a WAF Web ACL", [resource.type, resource.name])
}
