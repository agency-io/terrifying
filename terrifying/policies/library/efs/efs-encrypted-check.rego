# title: efs-encrypted-check
# description: Detects Amazon EFS file systems that are not encrypted at rest. Equivalent to AWS Security Hub FSBP EFS.1 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_efs_file_system
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_efs_file_system"
	not resource.attributes.encrypted
	msg := sprintf("Resource %v.%v: EFS file system is not encrypted at rest", [resource.type, resource.name])
}
