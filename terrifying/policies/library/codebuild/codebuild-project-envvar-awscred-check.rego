# title: codebuild-project-envvar-awscred-check
# description: Detects CodeBuild projects storing AWS credentials as plaintext environment variables. Equivalent to AWS Config codebuild-project-envvar-awscred-check. Maps to FSBP CodeBuild.2 (Critical).
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_codebuild_project
package terrifying

import rego.v1

sensitive_var_names := {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_codebuild_project"
	env := resource.attributes.environment[_]
	env_var := env.environment_variable[_]
	env_var.type == "PLAINTEXT"
	env_var.name in sensitive_var_names
	msg := sprintf("Resource %v.%v: CodeBuild project stores sensitive credential '%v' as a PLAINTEXT environment variable", [resource.type, resource.name, env_var.name])
}
