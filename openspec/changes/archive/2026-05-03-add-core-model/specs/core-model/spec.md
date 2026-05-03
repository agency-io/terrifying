## ADDED Requirements

### Requirement: HCL Parser

The system SHALL parse all `.tf` files in a given directory into `TerraformFile` objects using python-hcl2. Files that cannot be parsed SHALL produce a `Violation` with severity `error` and rule `parse_error`, and parsing SHALL continue for remaining files.

#### Scenario: Valid directory is parsed

- **WHEN** a directory containing `.tf` files is given to the parser
- **THEN** a `TerraformFile` is produced for each `.tf` file
- **AND** each file contains its resources, variables, outputs, locals, and module calls

#### Scenario: Unparseable file produces a violation

- **WHEN** a `.tf` file contains invalid HCL syntax
- **THEN** a `Violation` is returned with `rule="parse_error"` and `severity="error"`
- **AND** parsing continues for all other files in the directory

### Requirement: TerraformContext

The system SHALL provide a `TerraformContext` object that aggregates all `TerraformFile` objects for a checked directory and exposes a flat view of all resources across files.

#### Scenario: Context aggregates files

- **WHEN** a directory with multiple `.tf` files is parsed
- **THEN** `context.files` contains one `TerraformFile` per file
- **AND** `context.resources` contains all resources across all files

### Requirement: TerraformFile

The system SHALL provide a `TerraformFile` object with the following attributes:
- `path: Path` — absolute path to the file
- `resources: list[Resource]`
- `variables: list[Variable]`
- `outputs: list[Output]`
- `locals: list[Local]`
- `module_calls: list[ModuleCall]`
- `line_count: int`

#### Scenario: File attributes are populated

- **WHEN** a `.tf` file defining resources, variables, and outputs is parsed
- **THEN** the corresponding lists on `TerraformFile` are populated
- **AND** `line_count` reflects the number of lines in the file

### Requirement: Resource Value Object

The system SHALL provide a `Resource` value object with:
- `type: str` — e.g. `"aws_s3_bucket"`
- `name: str` — logical name in the Terraform config
- `attributes: dict` — raw attribute values as parsed
- `file: Path` — source file
- `line: int | None` — line number if available

#### Scenario: Resource is identified

- **WHEN** a `.tf` file contains `resource "aws_s3_bucket" "my_bucket" { ... }`
- **THEN** a `Resource` with `type="aws_s3_bucket"` and `name="my_bucket"` is produced

### Requirement: Variable Value Object

The system SHALL provide a `Variable` value object with:
- `name: str`
- `description: str | None`
- `default: object | None`
- `type: str | None`
- `file: Path`
- `line: int | None`

#### Scenario: Variable is identified

- **WHEN** a `.tf` file contains a `variable` block
- **THEN** a `Variable` with the correct name, description, and default is produced

### Requirement: Output Value Object

The system SHALL provide an `Output` value object with:
- `name: str`
- `description: str | None`
- `value: object`
- `file: Path`
- `line: int | None`

#### Scenario: Output is identified

- **WHEN** a `.tf` file contains an `output` block
- **THEN** an `Output` with the correct name and description is produced

### Requirement: ModuleCall Value Object

The system SHALL provide a `ModuleCall` value object with:
- `name: str`
- `source: str`
- `arguments: dict`
- `file: Path`
- `line: int | None`

#### Scenario: Module call is identified

- **WHEN** a `.tf` file contains a `module` block
- **THEN** a `ModuleCall` with the correct name and source is produced

### Requirement: Rule Base Class

The system SHALL provide a `Rule` base class with a `rule_id` property that derives the ID from the subclass name by converting it to snake_case. Subclasses SHALL implement `check(context: TerraformContext) -> list[Violation]`.

#### Scenario: Rule ID derived from class name

- **WHEN** a class named `MaxResourcesPerFile` extends `Rule`
- **THEN** `instance.rule_id` returns `"max_resources_per_file"`

#### Scenario: Rule check is called by runner

- **WHEN** the runner executes a rule
- **THEN** `rule.check(context)` is called with the full `TerraformContext`
- **AND** the returned violations are collected into the run results

### Requirement: Violation Dataclass

The system SHALL provide a `Violation` dataclass with fields:
- `rule: str` — the `rule_id` of the rule that produced it
- `file: Path` — the file where the violation was found
- `line: int | None` — line number if available
- `message: str` — human-readable description
- `severity: str` — `"error"` or `"warning"`, defaulting to `"error"`

#### Scenario: Violation is created by a rule

- **WHEN** a rule's `check()` method identifies a problem
- **THEN** it returns a `Violation` with `rule`, `file`, and `message` populated

### Requirement: Runner

The system SHALL provide a `Runner` that accepts a list of `Rule` instances and a `TerraformContext`, calls `check()` on each rule, and returns all violations as a flat list.

#### Scenario: Runner collects violations from multiple rules

- **WHEN** two rules each produce one violation against the same context
- **THEN** the runner returns a list containing both violations

#### Scenario: Runner returns empty list when no violations

- **WHEN** all rules pass against the context
- **THEN** the runner returns an empty list
