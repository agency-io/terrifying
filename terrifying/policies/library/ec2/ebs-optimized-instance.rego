# title: ebs-optimized-instance
# description: Detects running EC2 instances where EBS optimization is not enabled, limiting I/O throughput. Equivalent to AWS Config ebs-optimized-instance. Maps to FSBP EC2.7 (Medium).
# severity: Medium
# tags: security-hub, fsbp, nist-800-53, conformance-pack
# terraform_resources: aws_instance
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_instance"
	resource.attributes.ebs_optimized == false
	msg := sprintf("Resource %v.%v: EC2 instance does not have EBS optimization enabled", [resource.type, resource.name])
}
