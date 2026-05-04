## ADDED Requirements

### Requirement: terrifying add — engine selection
The `terrifying add` command SHALL require the user to specify which policy engine they want: `rego`, `c7n`, or `both`. In TUI mode this SHALL be presented as a radio-button selection at the top of the screen before the policy browser. In non-interactive mode it SHALL be controlled by a `--engine rego|c7n|both` flag (default: `both`).

#### Scenario: TUI engine selection presented first
- **WHEN** the TUI opens
- **THEN** the user sees an engine selector (Rego / c7n / Both) before the policy list

#### Scenario: Engine filter applied to policy list
- **WHEN** the user selects `rego`
- **THEN** only policies with `engine: rego` in the manifest are shown in the policy list

#### Scenario: Both engines shows all policies with engine badge
- **WHEN** the user selects `both`
- **THEN** all policies are shown; policies available in both engines display both `[R]` and `[C]` badges

#### Scenario: Non-interactive engine flag
- **WHEN** the user runs `terrifying add rds-storage-encrypted --engine c7n`
- **THEN** only the c7n variant of that policy is added

### Requirement: terrifying add — interactive TUI mode
The CLI SHALL provide a `terrifying add` subcommand that launches a full-screen TUI (built with `textual`) when invoked with no policy-ID arguments. The TUI SHALL display a tag browser panel and a policy list panel. Selecting a tag SHALL filter the policy list to policies carrying that tag. The user SHALL be able to toggle individual policies on/off and select all visible policies at once.

#### Scenario: TUI launched with no args
- **WHEN** the user runs `terrifying add` with no arguments
- **THEN** the TUI opens showing the engine selector, tag browser, and policy list

#### Scenario: Tag filter narrows policy list
- **WHEN** the user selects the `fsbp` tag in the tag browser
- **THEN** only policies tagged `fsbp` are shown in the policy list panel

#### Scenario: Policy detail shown on selection
- **WHEN** the user highlights a policy in the list
- **THEN** the detail pane shows its description, severity, Terraform resource types, tags, and engine

#### Scenario: Select all visible
- **WHEN** the user presses A
- **THEN** all currently visible (filtered) policies are toggled on

### Requirement: terrifying add — non-interactive mode
The CLI SHALL accept one or more policy IDs as positional arguments to `terrifying add` and add those policies directly without launching the TUI.

#### Scenario: Non-interactive add by ID
- **WHEN** the user runs `terrifying add s3-bucket-server-side-encryption-enabled rds-storage-encrypted`
- **THEN** those policies are added for all available engines (or the engine specified by `--engine`) without launching the TUI

#### Scenario: Unknown policy ID
- **WHEN** a supplied policy ID does not exist in the manifest for the selected engine
- **THEN** the CLI prints an error listing the unknown ID and exits with code 1

### Requirement: Confirmation delta before writing
Before writing any files the CLI SHALL print a confirmation summary showing: the list of files that will be created (with destination paths and engine labels), and a unified diff of the changes that will be made to `terrifying.yml`. The user SHALL be prompted to confirm before any file is written.

#### Scenario: Delta shown before apply
- **WHEN** the user confirms their selection
- **THEN** the CLI prints the file list (with `[rego]` or `[c7n]` labels) and the terrifying.yml diff, then prompts `Apply? [y/N]`

#### Scenario: User declines
- **WHEN** the user answers N
- **THEN** no files are written and no changes are made to terrifying.yml

#### Scenario: Dry run flag
- **WHEN** the user passes `--dry-run`
- **THEN** the CLI prints the delta but does not write any files or prompt for confirmation

### Requirement: Policy file output
The CLI SHALL write Rego files to the path configured under `policies.opa.path` in `terrifying.yml` (default `./policies/opa/`) and c7n files to `policies.c7n.path` (default `./policies/c7n/`). If a section is not yet configured, the CLI SHALL add it to `terrifying.yml`. The CLI SHALL NOT overwrite an existing file with the same name; it SHALL print a warning and skip that file.

#### Scenario: Rego files written to OPA path
- **WHEN** `terrifying.yml` has `policies.opa.path: ./infra/opa`
- **THEN** `.rego` files are written under `./infra/opa/`

#### Scenario: c7n files written to c7n path
- **WHEN** `terrifying.yml` has `policies.c7n.path: ./infra/c7n`
- **THEN** `.yml` files are written under `./infra/c7n/`

#### Scenario: Default paths when unconfigured
- **WHEN** `terrifying.yml` has no `policies` section
- **THEN** Rego files go to `./policies/opa/` and c7n files go to `./policies/c7n/`, and both paths are added to `terrifying.yml`

#### Scenario: Existing file not overwritten
- **WHEN** the target file already exists
- **THEN** the CLI prints a warning, skips that file, and continues

### Requirement: Param injection into terrifying.yml
For each selected policy that declares configurable params, the CLI SHALL prompt the user for a value (showing the default). Rego params SHALL be written into `policies.opa.params`; c7n params SHALL be written into `policies.c7n.params`. When the same param name is required by both a Rego and a c7n policy being added simultaneously, the CLI SHALL prompt once and write to both sections. Params already present in `terrifying.yml` SHALL NOT be overwritten.

#### Scenario: Shared param prompted once, written to both sections
- **WHEN** selected policies include a Rego and a c7n variant that both declare `required_tags`
- **THEN** the CLI prompts for `required_tags` once and writes it to both `policies.opa.params` and `policies.c7n.params`

#### Scenario: Existing param preserved
- **WHEN** `required_tags` is already present in `terrifying.yml`
- **THEN** the CLI prints `required_tags already set — keeping existing value` and does not overwrite it

### Requirement: textual optional dependency
`textual` SHALL be an optional dependency declared as an extras group (`terrifying[tui]`). If `textual` is not installed and the user runs `terrifying add` without policy ID arguments, the CLI SHALL print an error instructing the user to install `terrifying[tui]`. Non-interactive mode SHALL work without `textual`.

#### Scenario: textual missing, TUI requested
- **WHEN** textual is not installed and the user runs `terrifying add` with no arguments
- **THEN** the CLI prints `TUI requires textual: pip install terrifying[tui]` and exits with code 1

#### Scenario: textual missing, non-interactive works
- **WHEN** textual is not installed and the user runs `terrifying add <policy-id>`
- **THEN** the policy is added without requiring textual
