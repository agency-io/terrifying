# title: codebuild-project-logging-enabled
# description: Detects CodeBuild projects with neither CloudWatch Logs nor S3 logging enabled. Equivalent to AWS Config codebuild-project-logging-enabled. Maps to FSBP CodeBuild.4 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_codebuild_project
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_codebuild_project"
	not any_logging_enabled(resource)
	msg := sprintf("Resource %v.%v: CodeBuild project has neither CloudWatch Logs nor S3 logging enabled", [resource.type, resource.name])
}

any_logging_enabled(resource) if {
	logs := resource.attributes.logs_config[_]
	logs.cloudwatch_logs[_].status == "ENABLED"
}

any_logging_enabled(resource) if {
	logs := resource.attributes.logs_config[_]
	logs.s3_logs[_].status == "ENABLED"
}
