# Change: Add pytest Plugin

## Why

Users should be able to run architecture checks by typing `pytest` — no test files to write, no CLI to invoke separately. The plugin integrates terrifying into the standard pytest workflow so architecture violations appear alongside unit test failures in the same report.

## What Changes

- Implement a pytest plugin (`terrifying/pytest_plugin.py`) registered via `entry_points` in `pyproject.toml`
- The plugin reads `terrifying.yml` from the rootdir (the directory pytest is invoked from)
- It generates one `pytest.Item` per enabled rule and one per policy adapter (OPA, c7n)
- Each item has a name derived from the rule ID (e.g. `terrifying::max_resources_per_file`)
- Items fail with a formatted violation list if any violations are found
- Items pass silently if no violations are found
- If no `terrifying.yml` is present, the plugin is a no-op
- The Terraform directory is configured via `terrifying.yml` (a new required `terraform.path` key) or defaults to the rootdir

## Impact

- Affected specs: `pytest-plugin` (new)
- Affected code: `terrifying/pytest_plugin.py`, `pyproject.toml` (entry point)
- Depends on: `add-core-model`, `add-cli-and-config`
