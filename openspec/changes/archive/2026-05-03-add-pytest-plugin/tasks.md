## 1. Plugin (`terrifying/pytest_plugin.py`)

- [ ] 1.1 Implement `TerraformCheckItem(pytest.Item)` — represents a single rule or adapter check
- [ ] 1.2 `TerraformCheckItem.runtest()` runs the rule/adapter and raises `pytest.fail` with formatted violations if any error-severity violations are found
- [ ] 1.3 `TerraformCheckItem.repr_failure()` formats violations as `file:line [rule] message`
- [ ] 1.4 Implement `TerraformCheckCollector(pytest.Collector)` — collects items from config
- [ ] 1.5 `TerraformCheckCollector.collect()` loads `terrifying.yml`, builds rules via `ConfigLoader`, yields one `TerraformCheckItem` per rule and per configured policy adapter
- [ ] 1.6 Implement `pytest_collect_file` hook — returns a `TerraformCheckCollector` when `terrifying.yml` is encountered in the rootdir
- [ ] 1.7 If `terrifying.yml` is absent, plugin is a no-op
- [ ] 1.8 Terraform directory defaults to the directory containing `terrifying.yml`; overridable via `terraform.path` key in config
- [ ] 1.9 Parse violations from `context.parse_violations` are reported as a single item named `terrifying::parse_errors`
- [ ] 1.10 Verify `pytest_plugin.py` does not exceed 500 lines

## 2. Registration

- [ ] 2.1 Register plugin via `[project.entry-points."pytest11"]` in `pyproject.toml`: `terrifying = "terrifying.pytest_plugin"`
- [ ] 2.2 Run `uv sync` to confirm entry point is picked up

## 3. Config schema update

- [ ] 3.1 Add optional `terraform.path` key to `terrifying.yml` schema in `ConfigLoader`
- [ ] 3.2 `Config` dataclass gains `terraform_path: Path | None = None`
- [ ] 3.3 `ConfigLoader.load()` populates `terraform_path` from `terraform.path` if present

## 4. Tests (`tests/test_pytest_plugin.py`)

- [ ] 4.1 Plugin collects one item per enabled rule
- [ ] 4.2 Rule with no violations → item passes
- [ ] 4.3 Rule with violations → item fails with formatted message
- [ ] 4.4 Warning-severity violations → item passes (warnings printed, not failures)
- [ ] 4.5 No `terrifying.yml` → no items collected (plugin is no-op)
- [ ] 4.6 `terrifying.yml` with `terraform.path` → correct directory parsed
- [ ] 4.7 Parse errors → `parse_errors` item collected and fails
- [ ] 4.8 OPA adapter configured → one item collected for OPA
- [ ] 4.9 c7n adapter configured → one item collected for c7n
- [ ] 4.10 Item name format: `terrifying::<rule_id>`

Use `pytester` (pytest's built-in plugin testing fixture) to run end-to-end plugin tests.

## 5. Update sample project

- [ ] 5.1 Add `pytest` to `[dependency-groups] dev` in `sample-project/pyproject.toml`
- [ ] 5.2 Add `terraform.path` to `sample-project/terrifying.yml`
- [ ] 5.3 Update `sample-project/Makefile` — `make test` runs `uv run pytest`
- [ ] 5.4 Remove `check-rules` target (superseded by pytest)

## 6. Coverage Gate

- [ ] 6.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
