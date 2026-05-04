# title: rds-proxy-tls-encryption
# description: Detects RDS proxies not configured to require TLS for client connections. Equivalent to AWS Config rds-proxy-tls-encryption.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_db_proxy
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_proxy"
    not resource.attributes.require_tls
    msg := sprintf("Resource %v.%v: RDS proxy does not require TLS for client connections", [resource.type, resource.name])
}
