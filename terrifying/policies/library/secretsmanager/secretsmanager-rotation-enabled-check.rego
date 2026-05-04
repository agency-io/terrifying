# title: secretsmanager-rotation-enabled-check
# description: Detects Secrets Manager secrets that do not have automatic rotation enabled.
# severity: High
# tags: security-hub, fsbp, pci-dss, nist-800-53
# terraform_resources: aws_secretsmanager_secret, aws_secretsmanager_secret_rotation
package terrifying

import rego.v1

deny contains msg if {
    secret := input.resources[_]
    secret.type == "aws_secretsmanager_secret"
    not _has_rotation(input.resources, secret.name)
    msg := sprintf("Resource %v.%v: Secrets Manager secret rotation is not configured", [secret.type, secret.name])
}

_has_rotation(resources, secret_name) if {
    r := resources[_]
    r.type == "aws_secretsmanager_secret_rotation"
    r.attributes.secret_id == secret_name
}
