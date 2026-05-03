## 1. c7n Adapter (`terrifying/policies/c7n.py`)

- [ ] 1.1 Implement `C7nAdapter(policy_dir: Path)`
- [ ] 1.2 Implement YAML policy file discovery via `policy_dir.glob("*.yml")`
- [ ] 1.3 Implement `C7nAdapter.run(tf_dir: Path) -> list[Violation]`
- [ ] 1.4 Invoke `c7n-left run --policy <policy_dir> --directory <tf_dir> --output json` as a subprocess
- [ ] 1.5 Parse JSON output: map each match to `Violation(rule=f"c7n:{policy_name}", file=..., line=..., message=...)`
- [ ] 1.6 Populate `file` from `resource.filename` when present; `line` from `resource.line_start` when present
- [ ] 1.7 On `FileNotFoundError` from subprocess return `[Violation(rule="c7n_unavailable", severity="error", ...)]`
- [ ] 1.8 Empty policy directory → return `[]` without invoking subprocess
- [ ] 1.9 Verify `c7n.py` does not exceed 500 lines

## 2. Tests (`tests/policies/test_c7n.py`)

- [ ] 2.1 Test empty policy dir → empty list, no subprocess call (mock subprocess)
- [ ] 2.2 Test c7n JSON output with one match → one `Violation` with correct `rule`, `message`
- [ ] 2.3 Test c7n JSON output with `filename` and `line_start` present → `file` and `line` populated
- [ ] 2.4 Test c7n JSON output with `filename` absent → `file` is `None` (no crash)
- [ ] 2.5 Test c7n JSON output with `line_start` absent → `line` is `None` (no crash)
- [ ] 2.6 Test c7n JSON output with multiple matches → one `Violation` per match
- [ ] 2.7 Test c7n JSON output with no matches → empty list
- [ ] 2.8 Test `c7n-left` binary not on PATH (`FileNotFoundError`) → `c7n_unavailable` violation returned
- [ ] 2.9 Test `rule` field is `"c7n:<policy_name>"`
- [ ] 2.10 Test subprocess called with correct arguments (mock subprocess, assert call args)
- [ ] 2.11 Integration test (skipped if `c7n-left` not installed): real YAML policy against fixture Terraform directory

## 3. Coverage Gate

- [ ] 3.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
