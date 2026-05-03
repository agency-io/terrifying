## 1. Context Serialisation (`terrifying/core/context.py`)

- [ ] 1.1 Implement `TerraformContext.to_json() -> dict` — produces `{"files": [...], "resources": [...]}`
- [ ] 1.2 Each resource in JSON includes `type`, `name`, `attributes`, `file` (as string), `line`
- [ ] 1.3 Each file in JSON includes `path`, `line_count`, `resources`, `variables`, `outputs`

## 2. OPA Adapter (`terrifying/policies/opa.py`)

- [ ] 2.1 Implement `OpaAdapter(policy_dir: Path)`
- [ ] 2.2 Implement `.rego` file discovery via `policy_dir.glob("*.rego")`
- [ ] 2.3 Implement `OpaAdapter.run(context: TerraformContext) -> list[Violation]`
- [ ] 2.4 For each `.rego` file invoke `opa eval --stdin-input --data <policy> --format json 'data.terrifying.deny'`
- [ ] 2.5 Parse `deny` set from OPA JSON output — support plain string elements and `{"msg": ..., "file": ...}` objects
- [ ] 2.6 Map each denial to `Violation(rule=f"opa:{policy_stem}", ...)`
- [ ] 2.7 On `FileNotFoundError` from subprocess (opa not on PATH) return `[Violation(rule="opa_unavailable", ...)]`
- [ ] 2.8 Empty policy directory → return `[]` without invoking subprocess
- [ ] 2.9 Verify `opa.py` does not exceed 500 lines

## 3. Tests (`tests/policies/test_opa.py`)

- [ ] 3.1 Test `TerraformContext.to_json()`: all resource fields present and correctly typed
- [ ] 3.2 Test `TerraformContext.to_json()`: multiple files → all appear in `files` list
- [ ] 3.3 Test adapter with empty policy dir → empty list, no subprocess call (mock subprocess)
- [ ] 3.4 Test adapter: OPA returns plain string denial → `Violation` with correct `rule` and `message`
- [ ] 3.5 Test adapter: OPA returns structured `{"msg": ..., "file": ...}` denial → `file` field populated on `Violation`
- [ ] 3.6 Test adapter: OPA returns empty deny set → no violations
- [ ] 3.7 Test adapter: OPA returns multiple denials → one `Violation` per denial
- [ ] 3.8 Test adapter: multiple `.rego` files → each invoked, violations from all collected
- [ ] 3.9 Test adapter: OPA binary not on PATH (`FileNotFoundError`) → `opa_unavailable` violation returned
- [ ] 3.10 Test `rule` field on violation is `"opa:<filename_stem>"`
- [ ] 3.11 Integration test (skipped if `opa` not installed): real `.rego` policy against fixture context

## 4. Coverage Gate

- [ ] 4.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
