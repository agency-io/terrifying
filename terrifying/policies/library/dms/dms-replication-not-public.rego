# title: dms-replication-not-public
# description: Detects DMS replication instances configured with publicly accessible enabled, exposing database migration traffic to the internet. Equivalent to AWS Config dms-replication-not-public. Maps to FSBP DMS.1 (Critical).
# severity: Critical
# tags: security-hub, fsbp
# terraform_resources: aws_dms_replication_instance
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_dms_replication_instance"
	resource.attributes.publicly_accessible == true
	msg := sprintf("Resource %v.%v: DMS replication instance is publicly accessible", [resource.type, resource.name])
}
