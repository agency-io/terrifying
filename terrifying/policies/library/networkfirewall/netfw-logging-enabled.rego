# title: netfw-logging-enabled
# description: Detects AWS Network Firewalls with no logging destinations configured. Equivalent to AWS Config FSBP NetworkFirewall.2.
# severity: Medium
# tags: security-hub, fsbp
# terraform_resources: aws_networkfirewall_firewall, aws_networkfirewall_logging_configuration
package terrifying

import rego.v1

deny contains msg if {
    firewall := input.resources[_]
    firewall.type == "aws_networkfirewall_firewall"
    not _has_logging_config(input.resources, firewall.name)
    msg := sprintf("Resource %v.%v: Network Firewall has no logging destinations configured", [firewall.type, firewall.name])
}

_has_logging_config(resources, firewall_name) if {
    r := resources[_]
    r.type == "aws_networkfirewall_logging_configuration"
    r.attributes.firewall_name == firewall_name
    count(r.attributes.logging_configuration[_].log_destination_config) > 0
}
