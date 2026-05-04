# title: ecr-private-repo-kms-encrypted
# description: Detects ECR private repositories not encrypted with a customer managed KMS key. Equivalent to AWS Config ecr-private-repo-kms-encrypted. Maps to FSBP ECR.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_ecr_repository
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ecr_repository"
	not kms_encrypted(resource)
	msg := sprintf("Resource %v.%v: ECR repository is not encrypted with a customer managed KMS key", [resource.type, resource.name])
}

kms_encrypted(resource) if {
	cfg := resource.attributes.encryption_configuration[_]
	cfg.encryption_type == "KMS"
	cfg.kms_key
}
