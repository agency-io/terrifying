# best-practice-rules Specification

## Purpose
TBD - created by archiving change add-best-practice-rules. Update Purpose after archive.
## Requirements
### Requirement: No Hardcoded Values

The system SHALL provide a `NoHardcodedValues` rule that produces a `Violation` for any resource attribute whose value is a plain string or number literal rather than a reference to `var.*`, `local.*`, or `data.*`. A configurable `allowed_attributes` list SHALL exclude attributes that are legitimately hardcoded (e.g. `lifecycle`, `depends_on`).

#### Scenario: Parameterised attribute passes

- **WHEN** a resource attribute value is `var.region` or `local.env`
- **THEN** no violation is produced for that attribute

#### Scenario: Literal string attribute fails

- **WHEN** a resource attribute value is a plain string literal not in the allowed list
- **THEN** a violation is produced naming the resource, attribute, and value

#### Scenario: Allowed attribute is exempt

- **WHEN** an attribute name is in the configured `allowed_attributes` list
- **THEN** no violation is produced regardless of its value

### Requirement: Variables Have Descriptions

The system SHALL provide a `VariablesHaveDescriptions` rule that produces a `Violation` for any `variable` block that has no `description` field or has an empty description.

#### Scenario: Variable with description passes

- **WHEN** a variable block has a non-empty `description`
- **THEN** no violation is produced

#### Scenario: Variable without description fails

- **WHEN** a variable block has no `description` or an empty one
- **THEN** a violation is produced naming the variable and file

### Requirement: Outputs Have Descriptions

The system SHALL provide a `OutputsHaveDescriptions` rule that produces a `Violation` for any `output` block that has no `description` field or has an empty description.

#### Scenario: Output with description passes

- **WHEN** an output block has a non-empty `description`
- **THEN** no violation is produced

#### Scenario: Output without description fails

- **WHEN** an output block has no `description` or an empty one
- **THEN** a violation is produced naming the output and file

### Requirement: Required Tags

The system SHALL provide a `RequiredTags` rule that accepts a configurable list of required tag keys and produces a `Violation` for any resource whose `tags` attribute is missing one or more of those keys.

#### Scenario: Resource with all required tags passes

- **WHEN** a resource's `tags` attribute contains all configured required keys
- **THEN** no violation is produced

#### Scenario: Resource missing a required tag fails

- **WHEN** a resource's `tags` attribute is missing one or more required keys
- **THEN** a violation is produced naming the resource and the missing tags

#### Scenario: Resource with no tags block fails

- **WHEN** a resource has no `tags` attribute and required tags are configured
- **THEN** a violation is produced

