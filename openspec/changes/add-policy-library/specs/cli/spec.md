## ADDED Requirements

### Requirement: terrifying add — interactive TUI mode
The CLI SHALL provide a `terrifying add` subcommand that launches a full-screen TUI (built with `textual`) when invoked with no arguments. The TUI SHALL display a tag browser panel and a policy list panel. Selecting a tag SHALL filter the policy list to policies carrying that tag. The user SHALL be able to toggle individual policies on/off and select all visible policies at once.

#### Scenario: TUI launched with no args
- **WHEN** the user runs `terrifying add` with no arguments
- **THEN** the TUI opens showing all available tags and policies

#### Scenario: Tag filter narrows policy list
- **WHEN** the user selects the `fsbp` tag
- **THEN** only policies tagged `fsbp` are shown in the policy list panel

#### Scenario: Policy detail shown on selection
- **WHEN** the user highlights a policy in the list
- **THEN** the detail pane shows its description, severity, Terraform resource types, and tags

#### Scenario: Select all visible
- **WHEN** the user presses A
- **THEN** all currently visible (filtered) policies are toggled on

### Requirement: terrifying add — non-interactive mode
The CLI SHALL accept one or more policy IDs as positional arguments to `terrifying add` and add those policies directly without launching the TUI.

#### Scenario: Non-interactive add by ID
- **WHEN** the user runs `terrifying add s3-bucket-server-side-encryption-enabled rds-storage-encrypted`
- **THEN** those two policies are added without launching the TUI

#### Scenario: Unknown policy ID
- **WHEN** a supplied policy ID does not exist in the manifest
- **THEN** the CLI prints an error listing the unknown ID and exits with code 1

### Requirement: Confirmation delta before writing
Before writing any files the CLI SHALL print a confirmation summary showing: the list of `.rego` files that will be created (with destination paths), and a unified diff of the changes that will be made to `terrifying.yml`. The user SHALL be prompted to confirm before any file is written.

#### Scenario: Delta shown before apply
- **WHEN** the user confirms their selection
- **THEN** the CLI prints the file list and terrifying.yml diff, then prompts `Apply? [y/N]`

#### Scenario: User declines
- **WHEN** the user answers N
- **THEN** no files are written and no changes are made to terrifying.yml

#### Scenario: Dry run flag
- **WHEN** the user passes `--dry-run`
- **THEN** the CLI prints the delta but does not write any files or prompt for confirmation

### Requirement: Policy file output
The CLI SHALL write each selected policy's `.rego` file to the OPA policies directory configured in `terrifying.yml` (`policies.opa.path`). If `policies.opa` is not yet configured, the CLI SHALL default to `./policies/opa/` and add the section to `terrifying.yml`. The CLI SHALL NOT overwrite an existing `.rego` file with the same name; instead it SHALL print a warning and skip that file.

#### Scenario: Files written to configured path
- **WHEN** `terrifying.yml` has `policies.opa.path: ./infra/policies`
- **THEN** `.rego` files are written under `./infra/policies/`

#### Scenario: Default path when unconfigured
- **WHEN** `terrifying.yml` has no `policies.opa` section
- **THEN** files are written to `./policies/opa/` and `terrifying.yml` is updated to add `policies.opa.path: ./policies/opa`

#### Scenario: Existing file not overwritten
- **WHEN** the target `.rego` file already exists
- **THEN** the CLI prints a warning, skips that file, and continues with remaining files

### Requirement: Param injection into terrifying.yml
For each selected policy that declares configurable params, the CLI SHALL prompt the user for a value (showing the default). Param values SHALL be written into `terrifying.yml` under `policies.opa.params`. Params already present in `terrifying.yml` SHALL NOT be overwritten; the CLI SHALL inform the user that the existing value will be kept.

#### Scenario: Param prompted and injected
- **WHEN** a selected policy declares `required_tags` with default `[Environment, Team]`
- **AND** `required_tags` is not yet in `terrifying.yml`
- **THEN** the CLI prompts `required_tags [Environment, Team]:` and writes the value to `policies.opa.params.required_tags`

#### Scenario: Existing param preserved
- **WHEN** `required_tags` is already present in `terrifying.yml`
- **THEN** the CLI prints `required_tags already set — keeping existing value` and does not overwrite it

#### Scenario: User accepts default
- **WHEN** the user presses Enter without typing a value
- **THEN** the default value is used

### Requirement: textual optional dependency
`textual` SHALL be an optional dependency declared as an extras group (`terrifying[tui]`). If `textual` is not installed and the user runs `terrifying add` without policy ID arguments, the CLI SHALL print a clear error message instructing the user to install `terrifying[tui]`.

#### Scenario: textual missing, TUI requested
- **WHEN** textual is not installed
- **AND** the user runs `terrifying add` with no arguments
- **THEN** the CLI prints `TUI requires textual: pip install terrifying[tui]` and exits with code 1

#### Scenario: textual missing, non-interactive works
- **WHEN** textual is not installed
- **AND** the user runs `terrifying add <policy-id>`
- **THEN** the policy is added without requiring textual
