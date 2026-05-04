# Change: Add CLI and Configuration

## Why

A library without an entry point is not useful in CI/CD. The CLI and config layer ties everything together: it reads `terrifying.yml` to know which rules and adapters to enable with what parameters, runs them against a Terraform directory, and exits non-zero if any errors are found.

## What Changes

- Implement `terrifying.yml` config schema — rules section (enable/disable, parameters), policies section (OPA and c7n directories)
- Implement `ConfigLoader` — reads and validates `terrifying.yml`
- Implement CLI entry point `terrifying check <directory>` using the config to assemble rules and adapters, run them, print violations, and exit with code 1 on errors
- Support custom rule discovery from a configured `custom.path` directory
- Implement `--format` flag supporting `text` (default, human-readable) and `json`

## Impact

- Affected specs: `cli-and-config` (new)
- Affected code: `terrifying/cli.py`, `terrifying/core/config.py`
- Depends on: `add-core-model`, `add-structural-rules`, `add-best-practice-rules`, `add-opa-integration`, `add-c7n-integration`
