# title: elbv2-predefined-security-policy-ssl-check
# description: Detects ALB/NLB HTTPS or TLS listeners using outdated SSL security policies instead of recommended TLS 1.2+ policies. Equivalent to FSBP ELB.17 (Medium).
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_lb_listener
package terrifying

import rego.v1

recommended_policies := {
	"ELBSecurityPolicy-TLS13-1-2-2021-06",
	"ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
	"ELBSecurityPolicy-TLS13-1-2-Ext1-2021-06",
	"ELBSecurityPolicy-TLS13-1-2-Ext2-2021-06",
	"ELBSecurityPolicy-TLS13-1-3-2021-06",
	"ELBSecurityPolicy-FS-1-2-Res-2020-10",
	"ELBSecurityPolicy-FS-1-2-Res-2019-08",
	"ELBSecurityPolicy-FS-1-2-2019-08",
}

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb_listener"
	resource.attributes.protocol in {"HTTPS", "TLS"}
	ssl_policy := resource.attributes.ssl_policy
	not ssl_policy in recommended_policies
	msg := sprintf("Resource %v.%v: Load balancer listener uses non-recommended SSL policy '%v'", [resource.type, resource.name, ssl_policy])
}
