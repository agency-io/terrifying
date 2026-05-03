package terrifying

import rego.v1

# Deny any resource missing the Team tag.
deny contains msg if {
    resource := input.resources[_]
    not resource.attributes.tags.Team
    msg := sprintf("Resource %v.%v is missing required tag 'Team'", [resource.type, resource.name])
}

# Deny any resource missing the Environment tag.
deny contains msg if {
    resource := input.resources[_]
    not resource.attributes.tags.Environment
    msg := sprintf("Resource %v.%v is missing required tag 'Environment'", [resource.type, resource.name])
}
