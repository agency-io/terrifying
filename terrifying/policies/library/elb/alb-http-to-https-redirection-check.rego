# title: alb-http-to-https-redirection-check
# description: Detects ALBs with HTTP listeners that do not redirect to HTTPS. Equivalent to AWS Config alb-http-to-https-redirection-check. Maps to FSBP ELB.1 (Critical).
# severity: Critical
# tags: security-hub, fsbp, cis-benchmark, pci-dss
# terraform_resources: aws_lb_listener
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_lb_listener"
	resource.attributes.protocol == "HTTP"
	not redirects_to_https(resource)
	msg := sprintf("Resource %v.%v: ALB listener uses HTTP but does not redirect to HTTPS", [resource.type, resource.name])
}

redirects_to_https(resource) if {
	action := resource.attributes.default_action[_]
	action.type == "redirect"
	action.redirect[_].protocol == "HTTPS"
}
