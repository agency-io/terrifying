# title: ec2-launch-template-imdsv2-check
# description: Detects EC2 launch templates not requiring IMDSv2, allowing IMDSv1 and enabling SSRF-based credential theft. Equivalent to AWS Config ec2-launch-template-imdsv2-check. Maps to FSBP EC2.170 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_launch_template
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_launch_template"
	not imdsv2_required(resource)
	msg := sprintf("Resource %v.%v: EC2 launch template does not require IMDSv2", [resource.type, resource.name])
}

imdsv2_required(resource) if {
	resource.attributes.metadata_options[_].http_tokens == "required"
}
