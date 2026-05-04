# title: emr-master-no-public-ip
# description: Detects EMR clusters not launched in a VPC subnet, where the master node may receive a public IP exposing management interfaces. Equivalent to FSBP EMR.1.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_emr_cluster
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_emr_cluster"
	not resource.attributes.ec2_attributes
	msg := sprintf("Resource %v.%v: EMR cluster is not launched in a VPC subnet — master node may have a public IP", [resource.type, resource.name])
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_emr_cluster"
	ec2_attrs := resource.attributes.ec2_attributes[_]
	not ec2_attrs.subnet_id
	msg := sprintf("Resource %v.%v: EMR cluster is not launched in a VPC subnet — master node may have a public IP", [resource.type, resource.name])
}
