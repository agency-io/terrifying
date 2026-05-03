## 1. Configuration (`terrifying/core/config.py`)

- [ ] 1.1 Implement `ConfigLoader.load(path: Path) -> Config` — reads `terrifying.yml` via PyYAML
- [ ] 1.2 `Config` dataclass holds: `rules: dict[str, dict]`, `custom_path: Path | None`, `opa_policy_dir: Path | None`, `c7n_policy_dir: Path | None`
- [ ] 1.3 Implement `ConfigLoader.build_rules(config: Config) -> list[Rule]` — factory mapping rule keys to classes, passing parameters
- [ ] 1.4 Rule keys absent from config are not instantiated (disabled by default)
- [ ] 1.5 Missing `terrifying.yml` → return empty `Config` with no rules enabled (no crash)
- [ ] 1.6 Verify `config.py` does not exceed 500 lines

## 2. Custom Rule Discovery (`terrifying/core/discovery.py`)

- [ ] 2.1 Implement `discover_rules(path: Path) -> list[Rule]` — imports each `.py` file, inspects module attributes, returns instances of `Rule` subclasses (excluding `Rule` itself)
- [ ] 2.2 Non-`Rule` classes are silently ignored
- [ ] 2.3 Import errors log a warning and continue to the next file (do not crash the run)
- [ ] 2.4 Custom rules are instantiated with no constructor arguments
- [ ] 2.5 Verify `discovery.py` does not exceed 500 lines

## 3. CLI (`terrifying/cli.py`)

- [ ] 3.1 Implement `terrifying check <directory>` using `argparse`
- [ ] 3.2 Load config from `terrifying.yml` in current working directory
- [ ] 3.3 Parse Terraform directory via `Parser`
- [ ] 3.4 Assemble rule list from config + custom discovery
- [ ] 3.5 Run OPA adapter if configured
- [ ] 3.6 Run c7n adapter if configured
- [ ] 3.7 Print violations in text format by default: `<file>:<line> [<rule>] <severity>: <message>`
- [ ] 3.8 Print violations as JSON array when `--format json` is passed
- [ ] 3.9 Exit code 0 if no error-severity violations; exit code 1 if any error-severity violation
- [ ] 3.10 Warning-severity violations are printed but do not affect exit code
- [ ] 3.11 Verify `cli.py` does not exceed 500 lines

## 4. Tests (`tests/core/test_config.py`, `tests/core/test_discovery.py`, `tests/test_cli.py`)

- [ ] 4.1 `test_config.py`:
  - Rule key present with params → rule instantiated with correct params
  - Rule key absent → rule not in list
  - `custom.path` configured → `Config.custom_path` set
  - OPA policy dir configured → `Config.opa_policy_dir` set
  - c7n policy dir configured → `Config.c7n_policy_dir` set
  - Missing `terrifying.yml` → empty `Config` returned, no exception

- [ ] 4.2 `test_discovery.py`:
  - Python file with `Rule` subclass → class discovered and instantiated
  - Python file with non-`Rule` class → not returned
  - Python file with both → only `Rule` subclass returned
  - File with import error → warning emitted, discovery continues
  - Empty directory → empty list

- [ ] 4.3 `test_cli.py` (use `subprocess.run` or `click.testing.CliRunner` / `argparse` equivalent):
  - No violations → exit code 0, success message printed
  - Error violation → exit code 1, violation printed in text format
  - Warning-only violation → exit code 0, warning printed
  - `--format json` → stdout is valid JSON array with correct fields
  - Text format output contains file, rule, severity, message
  - Missing Terraform directory → error message, exit code 1

## 5. Coverage Gate

- [ ] 5.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
