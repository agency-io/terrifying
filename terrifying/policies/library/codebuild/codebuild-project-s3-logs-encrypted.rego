# title: codebuild-project-s3-logs-encrypted
# description: Detects CodeBuild projects where S3 logging is enabled but encryption is disabled. Equivalent to AWS Config codebuild-project-s3-logs-encrypted. Maps to FSBP CodeBuild.3 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_codebuild_project
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_codebuild_project"
	logs := resource.attributes.logs_config[_]
	s3_logs := logs.s3_logs[_]
	s3_logs.status == "ENABLED"
	s3_logs.encryption_disabled == true
	msg := sprintf("Resource %v.%v: CodeBuild project has S3 logging enabled but encryption is disabled", [resource.type, resource.name])
}
