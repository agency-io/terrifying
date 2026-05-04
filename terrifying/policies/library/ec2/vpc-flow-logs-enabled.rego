# title: vpc-flow-logs-enabled
# description: Detects VPCs that do not have flow logs enabled, preventing network traffic visibility for security investigations.
# severity: Medium
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_vpc
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_vpc"
	not has_flow_log(resource)
	msg := sprintf("Resource %v.%v: VPC does not have flow logs enabled", [resource.type, resource.name])
}

has_flow_log(resource) if {
	flow_log := input.resources[_]
	flow_log.type == "aws_flow_log"
	flow_log.attributes.vpc_id == resource.attributes.id
}
