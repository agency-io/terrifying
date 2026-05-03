## ADDED Requirements

### Requirement: Max Resources Per File

The system SHALL provide a `MaxResourcesPerFile` rule that produces a `Violation` for any file whose resource count exceeds a configurable maximum (default: 10).

#### Scenario: File within limit passes

- **WHEN** a file defines fewer resources than the configured maximum
- **THEN** no violation is produced for that file

#### Scenario: File exceeding limit fails

- **WHEN** a file defines more resources than the configured maximum
- **THEN** a violation is produced naming the file and the count

#### Scenario: Rule ID is derived from class name

- **WHEN** the rule is instantiated
- **THEN** `rule.rule_id` returns `"max_resources_per_file"`

### Requirement: Max Lines Per File

The system SHALL provide a `MaxLinesPerFile` rule that produces a `Violation` for any file whose line count exceeds a configurable maximum (default: 150).

#### Scenario: File within limit passes

- **WHEN** a file has fewer lines than the configured maximum
- **THEN** no violation is produced for that file

#### Scenario: File exceeding limit fails

- **WHEN** a file has more lines than the configured maximum
- **THEN** a violation is produced naming the file and the line count

#### Scenario: Rule ID is derived from class name

- **WHEN** the rule is instantiated
- **THEN** `rule.rule_id` returns `"max_lines_per_file"`

### Requirement: Resource File Naming

The system SHALL provide a `ResourceFileNaming` rule that produces a `Violation` for any `.tf` file whose name does not match a configurable regex pattern.

#### Scenario: Correctly named file passes

- **WHEN** a file name matches the configured pattern
- **THEN** no violation is produced for that file

#### Scenario: Incorrectly named file fails

- **WHEN** a file name does not match the configured pattern
- **THEN** a violation is produced naming the file and the expected pattern

#### Scenario: Rule ID is derived from class name

- **WHEN** the rule is instantiated
- **THEN** `rule.rule_id` returns `"resource_file_naming"`
