## ADDED Requirements

### Requirement: Global policy parameters
Both OPA and c7n sections in `terrifying.yml` SHALL support a `params` key containing
default parameter values applied to every policy in that section.

#### Scenario: Global params defined
- **WHEN** `policies.opa.params` defines `required_tags: [Environment, Team]`
- **THEN** every OPA policy receives `input.params.required_tags == ["Environment", "Team"]`

#### Scenario: No params defined
- **WHEN** no `params` key is present
- **THEN** policies receive `input.params == {}`

### Requirement: Per-policy parameter overrides
Individual policies SHALL support a `params` key that is merged over global params,
with policy-level values winning on conflict.

#### Scenario: Policy overrides global param
- **WHEN** global params define `required_tags: [Environment, Team]` and policy `require_encryption` defines `required_tags: [Environment]`
- **THEN** `require_encryption` receives `input.params.required_tags == ["Environment"]`

#### Scenario: Non-overlapping params merged
- **WHEN** global params define `required_tags: [Environment]` and policy params define `algorithm: AES256`
- **THEN** the policy receives both `required_tags` and `algorithm` in `input.params`

### Requirement: OPA parameter injection
Merged params SHALL be injected into the OPA input document as `input.params` alongside
the existing Terraform context fields.

#### Scenario: Params accessible in Rego
- **WHEN** `input.params.required_tags` is set
- **THEN** Rego policies can reference `input.params.required_tags[_]` to iterate over tag names

### Requirement: c7n Jinja2 template rendering
c7n policy files SHALL be treated as Jinja2 templates. Merged params are passed as
template variables and the rendered YAML is passed to `c7n-left`. Original files are
never modified.

#### Scenario: Template rendered with params
- **WHEN** a policy file contains `{{ required_tags[0] }}` and `required_tags: [Environment]` is configured
- **THEN** `c7n-left` receives rendered YAML with `Environment` substituted

#### Scenario: Template with loop
- **WHEN** a policy file uses `{% for tag in required_tags %}` iteration
- **THEN** the rendered YAML contains one policy block per tag

#### Scenario: Plain YAML passthrough
- **WHEN** a policy file contains no Jinja2 syntax
- **THEN** it is passed to `c7n-left` unchanged

### Requirement: Backward compatibility
The adapter SHALL accept a plain string path for `policies.opa` and `policies.c7n` (old format) and treat it as a `PolicyConfig` with empty params, preserving existing behaviour.

#### Scenario: Plain path string
- **WHEN** `policies.opa: ./policies/opa` (plain string, old format)
- **THEN** the adapter runs with no params, behaviour identical to before this change
