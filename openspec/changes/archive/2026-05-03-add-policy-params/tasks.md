## 1. Dependencies

- [ ] 1.1 Add `jinja2>=3` to `[project]` dependencies in `pyproject.toml`
- [ ] 1.2 Run `uv sync` to confirm resolution

## 2. Config (`terrifying/core/config.py`)

- [ ] 2.1 Add `PolicyConfig` dataclass: `path: Path`, `params: dict`, `policies: dict[str, dict]`
- [ ] 2.2 Replace `opa_policy_dir: Path | None` on `Config` with `opa: PolicyConfig | None`
- [ ] 2.3 Replace `c7n_policy_dir: Path | None` on `Config` with `c7n: PolicyConfig | None`
- [ ] 2.4 Update `ConfigLoader.load()` to parse the new nested structure for both `opa` and `c7n`
- [ ] 2.5 Implement `PolicyConfig.merged_params(policy_name: str) -> dict` — returns `{**self.params, **self.policies.get(policy_name, {}).get("params", {})}`
- [ ] 2.6 Maintain backward compatibility: if `policies.opa` is a plain string path (old format), treat it as `PolicyConfig(path=Path(value), params={}, policies={})`
- [ ] 2.7 Update `ConfigLoader.build_rules()` and `cli.py` references from `config.opa_policy_dir` / `config.c7n_policy_dir` to `config.opa.path` / `config.c7n.path`

## 3. OPA Adapter (`terrifying/policies/opa.py`)

- [ ] 3.1 Update `OpaAdapter.__init__` to accept `policy_config: PolicyConfig` instead of `policy_dir: Path`
- [ ] 3.2 In `_run_policy()`, compute merged params: `policy_config.merged_params(policy.stem)`
- [ ] 3.3 Inject merged params into input document: `{"files": ..., "resources": ..., "params": merged_params}`
- [ ] 3.4 Maintain backward compatibility: `OpaAdapter` still works if constructed with a plain `Path` (no params)

## 4. c7n Adapter (`terrifying/policies/c7n.py`)

- [ ] 4.1 Update `C7nAdapter.__init__` to accept `policy_config: PolicyConfig` instead of `policy_dir: Path`
- [ ] 4.2 Discover policy files via `policy_config.path.glob("*.yml")` and `policy_config.path.glob("*.yml.j2")`
- [ ] 4.3 Implement `_render_policy(policy_file: Path, params: dict) -> str` using `jinja2.Environment` to render the template with merged params
- [ ] 4.4 Write rendered YAML to a `tempfile.NamedTemporaryFile` and pass that path to `c7n-left`
- [ ] 4.5 Clean up temp files after `c7n-left` returns
- [ ] 4.6 Non-template `.yml` files (no Jinja2 syntax) render cleanly with no params — no special handling needed
- [ ] 4.7 Maintain backward compatibility: `C7nAdapter` still works if constructed with a plain `Path`

## 5. pytest plugin (`terrifying/pytest_plugin.py`)

- [ ] 5.1 Update `TerraformCheckCollector.collect()` to pass `config.opa` / `config.c7n` (new `PolicyConfig`) to adapters

## 6. Tests — one per file

### `tests/core/config/policy_config/`
- [ ] 6.1 `test_merged_params_global_only.py` — no policy override → global params returned
- [ ] 6.2 `test_merged_params_policy_override.py` — policy-level param overrides global
- [ ] 6.3 `test_merged_params_merge.py` — policy-level params merged with globals (non-overlapping keys both present)
- [ ] 6.4 `test_backward_compat_plain_path.py` — plain string `policies.opa` value → `PolicyConfig` with empty params
- [ ] 6.5 `test_opa_section_parsed.py` — nested opa section parsed into `PolicyConfig`
- [ ] 6.6 `test_c7n_section_parsed.py` — nested c7n section parsed into `PolicyConfig`

### `tests/policies/opa/`
- [ ] 6.7 `test_params_injected_into_input.py` — global params appear in subprocess input JSON
- [ ] 6.8 `test_policy_params_override_global.py` — per-policy params override global in input JSON
- [ ] 6.9 `test_no_params_empty_dict.py` — no params configured → `input.params` is `{}`

### `tests/policies/c7n/`
- [ ] 6.10 `test_template_rendered_with_params.py` — Jinja2 template rendered with global params before c7n-left invocation
- [ ] 6.11 `test_policy_params_override_in_template.py` — per-policy params override global in rendered template
- [ ] 6.12 `test_plain_yml_no_params.py` — plain YAML (no Jinja2 syntax) passes through unchanged
- [ ] 6.13 `test_temp_file_cleaned_up.py` — temp file removed after c7n-left returns
- [ ] 6.14 `test_j2_extension_discovered.py` — `.yml.j2` files discovered alongside `.yml`

## 7. Update sample project

- [ ] 7.1 Update `sample-project/terrifying.yml` to use new nested `policies.opa` and `policies.c7n` format with params
- [ ] 7.2 Update `sample-project/policies/opa/require_tags.rego` to read tags from `input.params.required_tags`
- [ ] 7.3 Update `sample-project/policies/c7n/require_tags.yml` to use Jinja2 template syntax

## 8. Coverage Gate

- [ ] 8.1 Run `pytest --cov=terrifying --cov-branch --cov-fail-under=95` and confirm it passes
