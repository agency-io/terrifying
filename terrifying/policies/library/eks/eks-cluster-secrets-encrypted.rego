# title: eks-cluster-secrets-encrypted
# description: Detects EKS clusters without KMS encryption configured for Kubernetes secrets. Equivalent to AWS Config eks-secrets-encrypted. Maps to FSBP EKS.3 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_eks_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_eks_cluster"
	enc := resource.attributes.encryption_config[_]
	not "secrets" in enc.resources
	msg := sprintf("Resource %v.%v: secrets encryption not configured", [resource.type, resource.name])
}
