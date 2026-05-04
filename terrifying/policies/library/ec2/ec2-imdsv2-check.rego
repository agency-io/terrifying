# title: ec2-imdsv2-check
# description: Detects EC2 instances that do not require IMDSv2, leaving them vulnerable to SSRF-based credential theft. Equivalent to AWS Config ec2-imdsv2-check. Maps to FSBP EC2.8 (High), CIS 5.6, PCI DSS.
# severity: High
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_instance
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_instance"
	not resource.attributes.metadata_options
	msg := sprintf("Resource %v.%v: IMDSv2 is not enforced (metadata_options not set)", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_instance"
	resource.attributes.metadata_options[_].http_tokens != "required"
	msg := sprintf("Resource %v.%v: IMDSv2 is not enforced (http_tokens is not required)", [resource.type, resource.name])
}
