# title: internet-gateway-authorized-vpc-only
# description: Flags internet gateways attached to any VPC for review to ensure only authorized VPCs have internet gateway attachments. Maps to conformance-pack (Medium).
# severity: Medium
# tags: conformance-pack
# terraform_resources: aws_internet_gateway
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_internet_gateway"
	resource.attributes.vpc_id
	msg := sprintf("Resource %v.%v: internet gateway is attached to a VPC — verify attachment is authorized", [resource.type, resource.name])
}
