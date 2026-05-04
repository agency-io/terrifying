# title: cloudfront-custom-ssl-certificate
# description: Detects CloudFront distributions using the default CloudFront SSL certificate instead of a custom one. Equivalent to AWS Config cloudfront-custom-ssl-certificate. Maps to FSBP CloudFront.7 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	viewer_cert := resource.attributes.viewer_certificate[_]
	viewer_cert.cloudfront_default_certificate == true
	msg := sprintf("Resource %v.%v: CloudFront distribution is using the default CloudFront SSL certificate instead of a custom certificate", [resource.type, resource.name])
}
