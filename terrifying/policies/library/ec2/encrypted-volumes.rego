# title: encrypted-volumes
# description: Detects attached EBS volumes that are not encrypted at rest. Equivalent to AWS Config encrypted-volumes. Maps to CT Mandatory, FSBP EC2.3, CIS 2.2.1, PCI DSS.
# severity: High
# tags: control-tower, control-tower-mandatory, security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_ebs_volume
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_ebs_volume"
	not resource.attributes.encrypted
	msg := sprintf("Resource %v.%v: EBS volume is not encrypted", [resource.type, resource.name])
}
