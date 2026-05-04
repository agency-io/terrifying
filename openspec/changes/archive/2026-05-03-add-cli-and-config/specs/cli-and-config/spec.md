## ADDED Requirements

### Requirement: Configuration File

The system SHALL support a `terrifying.yml` file that configures which built-in rules are enabled and their parameters, the path to custom rules, and the directories for OPA and c7n policies. Any rule key not present is disabled by default.

#### Scenario: Rule enabled with parameters

- **WHEN** `terrifying.yml` contains `max_resources_per_file: {max: 8}`
- **THEN** `MaxResourcesPerFile` is instantiated with `max_resources=8` and included in the run

#### Scenario: Rule absent from config is disabled

- **WHEN** `terrifying.yml` does not mention `max_lines_per_file`
- **THEN** `MaxLinesPerFile` is not run

#### Scenario: Custom rule path configured

- **WHEN** `terrifying.yml` contains `custom: {path: ./rules/}`
- **THEN** all Python files in `./rules/` are discovered and any `Rule` subclasses found are instantiated and included in the run

### Requirement: CLI Check Command

The system SHALL provide a `terrifying check <directory>` command that parses the Terraform directory, loads config from `terrifying.yml` in the current working directory, runs all enabled rules and policy adapters, prints violations, and exits with code 0 if no errors are found or code 1 if any error-severity violations exist.

#### Scenario: No violations — exit 0

- **WHEN** all rules pass against the Terraform directory
- **THEN** the command prints a success message and exits with code 0

#### Scenario: Error violation found — exit 1

- **WHEN** at least one rule produces an error-severity violation
- **THEN** the command prints the violation details and exits with code 1

#### Scenario: Warning-only violations — exit 0

- **WHEN** only warning-severity violations are produced
- **THEN** the command prints the warnings and exits with code 0

### Requirement: Text Output Format

The system SHALL print violations in a human-readable format by default, showing the file path, line (if available), rule ID, severity, and message. One violation per line.

#### Scenario: Violation printed in text format

- **WHEN** a violation is produced and `--format text` is active (default)
- **THEN** the output line contains the file, rule ID, and message

### Requirement: JSON Output Format

The system SHALL support `--format json` which prints all violations as a JSON array, with each violation as an object containing `rule`, `file`, `line`, `message`, and `severity` fields.

#### Scenario: JSON output produced

- **WHEN** `--format json` is passed
- **THEN** stdout contains a valid JSON array of violation objects

### Requirement: Custom Rule Discovery

The system SHALL discover `Rule` subclasses from Python files in the directory configured under `custom.path`. Discovery SHALL import each file, inspect its classes, and include any that subclass `Rule` and are not `Rule` itself.

#### Scenario: Custom rule is discovered and run

- **WHEN** a Python file in the custom path defines a class extending `Rule`
- **THEN** that rule is instantiated with no arguments and included in the run

#### Scenario: Non-Rule classes are ignored

- **WHEN** a Python file in the custom path contains classes that do not extend `Rule`
- **THEN** those classes are not instantiated or run
