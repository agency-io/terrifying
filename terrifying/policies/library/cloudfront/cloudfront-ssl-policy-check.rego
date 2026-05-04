# title: cloudfront-ssl-policy-check
# description: Detects CloudFront distributions using outdated TLS security policies for viewer connections. Equivalent to FSBP CloudFront.15. Maps to Medium severity.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deprecated_policies := {"SSLv3", "TLSv1", "TLSv1_2016", "TLSv1.1_2016"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	viewer_cert := resource.attributes.viewer_certificate[_]
	viewer_cert.minimum_protocol_version in deprecated_policies
	msg := sprintf("Resource %v.%v: CloudFront distribution uses deprecated TLS policy '%v' for viewer connections", [resource.type, resource.name, viewer_cert.minimum_protocol_version])
}
