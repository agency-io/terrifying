# opa-integration Specification

## Purpose
TBD - created by archiving change add-opa-integration. Update Purpose after archive.
## Requirements
### Requirement: OPA Adapter

The system SHALL provide an `OpaAdapter` that discovers `.rego` files from a configured directory, serialises a `TerraformContext` to JSON, invokes `opa eval` as a subprocess for each policy file, and returns the results normalised as `Violation` objects.

#### Scenario: OPA policy produces a violation

- **WHEN** a `.rego` policy's `deny` set is non-empty for the given Terraform context
- **THEN** each element is converted to a `Violation` with `rule="opa:<filename>"` and the element's `msg` as the message

#### Scenario: OPA policy produces no violations

- **WHEN** a `.rego` policy's `deny` set is empty
- **THEN** no violations are produced for that policy

#### Scenario: OPA binary not on PATH

- **WHEN** `opa eval` cannot be found
- **THEN** a single `Violation` with `rule="opa_unavailable"` and `severity="error"` is returned, with a message directing the user to install OPA

#### Scenario: Policy directory is empty

- **WHEN** the configured policy directory contains no `.rego` files
- **THEN** no violations are produced and no subprocess is invoked

### Requirement: OPA Input Format

The system SHALL serialise `TerraformContext` to a JSON structure with `files` and `resources` arrays before passing it to `opa eval` as `--stdin-input`. Each resource SHALL include `type`, `name`, `attributes`, and `file` fields.

#### Scenario: Input includes all resources

- **WHEN** a context with two files each containing resources is serialised
- **THEN** the JSON input's `resources` array contains all resources from both files

### Requirement: OPA Violation Convention

The system SHALL document and support a `deny` set convention in Rego policies. Each element in `deny` SHALL be either a plain string (used as the message) or an object with a `msg` field and an optional `file` field. The adapter SHALL map each to a `Violation`.

#### Scenario: Plain string denial

- **WHEN** a Rego policy returns `deny["resource missing encryption"]`
- **THEN** the adapter produces a `Violation` with `message="resource missing encryption"`

#### Scenario: Structured denial with file

- **WHEN** a Rego policy returns `deny[{"msg": "missing tag", "file": "main.tf"}]`
- **THEN** the adapter produces a `Violation` with `message="missing tag"` and `file=Path("main.tf")`

