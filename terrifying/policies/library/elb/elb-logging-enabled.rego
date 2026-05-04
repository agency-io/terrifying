# title: elb-logging-enabled
# description: Detects Application Load Balancers without S3 access logging enabled. Equivalent to AWS Config elb-logging-enabled. Maps to FSBP ELB.5 (Medium).
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss, nist-800-53
# terraform_resources: aws_lb
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	not resource.attributes.access_logs
	msg := sprintf("Resource %v.%v: Load balancer does not have access logging configured", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb"
	access_logs := resource.attributes.access_logs[_]
	not access_logs.enabled
	msg := sprintf("Resource %v.%v: Load balancer does not have access logging enabled", [resource.type, resource.name])
}
