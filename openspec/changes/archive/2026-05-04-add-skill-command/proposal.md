# Change: Add `terrifying skill` CLI command

## Why

Users of the terrifying framework work in projects where Claude Code may not know how to write terrifying tests, use the bundled policy library, or configure `terrifying.yml`. A `terrifying skill` command outputs a ready-to-use Claude Code skill (`.claude/commands/terrifying.md`) that gives Claude the context it needs to assist effectively in any terrifying-powered project.

## What Changes

- Add `terrifying skill --format <fmt>` subcommand that prints a skill document to stdout
- `--format claude-code` (default) outputs a Claude Code slash command markdown file
- Unsupported formats print a message directing the user to raise a GitHub issue
- Users install with: `terrifying skill > .claude/commands/terrifying.md`

## Impact

- Affected specs: `cli`
- Affected code: `terrifying/cli.py`, new `terrifying/skill.py`
