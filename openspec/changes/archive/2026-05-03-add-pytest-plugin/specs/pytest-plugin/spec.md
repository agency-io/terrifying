## ADDED Requirements

### Requirement: Automatic pytest collection
The plugin SHALL register with pytest via the `pytest11` entry point so that running `pytest` in a project with `terrifying.yml` automatically collects and runs architecture checks without any user-written test files.

#### Scenario: terrifying.yml present
- **WHEN** pytest is invoked in a directory containing `terrifying.yml`
- **THEN** one test item is collected per enabled rule and per configured policy adapter

#### Scenario: terrifying.yml absent
- **WHEN** pytest is invoked in a directory without `terrifying.yml`
- **THEN** no terrifying items are collected and pytest proceeds normally

### Requirement: Per-rule test items
Each enabled rule SHALL produce one `pytest.Item` named `terrifying::<rule_id>`.

#### Scenario: Rule passes
- **WHEN** a rule produces no error-severity violations
- **THEN** the corresponding test item passes

#### Scenario: Rule fails
- **WHEN** a rule produces one or more error-severity violations
- **THEN** the corresponding test item fails with a message listing each violation as `file:line [rule] message`

#### Scenario: Warning-only violations
- **WHEN** a rule produces only warning-severity violations
- **THEN** the corresponding test item passes

### Requirement: Terraform directory configuration
The Terraform directory to check SHALL default to the directory containing `terrifying.yml` and MAY be overridden via a `terraform.path` key in `terrifying.yml`.

#### Scenario: Default path
- **WHEN** `terrifying.yml` does not specify `terraform.path`
- **THEN** the directory containing `terrifying.yml` is parsed

#### Scenario: Explicit path
- **WHEN** `terrifying.yml` specifies `terraform.path: ./infra`
- **THEN** `./infra` (relative to `terrifying.yml`) is parsed

### Requirement: Parse error reporting
Parse errors encountered during HCL parsing SHALL be reported as a single test item named `terrifying::parse_errors`.

#### Scenario: Parse errors present
- **WHEN** one or more `.tf` files fail to parse
- **THEN** a `terrifying::parse_errors` item is collected and fails listing the affected files
