# title: cloudfront-no-deprecated-ssl-protocols
# description: Detects CloudFront distributions with custom origins using deprecated SSL/TLS protocols (SSLv3, TLSv1, TLSv1.1). Equivalent to FSBP CloudFront.10. Maps to Medium severity.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deprecated_protocols := {"SSLv3", "TLSv1", "TLSv1.1"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	origin := resource.attributes.origin[_]
	custom_config := origin.custom_origin_config[_]
	protocol := custom_config.origin_ssl_protocols[_]
	protocol in deprecated_protocols
	msg := sprintf("Resource %v.%v: CloudFront distribution has an origin using deprecated SSL/TLS protocol: %v", [resource.type, resource.name, protocol])
}
