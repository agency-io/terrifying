## 1. Implementation

- [ ] 1.1 Create `terrifying/rules/structural/` package with `__init__.py`
- [ ] 1.2 Implement `MaxResourcesPerFile(max_resources: int = 10)` in `max_resources_per_file.py` — one class, one file
- [ ] 1.3 Implement `MaxLinesPerFile(max_lines: int = 150)` in `max_lines_per_file.py`
- [ ] 1.4 Implement `ResourceFileNaming(pattern: str)` in `resource_file_naming.py` — compiles regex in `__init__`
- [ ] 1.5 Verify each rule file does not exceed 500 lines (all will be well under; noted for consistency)

## 2. Tests (`tests/rules/structural/`)

- [ ] 2.1 `test_max_resources_per_file.py`:
  - Below limit → no violations
  - Exactly at limit → no violations (boundary)
  - One over limit → one violation naming the file and count
  - Multiple files: one over, one under → only the over-limit file produces a violation
  - Default `max_resources=10` is respected
  - Custom `max_resources` value is respected
  - `rule_id` == `"max_resources_per_file"`

- [ ] 2.2 `test_max_lines_per_file.py`:
  - Below limit → no violations
  - Exactly at limit → no violations (boundary)
  - One over limit → one violation naming the file and line count
  - Multiple files: mixed → only over-limit files produce violations
  - Default `max_lines=150` is respected
  - Custom `max_lines` value is respected
  - `rule_id` == `"max_lines_per_file"`

- [ ] 2.3 `test_resource_file_naming.py`:
  - File name matches pattern → no violation
  - File name does not match pattern → violation naming file and pattern
  - Multiple files: mixed matches → only non-matching produce violations
  - Pattern is a valid regex (e.g. `r"^[a-z_]+\.tf$"`)
  - `rule_id` == `"resource_file_naming"`

## 3. Coverage Gate

- [ ] 3.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
