# title: ec2-transit-gateway-auto-vpc-attach-disabled
# description: Detects Transit Gateways with AutoAcceptSharedAttachments enabled, allowing any account to attach VPCs without approval. Equivalent to AWS Config ec2-transit-gateway-auto-vpc-attach-disabled. Maps to FSBP EC2.23 (High).
# severity: High
# tags: security-hub, fsbp, conformance-pack
# terraform_resources: aws_ec2_transit_gateway
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ec2_transit_gateway"
	resource.attributes.auto_accept_shared_attachments == "enable"
	msg := sprintf("Resource %v.%v: Transit Gateway has auto_accept_shared_attachments enabled", [resource.type, resource.name])
}
