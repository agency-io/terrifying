# title: autoscaling-launchconfig-requires-imdsv2
# description: Detects Auto Scaling launch configurations that do not require IMDSv2, allowing IMDSv1 usage and SSRF-based credential theft. Equivalent to AWS Config autoscaling-launchconfig-requires-imdsv2. Maps to FSBP AutoScaling.3 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_launch_configuration
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_launch_configuration"
	not imdsv2_required(resource)
	msg := sprintf("Resource %v.%v: Launch configuration does not require IMDSv2", [resource.type, resource.name])
}

imdsv2_required(resource) if {
	resource.attributes.metadata_options[_].http_tokens == "required"
}
