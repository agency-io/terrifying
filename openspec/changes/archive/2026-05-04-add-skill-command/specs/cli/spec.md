## ADDED Requirements

### Requirement: Skill Command
The CLI SHALL provide a `skill` subcommand with a `--format` flag (default: `claude-code`) that writes an AI assistant skill document to stdout.

#### Scenario: Claude Code format output
- **WHEN** the user runs `terrifying skill` or `terrifying skill --format claude-code`
- **THEN** a markdown document is printed to stdout suitable for use as a Claude Code slash command
- **AND** the document covers writing Rego and c7n tests, using `terrifying add`, and configuring `terrifying.yml`

#### Scenario: Pipeable to Claude Code commands directory
- **WHEN** the user runs `terrifying skill > .claude/commands/terrifying.md`
- **THEN** the file is created and usable as a Claude Code slash command

#### Scenario: Unsupported format
- **WHEN** the user runs `terrifying skill --format <unsupported>`
- **THEN** a message is printed to stdout indicating the format is not yet supported
- **AND** the message includes the GitHub issues URL so the user can request support
