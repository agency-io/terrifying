## 1. Dependencies

- [ ] 1.1 Add `textual>=0.60` to `[project.optional-dependencies] tui` in `pyproject.toml`
- [ ] 1.2 Add `ruamel.yaml>=0.18` to `[project]` dependencies (YAML round-trip editing preserving comments)
- [ ] 1.3 Run `uv sync --all-extras` to confirm resolution

## 2. Policy library — classification and rewrite

- [ ] 2.1 For each of the 208 source policies in `spire-controls-staging/rego/policies/`, classify as SHIFT-LEFT or RUNTIME-ONLY based on whether the check can be performed against Terraform source attributes
- [ ] 2.2 Create `terrifying/policies/library/<service>/` directories for each service
- [ ] 2.3 For each SHIFT-LEFT policy, write a rewritten `.rego` file that:
  - Uses `package terrifying`
  - Iterates `input.resources[_]`, filters by `resource.type`
  - Checks `resource.attributes.*` using the python-hcl2 parsed attribute paths
  - Populates `deny` set with violation messages
  - Retains METADATA comment block (title, description, severity, tags) from the source
- [ ] 2.4 Excluded (RUNTIME-ONLY) policies: `ec2-stopped-instance`, `ec2-volume-inuse-check`, `eip-attached`, `ebs-snapshot-public-restorable-check`, `dynamodb-in-backup-plan`, `efs-in-backup-plan`, `vpc-network-acl-unused-check`, `access-keys-rotated`, `iam-user-mfa-enabled`, `iam-user-unused-credentials-check`, `mfa-enabled-for-iam-console-access`, `kms-cmk-not-scheduled-for-deletion-2`, `secretsmanager-scheduled-rotation-success-check`, `secretsmanager-secret-periodic-rotation`, `secretsmanager-secret-unused`, `cloudwatch-alarm-action-enabled-check`

## 3. Manifest (`terrifying/policies/library/manifest.yaml`)

- [ ] 3.1 Write `manifest.yaml` with one entry per bundled policy containing: `id`, `service`, `file`, `description`, `severity`, `terraform_resources`, `tags`, `params`
- [ ] 3.2 Derive tags from source policy METADATA blocks; normalize to kebab-case; add service tag from directory name and severity tag from metadata
- [ ] 3.3 For policies using `input.params.*`, add param descriptors with `name`, `type`, `description`, `default`

## 4. Manifest loader (`terrifying/policies/library/__init__.py`)

- [ ] 4.1 Implement `load_manifest() -> list[PolicyEntry]` — loads `manifest.yaml` bundled via `importlib.resources`
- [ ] 4.2 Implement `PolicyEntry` dataclass: `id`, `service`, `file`, `description`, `severity`, `terraform_resources`, `tags`, `params`
- [ ] 4.3 Implement `get_policy_rego(policy_id: str) -> str` — returns the `.rego` file contents via `importlib.resources`
- [ ] 4.4 Implement `filter_by_tags(entries, tags: list[str]) -> list[PolicyEntry]` — returns entries matching ALL supplied tags

## 5. CLI — `terrifying add` subcommand (`terrifying/cli.py`)

- [ ] 5.1 Add `add` subcommand to the argparse CLI: `terrifying add [policy-id ...]`
- [ ] 5.2 Add `--dry-run` flag: print delta without writing files
- [ ] 5.3 Implement `_resolve_policies(ids: list[str]) -> list[PolicyEntry]` — looks up IDs in manifest, errors on unknown IDs
- [ ] 5.4 Implement `_collect_params(entries: list[PolicyEntry], existing_config: dict) -> dict` — prompts for each unique undeclared param, returns merged param dict
- [ ] 5.5 Implement `_build_delta(entries, params, config_path: Path) -> Delta` — computes list of files to write and YAML diff for terrifying.yml
- [ ] 5.6 Implement `_print_delta(delta: Delta)` — prints file list and terrifying.yml unified diff to stdout
- [ ] 5.7 Implement `_apply_delta(delta: Delta)` — writes `.rego` files (skip + warn on existing), updates terrifying.yml via ruamel.yaml
- [ ] 5.8 Non-interactive path: resolve → collect params → build delta → print delta → prompt confirm → apply

## 6. TUI (`terrifying/tui.py`)

- [ ] 6.1 Implement `PolicyBrowserApp(textual.App)` with three panels: tag list, policy list, detail pane
- [ ] 6.2 Tag list: shows all unique tags with policy counts; clicking or arrowing to a tag filters policy list
- [ ] 6.3 Policy list: checkbox list of policies matching current tag filter; Space toggles, A selects all visible
- [ ] 6.4 Detail pane: shows description, severity, terraform_resources, tags for the highlighted policy
- [ ] 6.5 Footer bar shows keybindings: `[Space] Toggle  [A] Select all  [Enter] Add  [Q] Quit`
- [ ] 6.6 On Enter: return selected `list[PolicyEntry]` to caller and exit
- [ ] 6.7 Lazy import `textual` — if not installed, `terrifying add` (no args) prints install hint and exits 1

## 7. Tests

### `tests/policies/library/`
- [ ] 7.1 `test_manifest_loads.py` — `load_manifest()` returns non-empty list of `PolicyEntry`
- [ ] 7.2 `test_manifest_entries_valid.py` — every entry has required fields non-empty, file exists in library
- [ ] 7.3 `test_filter_by_tags.py` — filter returns only entries carrying all supplied tags
- [ ] 7.4 `test_get_policy_rego.py` — returns non-empty string for known policy ID; raises for unknown ID
- [ ] 7.5 `test_no_runtime_only_policies.py` — excluded policy IDs not present in manifest

### `tests/cli/add/`
- [ ] 7.6 `test_add_noninteractive_writes_files.py` — policy ID arg → `.rego` written to configured path
- [ ] 7.7 `test_add_unknown_id_exits_1.py` — unknown policy ID → exit code 1
- [ ] 7.8 `test_add_dry_run_no_files_written.py` — `--dry-run` → no files created, delta printed
- [ ] 7.9 `test_add_skips_existing_file.py` — existing `.rego` → warning printed, file not overwritten
- [ ] 7.10 `test_add_injects_params_into_yml.py` — policy with params → `policies.opa.params` updated
- [ ] 7.11 `test_add_preserves_existing_param.py` — param already in yml → not overwritten
- [ ] 7.12 `test_add_creates_opa_section_when_missing.py` — no `policies.opa` in yml → section created with default path
- [ ] 7.13 `test_add_default_output_path.py` — unconfigured yml → files written to `./policies/opa/`
- [ ] 7.14 `test_textual_missing_exits_1.py` — textual not installed + no args → exit 1 with install hint

## 8. Coverage gate

- [ ] 8.1 Run `uv run pytest --cov=terrifying --cov-branch --cov-fail-under=95` and confirm it passes
