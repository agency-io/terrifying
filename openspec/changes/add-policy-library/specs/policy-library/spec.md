## ADDED Requirements

### Requirement: Bundled policy library
terrifying SHALL ship a curated library of shift-left-compatible Rego policies bundled inside the package at `terrifying/policies/library/<service>/<policy-id>.rego`. Each policy SHALL be rewritten from the Steampipe live-resource input schema to the terrifying TerraformContext input schema (`input.resources[_].attributes`). Each policy SHALL use `package terrifying` and populate the `deny` set.

#### Scenario: Policy evaluates TerraformContext resources
- **WHEN** a bundled policy is evaluated by the OPA adapter
- **THEN** it iterates `input.resources[_]`, filters by `resource.type`, and checks `resource.attributes`

#### Scenario: Runtime-only policies excluded
- **WHEN** a source policy checks live state (instance state, key rotation age, last-accessed timestamps, EIP association, backup plan membership)
- **THEN** it is NOT included in the bundled library

#### Scenario: Policy uses deny convention
- **WHEN** a bundled policy detects a violation
- **THEN** it adds a message string to the `deny` set (not `violation`)

### Requirement: Policy manifest
terrifying SHALL maintain a machine-readable manifest at `terrifying/policies/library/manifest.yaml` describing every bundled policy. Each entry SHALL include: `id`, `service`, `file` (relative path within the library), `description`, `severity`, `terraform_resources` (list of Terraform resource types the policy targets), `tags` (list of kebab-case tag strings), and `params` (list of configurable parameter descriptors, empty list if none).

#### Scenario: Manifest entry with no params
- **WHEN** a policy requires no configurable values
- **THEN** its manifest entry has `params: []`

#### Scenario: Manifest entry with params
- **WHEN** a policy uses `input.params.required_tags`
- **THEN** its manifest entry declares a param with `name: required_tags`, `type: list[string]`, a description, and a default value

### Requirement: Tag taxonomy
Every bundled policy SHALL be tagged with one or more compliance framework tags (`fsbp`, `cis-benchmark`, `pci-dss`, `nist-800-53`, `control-tower`, `control-tower-mandatory`, `control-tower-strongly-recommended`, `control-tower-elective`), a service tag matching the AWS service directory name, and a severity tag (`high`, `medium`, `low`). Tags SHALL be derived from the METADATA block of the source policy and normalized to kebab-case.

#### Scenario: Policy tagged with framework
- **WHEN** the source policy METADATA lists `tags: [fsbp, cis-benchmark]`
- **THEN** the manifest entry carries `tags: [fsbp, cis-benchmark, ...]`

#### Scenario: Service tag added automatically
- **WHEN** a policy lives in `library/s3/`
- **THEN** its manifest tags include `s3`
