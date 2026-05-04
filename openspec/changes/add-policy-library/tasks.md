## 1. Dependencies

- [x] 1.1 Add `textual>=0.60` to `[project.optional-dependencies] tui` in `pyproject.toml`
- [x] 1.2 Add `ruamel.yaml>=0.18` to `[project]` dependencies
- [x] 1.3 Run `uv sync --all-extras` to confirm resolution

## 2. Rego policy library — rewrite

- [x] 2.1 Classify each of the 208 source policies in `spire-controls-staging/rego/policies/` as SHIFT-LEFT or RUNTIME-ONLY
- [x] 2.2 Create `terrifying/policies/library/<service>/` directories for each service
- [x] 2.3 For each SHIFT-LEFT Rego policy, write a rewritten `.rego` file that:
  - Uses `package terrifying`
  - Iterates `input.resources[_]`, filters by `resource.type`
  - Checks `resource.attributes.*` using python-hcl2 parsed attribute paths
  - Populates `deny` set with violation messages
  - Retains title, description, severity, and tags in a comment header
- [x] 2.4 Excluded RUNTIME-ONLY policies (do not bundle): `ec2-stopped-instance`, `ec2-volume-inuse-check`, `eip-attached`, `ebs-snapshot-public-restorable-check`, `dynamodb-in-backup-plan`, `efs-in-backup-plan`, `vpc-network-acl-unused-check`, `access-keys-rotated`, `iam-user-mfa-enabled`, `iam-user-unused-credentials-check`, `mfa-enabled-for-iam-console-access`, `kms-cmk-not-scheduled-for-deletion-2`, `secretsmanager-scheduled-rotation-success-check`, `secretsmanager-secret-periodic-rotation`, `secretsmanager-secret-unused`, `cloudwatch-alarm-action-enabled-check`

## 3. c7n policy library — rewrite

- [x] 3.1 For each source policy in `spire-controls-staging/c7n/policies/`, apply the same SHIFT-LEFT / RUNTIME-ONLY classification as the Rego set
- [x] 3.2 For each SHIFT-LEFT c7n policy, write a rewritten `.yml` file under the same `terrifying/policies/library/<service>/` directory that:
  - Sets `resource: terraform.<resource_type>` (e.g. `terraform.aws_db_instance`)
  - Removes the `mode` block entirely
  - Replaces runtime-specific filters with attribute-based c7n-left filters
  - Removes the `actions` block entirely
  - Retains `name`, `description`, and `tags` fields
- [x] 3.3 Exclude policies where no c7n-left attribute filter equivalent exists for the runtime filter used

## 4. Manifest (`terrifying/policies/library/manifest.yaml`)

- [x] 4.1 Write `manifest.yaml` with one entry per engine variant: `id`, `engine`, `service`, `file`, `description`, `severity`, `terraform_resources`, `tags`, `params`
- [x] 4.2 Derive tags from source metadata; normalize to kebab-case; auto-add service tag, severity tag, and engine tag (`rego` or `c7n`)
- [x] 4.3 For policies using `input.params.*` (Rego) or Jinja2 variables (c7n), add param descriptors with `name`, `type`, `description`, `default`

## 5. Manifest loader (`terrifying/policies/library/__init__.py`)

- [x] 5.1 Implement `PolicyEntry` dataclass: `id`, `engine`, `service`, `file`, `description`, `severity`, `terraform_resources`, `tags`, `params`
- [x] 5.2 Implement `load_manifest() -> list[PolicyEntry]` — loads `manifest.yaml` via `importlib.resources`
- [x] 5.3 Implement `get_policy_source(entry: PolicyEntry) -> str` — returns file contents via `importlib.resources`
- [x] 5.4 Implement `filter_by_tags(entries, tags: list[str]) -> list[PolicyEntry]` — entries matching ALL supplied tags
- [x] 5.5 Implement `filter_by_engine(entries, engine: str) -> list[PolicyEntry]` — `engine` in (`rego`, `c7n`, `both`)

## 6. CLI — `terrifying add` subcommand (`terrifying/cli.py`)

- [x] 6.1 Add `add` subcommand: `terrifying add [policy-id ...] [--engine rego|c7n|both] [--dry-run]`
- [x] 6.2 Implement `_resolve_policies(ids, engine) -> list[PolicyEntry]` — looks up IDs in manifest for the given engine; errors on unknown IDs
- [x] 6.3 Implement `_collect_params(entries, existing_config) -> dict[str, dict]` — returns `{"opa": {...}, "c7n": {...}}`; prompts once for shared param names; skips params already in config
- [x] 6.4 Implement `_build_delta(entries, params, config_path) -> Delta` — computes files to write per engine and unified diff of terrifying.yml
- [x] 6.5 Implement `_print_delta(delta)` — prints file list with `[rego]`/`[c7n]` labels and terrifying.yml diff
- [x] 6.6 Implement `_apply_delta(delta)` — writes files (skip + warn on existing), updates terrifying.yml via ruamel.yaml
- [x] 6.7 Non-interactive path: resolve → collect params → build delta → print delta → prompt confirm → apply

## 7. TUI (`terrifying/tui.py`)

- [x] 7.1 Implement `PolicyBrowserApp(textual.App)` with engine selector, tag browser panel, policy list panel, and detail pane
- [x] 7.2 Engine selector: radio buttons for `Rego`, `c7n`, `Both` — changing selection re-filters the tag browser and policy list
- [x] 7.3 Tag browser: unique tags with policy counts for the selected engine(s); clicking a tag filters the policy list
- [x] 7.4 Policy list: checkbox list; Space toggles, A selects all visible; policies available in both engines show `[R]` and `[C]` badges when `Both` is selected
- [x] 7.5 Detail pane: description, severity, terraform_resources, tags, engine for the highlighted policy
- [x] 7.6 Footer: `[Tab] Engine  [Space] Toggle  [A] All  [Enter] Add  [Q] Quit`
- [x] 7.7 On Enter: return `list[PolicyEntry]` of selected variants to caller
- [x] 7.8 Lazy-import `textual` — if missing, `terrifying add` (no args) prints install hint and exits 1

## 8. Test helpers (`tests/policies/library/helpers.py`)

- [x] 8.1 Implement `rego_input(resources: list[dict], params: dict = {}) -> dict` — builds the OPA input document dict
- [x] 8.2 Implement `eval_rego_policy(policy_path: Path, input_doc: dict) -> list[str]` — runs `opa eval data.terrifying.deny` via subprocess, returns list of deny messages
- [x] 8.3 Implement `resource(type: str, name: str, attributes: dict) -> dict` — builds a single resource dict in TerraformContext format
- [x] 8.4 Implement `c7n_violations(policy_path: Path, tf_fixture: str) -> list[dict]` — writes fixture to temp dir, runs `c7n-left`, returns parsed violations
- [x] 8.5 Implement `tf_resource(type: str, name: str, body: str) -> str` — builds a minimal Terraform HCL resource block string for use as a fixture

## 9. Per-policy tests

### `tests/policies/library/rego/<service>/`
- [x] 9.1 For each bundled Rego policy, create `test_<policy_id>.py` with:
  - One test asserting `eval_rego_policy` returns empty `deny` for a compliant resource fixture
  - One test asserting `eval_rego_policy` returns a non-empty `deny` for a non-compliant resource fixture
  - Each test file SHALL use helpers from `tests/policies/library/helpers.py` and remain under 30 lines

### `tests/policies/library/c7n/<service>/`
- [x] 9.2 For each bundled c7n policy, create `test_<policy_id>.py` with:
  - One test asserting `c7n_violations` returns no violations for a compliant Terraform fixture
  - One test asserting `c7n_violations` returns at least one violation for a non-compliant Terraform fixture
  - Each test file SHALL use helpers from `tests/policies/library/helpers.py` and remain under 30 lines

## 10. Manifest and CLI tests

### `tests/policies/library/`
- [x] 10.1 `test_manifest_loads.py` — `load_manifest()` returns non-empty list
- [x] 10.2 `test_manifest_entries_valid.py` — every entry has required fields; referenced file exists in library
- [x] 10.3 `test_filter_by_tags.py` — returns only entries matching all supplied tags
- [x] 10.4 `test_filter_by_engine.py` — returns only entries for the specified engine
- [x] 10.5 `test_get_policy_source.py` — returns non-empty string for known entry; raises for unknown
- [x] 10.6 `test_no_runtime_only_policies.py` — excluded policy IDs absent from manifest for both engines
- [x] 10.7 `test_rego_policies_use_deny.py` — every bundled `.rego` file contains `deny contains` not `violation`
- [x] 10.8 `test_c7n_policies_no_mode_block.py` — every bundled c7n `.yml` file has no `mode:` key
- [x] 10.9 `test_c7n_policies_terraform_resource.py` — every bundled c7n `.yml` `resource` starts with `terraform.`

### `tests/cli/add/`
- [x] 10.10 `test_add_noninteractive_rego.py` — policy ID + `--engine rego` → `.rego` written to opa path
- [x] 10.11 `test_add_noninteractive_c7n.py` — policy ID + `--engine c7n` → `.yml` written to c7n path
- [x] 10.12 `test_add_both_engines.py` — `--engine both` → both `.rego` and `.yml` written
- [x] 10.13 `test_add_unknown_id_exits_1.py` — unknown policy ID → exit code 1
- [x] 10.14 `test_add_dry_run_no_files_written.py` — `--dry-run` → no files created
- [x] 10.15 `test_add_skips_existing_file.py` — existing file → warning, not overwritten
- [x] 10.16 `test_add_injects_rego_params.py` — Rego policy with params → `policies.opa.params` updated
- [x] 10.17 `test_add_injects_c7n_params.py` — c7n policy with params → `policies.c7n.params` updated
- [x] 10.18 `test_add_shared_param_written_to_both.py` — shared param → written to both opa and c7n sections
- [x] 10.19 `test_add_preserves_existing_param.py` — param already in yml → not overwritten
- [x] 10.20 `test_add_creates_opa_section.py` — no `policies.opa` in yml → section created with default path
- [x] 10.21 `test_add_creates_c7n_section.py` — no `policies.c7n` in yml → section created with default path
- [x] 10.22 `test_textual_missing_exits_1.py` — textual not installed + no args → exit 1 with install hint

## 11. Coverage gate

- [x] 11.1 Run `uv run pytest --cov=terrifying --cov-branch --cov-fail-under=95` and confirm it passes
