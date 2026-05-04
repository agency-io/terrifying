# Change: Add bundled policy library with interactive CLI picker

## Why

terrifying has no built-in policies — users must write every rule from scratch. A curated library of ~190 shift-left-compatible AWS best-practice policies (sourced from spire-controls-staging) would let teams adopt terrifying with immediate coverage for CIS, FSBP, PCI, NIST, and Control Tower requirements, without writing a single line of Rego.

## What Changes

- **Policy library**: ~190 shift-left-compatible Rego policies bundled inside the terrifying package under `terrifying/policies/library/<service>/`. Policies are rewritten from the Steampipe live-resource schema to the terrifying TerraformContext schema (`input.resources[_].attributes`). Runtime-only policies (those that check live state such as key rotation age, EIP attachment, or instance stopped state) are excluded.
- **Manifest**: `terrifying/policies/library/manifest.yaml` — machine-readable index of every bundled policy: service, description, severity, tags, Terraform resource types checked, and any configurable params.
- **Tag taxonomy**: Every policy is tagged by compliance framework (`cis-benchmark`, `fsbp`, `pci-dss`, `nist-800-53`, `control-tower`, `control-tower-mandatory`, `control-tower-strongly-recommended`, `control-tower-elective`), by AWS service (`s3`, `rds`, `ec2`, …), and by severity (`high`, `medium`, `low`). Tags come directly from the source policy METADATA blocks.
- **`terrifying add` CLI command**: interactive TUI (built with `textual`) that lets users browse policies by tag, multi-select, preview the files that will be written, and confirm. Writes `.rego` files to the project's OPA policies directory and updates `terrifying.yml` with any required params.
- **Param detection and injection**: Rewritten policies that require configurable values (e.g. `required_tags`, `allowed_ports`, `min_retention_days`) declare params in the manifest. The CLI reads these, prompts the user for values, and injects them into `terrifying.yml` under `policies.opa.params`.
- **Confirmation delta**: Before writing anything the CLI prints a unified diff of the `terrifying.yml` changes and lists the `.rego` files that will be created. The user must confirm before any file is written.

## Impact

- Affected specs: `policy-library` (new), `cli` (modified — new `add` subcommand)
- Affected code: `terrifying/policies/library/`, `terrifying/policies/library/manifest.yaml`, `terrifying/cli.py`, `pyproject.toml` (new `textual` dependency)
- New dependency: `textual>=0.60` for the TUI
- Source policies: `spire-controls-staging/rego/policies/` — originals are never modified; rewritten copies are committed into this repo
- Runtime-only policies excluded (not bundled): `ec2-stopped-instance`, `ec2-volume-inuse-check`, `eip-attached`, `ebs-snapshot-public-restorable-check`, `dynamodb-in-backup-plan`, `efs-in-backup-plan`, `vpc-network-acl-unused-check`, `access-keys-rotated`, `iam-user-mfa-enabled`, `iam-user-unused-credentials-check`, `mfa-enabled-for-iam-console-access`, `kms-cmk-not-scheduled-for-deletion-2`, `secretsmanager-scheduled-rotation-success-check`, `secretsmanager-secret-periodic-rotation`, `secretsmanager-secret-unused`, `cloudwatch-alarm-action-enabled-check`
