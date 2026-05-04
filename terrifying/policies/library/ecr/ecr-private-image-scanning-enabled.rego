# title: ecr-private-image-scanning-enabled
# description: Detects ECR private repositories without scan-on-push enabled, missing vulnerability detection on new images. Equivalent to AWS Config ecr-private-image-scanning-enabled. Maps to FSBP ECR.1 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_ecr_repository
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecr_repository"
	not scan_on_push_enabled(resource.attributes)
	msg := sprintf("Resource %v.%v: ECR repository does not have scan-on-push enabled", [resource.type, resource.name])
}

scan_on_push_enabled(attrs) if {
	attrs.image_scanning_configuration[_].scan_on_push == true
}
