# title: cloudfront-s3-origin-access-control-enabled
# description: Detects CloudFront distributions with S3 origins that lack an Origin Access Control ID, allowing public S3 access. Equivalent to FSBP CloudFront.13. Maps to Medium severity.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_cloudfront_distribution
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_cloudfront_distribution"
	origin := resource.attributes.origin[_]
	contains(origin.domain_name, ".s3.")
	not oac_configured(origin)
	msg := sprintf("Resource %v.%v: CloudFront distribution has S3 origin '%v' without Origin Access Control configured", [resource.type, resource.name, origin.domain_name])
}

oac_configured(origin) if {
	origin.origin_access_control_id != ""
	origin.origin_access_control_id != null
}
