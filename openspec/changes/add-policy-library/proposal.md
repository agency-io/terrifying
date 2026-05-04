# Change: Add bundled policy library with interactive CLI picker

## Why

terrifying has no built-in policies — users must write every rule from scratch. A curated library of ~190 shift-left-compatible AWS best-practice policies (sourced from spire-controls-staging) in both Rego and c7n-left formats would let teams adopt terrifying with immediate coverage for CIS, FSBP, PCI, NIST, and Control Tower requirements, without writing a single line of policy code.

## What Changes

- **Rego policy library**: ~190 shift-left-compatible Rego policies bundled at `terrifying/policies/library/<service>/<name>.rego`. Rewritten from Steampipe live-resource schema to the terrifying TerraformContext schema (`input.resources[_].attributes`). Uses `package terrifying` and populates `deny`.
- **c7n policy library**: ~180 shift-left-compatible c7n-left policies bundled at `terrifying/policies/library/<service>/<name>.yml`. Rewritten from CloudTrail event-driven runtime mode (with `mode: type: cloudtrail` and SQS actions) to c7n-left IaC-scanning format (`resource: terraform.*`, no `mode` block, attribute-based filters). Runtime-only policies are excluded from both engines.
- **Manifest**: `terrifying/policies/library/manifest.yaml` — machine-readable index with one entry per engine variant. Each entry includes: `id`, `engine` (`rego` | `c7n`), `service`, `file`, `description`, `severity`, `terraform_resources`, `tags`, and `params`.
- **Tag taxonomy**: Policies are tagged by compliance framework (`cis-benchmark`, `fsbp`, `pci-dss`, `nist-800-53`, `control-tower-mandatory`, `control-tower-strongly-recommended`, `control-tower-elective`), AWS service (`s3`, `rds`, `ec2`, …), severity (`high`, `medium`, `low`), and engine (`rego`, `c7n`). Tags come from source METADATA/tags blocks.
- **`terrifying add` CLI command**: interactive TUI (built with `textual`) that lets users browse by tag, filter by engine, multi-select policies, and preview the files that will be written. Writes policy files to the appropriate engine directory and updates `terrifying.yml` with any required params.
- **Param detection and injection**: Policies that require configurable values (e.g. `required_tags`) declare params in the manifest. The CLI prompts for values and injects them into `terrifying.yml` under `policies.opa.params` or `policies.c7n.params` as appropriate.
- **Confirmation delta**: Before writing anything the CLI prints a unified diff of `terrifying.yml` changes and the list of files to be created. The user must confirm before any file is written.
- **Per-policy unit tests**: Every bundled policy (Rego and c7n) SHALL have a dedicated unit test. A shared test-helper module provides fixture builders and assertion utilities so each test file remains under ~30 lines. Rego tests use `opa test` via subprocess; c7n-left tests use a temporary Terraform fixture and `c7n-left` subprocess.

## Impact

- Affected specs: `policy-library` (new), `cli` (modified — new `add` subcommand)
- Affected code: `terrifying/policies/library/`, `terrifying/policies/library/manifest.yaml`, `terrifying/cli.py`, `pyproject.toml`
- New dependencies: `textual>=0.60` (optional, `terrifying[tui]`), `ruamel.yaml>=0.18`
- Source Rego: `spire-controls-staging/rego/policies/` — originals never modified
- Source c7n: `spire-controls-staging/c7n/policies/` — originals never modified
- Runtime-only policies excluded from both engines: `ec2-stopped-instance`, `ec2-volume-inuse-check`, `eip-attached`, `ebs-snapshot-public-restorable-check`, `dynamodb-in-backup-plan`, `efs-in-backup-plan`, `vpc-network-acl-unused-check`, `access-keys-rotated`, `iam-user-mfa-enabled`, `iam-user-unused-credentials-check`, `mfa-enabled-for-iam-console-access`, `kms-cmk-not-scheduled-for-deletion-2`, `secretsmanager-scheduled-rotation-success-check`, `secretsmanager-secret-periodic-rotation`, `secretsmanager-secret-unused`, `cloudwatch-alarm-action-enabled-check`
