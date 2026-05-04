# title: codebuild-project-source-repo-url-check
# description: Detects CodeBuild projects whose source repository URL contains embedded credentials (@ in URL). Equivalent to AWS Config codebuild-project-source-repo-url-check. Maps to FSBP CodeBuild.1 (Critical).
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_codebuild_project
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_codebuild_project"
	source := resource.attributes.source[_]
	contains(source.location, "@")
	msg := sprintf("Resource %v.%v: CodeBuild project source URL appears to contain embedded credentials", [resource.type, resource.name])
}
