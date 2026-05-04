# title: eks-cluster-log-enabled
# description: Detects EKS clusters where audit logging is disabled. Equivalent to AWS Config eks-cluster-log-enabled. Maps to FSBP EKS.8 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_eks_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_eks_cluster"
	not resource.attributes.enabled_cluster_log_types
	msg := sprintf("Resource %v.%v: EKS cluster does not have cluster logging enabled", [resource.type, resource.name])
}
