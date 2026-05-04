package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    tag := input.params.required_tags[_]
    not resource.attributes.tags[tag]
    msg := sprintf("Resource %v.%v is missing required tag '%v'", [resource.type, resource.name, tag])
}
