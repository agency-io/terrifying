# title: eks-cluster-supported-version
# description: Detects EKS clusters running Kubernetes versions older than 1.28 which no longer receive security patches. Equivalent to AWS Config eks-cluster-supported-version. Maps to FSBP EKS.2 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_eks_cluster
package terrifying

import rego.v1

minimum_version := "1.28"

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_eks_cluster"
	resource.attributes.version < minimum_version
	msg := sprintf("Resource %v.%v: EKS cluster runs Kubernetes version '%v' which is below the minimum supported version %v", [resource.type, resource.name, resource.attributes.version, minimum_version])
}
