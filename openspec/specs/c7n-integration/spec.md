# c7n-integration Specification

## Purpose
TBD - created by archiving change add-c7n-integration. Update Purpose after archive.
## Requirements
### Requirement: c7n Adapter

The system SHALL provide a `C7nAdapter` that accepts a policy directory and a Terraform directory, invokes `c7n-left run --policy <policy_dir> --directory <tf_dir> --output json` as a subprocess, parses the JSON output, and returns results normalised as `Violation` objects.

#### Scenario: c7n policy finds a violation

- **WHEN** a c7n YAML policy matches a resource in the Terraform directory
- **THEN** each match is converted to a `Violation` with `rule="c7n:<policy_name>"`, the resource file as `file`, and the policy match reason as `message`

#### Scenario: c7n policy finds no violations

- **WHEN** all resources in the Terraform directory pass the c7n policies
- **THEN** no violations are produced

#### Scenario: c7n-left binary not on PATH

- **WHEN** `c7n-left` cannot be found
- **THEN** a single `Violation` with `rule="c7n_unavailable"` and `severity="error"` is returned, directing the user to install `c7n-left`

#### Scenario: Policy directory is empty

- **WHEN** the configured policy directory contains no YAML files
- **THEN** no violations are produced and no subprocess is invoked

### Requirement: c7n Violation Mapping

The system SHALL map c7n-left JSON output fields to `Violation` fields as follows:
- `policy.name` → `rule` (prefixed with `"c7n:"`)
- `resource.filename` → `file`
- `resource.line_start` → `line` (if available)
- Policy match description → `message`

#### Scenario: File and line populated from c7n output

- **WHEN** c7n-left output includes `filename` and `line_start` for a match
- **THEN** the resulting `Violation` has `file` and `line` set accordingly

