# policy-library Specification

## Purpose
TBD - created by archiving change add-policy-library. Update Purpose after archive.
## Requirements
### Requirement: Bundled Rego policy library
terrifying SHALL ship a curated library of shift-left-compatible Rego policies bundled inside the package at `terrifying/policies/library/<service>/<policy-id>.rego`. Each policy SHALL be rewritten from the Steampipe live-resource input schema to the terrifying TerraformContext input schema (`input.resources[_].attributes`). Each policy SHALL use `package terrifying` and populate the `deny` set. Runtime-only policies SHALL be excluded.

#### Scenario: Rego policy evaluates TerraformContext resources
- **WHEN** a bundled Rego policy is evaluated by the OPA adapter
- **THEN** it iterates `input.resources[_]`, filters by `resource.type`, and checks `resource.attributes`

#### Scenario: Rego policy uses deny convention
- **WHEN** a bundled Rego policy detects a violation
- **THEN** it adds a message string to the `deny` set (not `violation`)

#### Scenario: Runtime-only Rego policies excluded
- **WHEN** a source policy checks live state (instance state, key rotation age, last-accessed timestamps, EIP association, backup plan membership)
- **THEN** it is NOT included in the bundled Rego library

### Requirement: Bundled c7n policy library
terrifying SHALL ship a curated library of shift-left-compatible c7n-left policies bundled inside the package at `terrifying/policies/library/<service>/<policy-id>.yml`. Each policy SHALL be rewritten from CloudTrail event-driven runtime mode to c7n-left IaC-scanning format: `resource` SHALL use the `terraform.*` prefix, the `mode` block SHALL be removed, runtime-specific filters SHALL be replaced with attribute-based filters, and `actions` blocks SHALL be removed. Runtime-only policies SHALL be excluded.

#### Scenario: c7n policy uses terraform resource type
- **WHEN** a bundled c7n policy is passed to c7n-left
- **THEN** its `resource` field is `terraform.<resource_type>` (e.g. `terraform.aws_db_instance`)

#### Scenario: c7n policy has no mode block
- **WHEN** a bundled c7n policy file is read
- **THEN** it contains no `mode` key

#### Scenario: c7n policy has no actions block
- **WHEN** a bundled c7n policy file is read
- **THEN** it contains no `actions` key

#### Scenario: Runtime-only c7n policies excluded
- **WHEN** a source c7n policy uses filters that require live AWS state (e.g. `shield-enabled`, event-only checks)
- **THEN** it is NOT included in the bundled c7n library

### Requirement: Policy manifest
terrifying SHALL maintain a machine-readable manifest at `terrifying/policies/library/manifest.yaml`. Each entry SHALL describe one engine variant of one policy and SHALL include: `id`, `engine` (`rego` or `c7n`), `service`, `file` (relative path within the library), `description`, `severity`, `terraform_resources` (list of Terraform resource types), `tags`, and `params` (list of configurable parameter descriptors, empty list if none). A control implemented in both engines SHALL have two separate entries with the same `id` and different `engine` values.

#### Scenario: Control in both engines has two entries
- **WHEN** `rds-storage-encrypted` is implemented in both Rego and c7n
- **THEN** the manifest contains two entries: one with `engine: rego` and one with `engine: c7n`

#### Scenario: Manifest entry with params
- **WHEN** a policy uses `input.params.required_tags` (Rego) or `{{ required_tags }}` (c7n)
- **THEN** its manifest entry declares a param with `name`, `type`, `description`, and `default`

### Requirement: Tag taxonomy
Every bundled policy SHALL be tagged with compliance framework tags (`fsbp`, `cis-benchmark`, `pci-dss`, `nist-800-53`, `control-tower-mandatory`, `control-tower-strongly-recommended`, `control-tower-elective`), a service tag, a severity tag (`high`, `medium`, `low`), and an engine tag (`rego` or `c7n`). Tags SHALL be derived from the source policy metadata and normalized to kebab-case.

#### Scenario: Engine tag added automatically
- **WHEN** an entry has `engine: rego`
- **THEN** its tags include `rego`

#### Scenario: Service tag added automatically
- **WHEN** a policy lives in `library/rds/`
- **THEN** its tags include `rds`

### Requirement: Per-policy unit tests
Every bundled policy — both Rego and c7n — SHALL have a corresponding unit test that exercises at least one compliant fixture (no violation) and one non-compliant fixture (violation detected). A shared test-helper module (`tests/policies/library/helpers.py`) SHALL provide fixture builders and assertion utilities so that each individual test file requires minimal boilerplate. Rego policy tests SHALL invoke `opa test` (or `opa eval`) via subprocess against an inline input document. c7n-left policy tests SHALL write a minimal Terraform fixture to a temp directory and invoke `c7n-left` via subprocess, asserting on violations found.

#### Scenario: Rego policy passes for compliant resource
- **WHEN** the policy is evaluated against a TerraformContext containing a compliant resource (e.g. `storage_encrypted: true`)
- **THEN** `deny` is empty

#### Scenario: Rego policy fails for non-compliant resource
- **WHEN** the policy is evaluated against a TerraformContext containing a non-compliant resource (e.g. `storage_encrypted: false`)
- **THEN** `deny` contains a message identifying the resource

#### Scenario: c7n policy passes for compliant fixture
- **WHEN** `c7n-left` runs the policy against a Terraform fixture where the resource is compliant
- **THEN** no violations are reported

#### Scenario: c7n policy fails for non-compliant fixture
- **WHEN** `c7n-left` runs the policy against a Terraform fixture where the resource is non-compliant
- **THEN** a violation is reported for that resource

#### Scenario: Test helper reduces per-test boilerplate
- **WHEN** a new per-policy test is added
- **THEN** it uses helper functions from `tests/policies/library/helpers.py` and remains under 30 lines

