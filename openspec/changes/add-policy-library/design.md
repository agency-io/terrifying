## Context

spire-controls-staging contains 208 OPA/Rego policies written against Steampipe live-resource row schemas and 194 c7n policies written for CloudTrail event-driven Lambda mode. Neither format is directly consumable by terrifying:

- Rego policies use per-row Steampipe input (`input.db_instance_identifier`, `input.storage_encrypted`) and `violation` rule. terrifying expects `input.resources[_].attributes` and `deny`.
- c7n policies use `resource: aws.*` (runtime resource type), `mode: type: cloudtrail`, event triggers, and SQS `notify` actions. terrifying's c7n integration uses `c7n-left` which expects `resource: terraform.*`, no `mode` block, and attribute-based filters only.

~16 of the 208 Rego policies check live runtime state (instance stopped state, key rotation age, EIP association, last-accessed timestamps). These are excluded from both engines.

## Goals / Non-Goals

- Goals:
  - Bundle ~190 rewritten shift-left Rego policies and ~180 c7n-left policies inside the terrifying package
  - TUI lets users choose engine (Rego, c7n, or both) then browse and select policies by tag
  - Detect configurable params and inject them into the correct section of terrifying.yml
  - Keep the source repo (spire-controls-staging) unmodified

- Non-Goals:
  - Auto-updating bundled policies when spire-controls-staging changes (manual re-sync for now)
  - Executing or validating policies at TUI time (add only; validation happens on next `pytest` run)
  - Generating c7n-left policies for controls that have no Terraform-attribute equivalent (e.g. tag-based controls requiring live resource scan)

## Decisions

### Rego rewrite schema

**Decision**: Rewrite each Rego policy to use `input.resources[_]` with the TerraformContext schema.

The TerraformContext input document passed to OPA:

```json
{
  "resources": [
    {
      "type": "aws_db_instance",
      "name": "primary",
      "file": "infra/main.tf",
      "attributes": { "storage_encrypted": true }
    }
  ],
  "params": { ... }
}
```

Before (Steampipe):
```rego
violation contains msg if {
    input.storage_encrypted == false
    msg := sprintf("RDS instance '%v' lacks encryption", [input.db_instance_identifier])
}
```

After (TerraformContext):
```rego
deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.storage_encrypted
    msg := sprintf("Resource %v.%v: storage encryption is disabled", [resource.type, resource.name])
}
```

Rule changes from `violation` to `deny`; package changes from `spire.controls.*` to `terrifying`.

### c7n rewrite schema

**Decision**: Rewrite each c7n policy from CloudTrail event mode to c7n-left IaC-scanning format.

Before (runtime c7n):
```yaml
- name: rds-storage-encrypted
  resource: rds
  mode:
    type: cloudtrail
    role: arn:aws:iam::{account_id}:role/SpireControls
    events:
      - source: rds.amazonaws.com
        event: CreateDBInstance
        ids: "requestParameters.dBInstanceIdentifier"
  filters:
    - StorageEncrypted: false
  actions:
    - type: notify
      to: [spire-findings-queue]
      transport:
        type: sqs
        queue: arn:aws:sqs:{region}:{account_id}:spire-findings
```

After (c7n-left):
```yaml
- name: rds-storage-encrypted
  resource: terraform.aws_db_instance
  filters:
    - storage_encrypted: false
```

Changes: `resource` uses `terraform.*` prefix; `mode` block removed; runtime-specific filters replaced with attribute filters; `actions` removed.

### Package naming (Rego)

**Decision**: All rewritten Rego policies use `package terrifying` so they work with the existing `data.terrifying.deny` evaluation path in terrifying's OPA adapter.

### Manifest format

**Decision**: `manifest.yaml` with one entry per engine variant. A control implemented in both engines has two entries (same `id`, different `engine`).

```yaml
policies:
  - id: rds-storage-encrypted
    engine: rego
    service: rds
    file: rds/rds-storage-encrypted.rego
    description: RDS instances must have storage encryption enabled
    severity: high
    terraform_resources: [aws_db_instance]
    tags: [fsbp, cis-benchmark, pci-dss, control-tower-strongly-recommended, rds, high, rego]
    params: []
  - id: rds-storage-encrypted
    engine: c7n
    service: rds
    file: rds/rds-storage-encrypted.yml
    description: RDS instances must have storage encryption enabled
    severity: high
    terraform_resources: [aws_db_instance]
    tags: [fsbp, cis-benchmark, pci-dss, control-tower-strongly-recommended, rds, high, c7n]
    params: []
```

Engine tags (`rego`, `c7n`) are added automatically so users can filter by engine in the TUI.

### TUI layout and engine selection

The TUI opens with an engine selection step before the policy browser. The user picks `Rego`, `c7n`, or `Both`. The tag browser and policy list are then filtered to the selected engine(s). Policies available in both engines show a badge when `Both` is selected.

```
┌─ terrifying add ──────────────────────────────────────────────┐
│ Engine: ( ) Rego  ( ) c7n  (•) Both                          │
├──────────────────┬────────────────────────────────────────────┤
│ Tags             │ Policies                    [rego] [c7n]  │
│ > fsbp (87)      │ [x] rds-storage-encrypted   [R]   [C]    │
│   cis (64)       │ [ ] s3-bucket-sse-enabled   [R]   [C]    │
│   high (52)      │ [ ] ec2-imdsv2-check        [R]          │
│   rds (21)       │                                           │
│                  │ Description: RDS storage encryption       │
│                  │ Severity: high                            │
│                  │ Resources: aws_db_instance                │
├──────────────────┴────────────────────────────────────────────┤
│ [Tab] Switch engine  [Space] Toggle  [A] All  [Enter] Add    │
└───────────────────────────────────────────────────────────────┘
```

When a policy is selected and available in both engines, the user selects which engine variant to add (or both).

### Param injection — per engine

Rego params → `policies.opa.params` in terrifying.yml
c7n params → `policies.c7n.params` in terrifying.yml

If the same param (e.g. `required_tags`) is used by both a Rego and a c7n policy being added simultaneously, the CLI prompts once and writes to both sections.

### Output directories

- Rego files → `policies.opa.path` from terrifying.yml, default `./policies/opa/`
- c7n files → `policies.c7n.path` from terrifying.yml, default `./policies/c7n/`

### textual optional dependency

`textual>=0.60` is an optional extras group (`terrifying[tui]`). The non-interactive `terrifying add <id>` path works without textual.

## Risks / Trade-offs

- **Rewrite accuracy**: ~190 Rego + ~180 c7n rewrites risk introducing subtle bugs. Each rewritten policy retains a comment block documenting the Terraform resource type(s) and attribute path(s) checked.
- **HCL attribute shape**: python-hcl2 parses nested blocks as lists of dicts. Attribute paths in rewritten policies must match the parsed shape, not the HCL source shape. See reference table below.
- **c7n-left filter coverage**: Not all runtime c7n filters have c7n-left equivalents. Policies using runtime-only filter types (`bucket-encryption`, `shield-enabled`, etc.) will be excluded from the c7n library if no equivalent attribute filter exists.

## Common HCL Attribute Paths (python-hcl2)

| Terraform attribute | Parsed path in `resource.attributes` |
|---|---|
| `storage_encrypted = true` | `attributes["storage_encrypted"] == True` |
| `server_side_encryption_configuration { rule { ... } }` | `attributes["server_side_encryption_configuration"][0]["rule"]` |
| `tags = { Environment = "prod" }` | `attributes["tags"]["Environment"]` |
| `logging { target_bucket = "..." }` | `attributes["logging"][0]["target_bucket"]` |
| `vpc_config { subnet_ids = [...] }` | `attributes["vpc_config"][0]["subnet_ids"]` |
| `multi_az = true` | `attributes["multi_az"] == True` |
| `publicly_accessible = false` | `attributes["publicly_accessible"] == False` |
