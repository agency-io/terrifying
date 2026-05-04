# title: eks-endpoint-no-public-access
# description: Detects EKS clusters with the Kubernetes API server endpoint publicly accessible. Equivalent to AWS Config eks-endpoint-no-public-access. Maps to FSBP EKS.1 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_eks_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_eks_cluster"
	resource.attributes.kubernetes_network_config[_].endpoint_public_access == true
	msg := sprintf("Resource %v.%v: EKS cluster has the Kubernetes API server endpoint publicly accessible", [resource.type, resource.name])
}
