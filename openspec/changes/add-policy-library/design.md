## Context

spire-controls-staging contains 208 OPA/Rego policies written against Steampipe live-resource row schemas (`input.db_instance_identifier`, `input.storage_encrypted`, etc.) and 194 c7n policies written for CloudTrail event-driven Lambda mode. Neither format is directly consumable by terrifying. The Rego policies need their input schema rewritten to match TerraformContext (`input.resources[_]`). The c7n policies use runtime event mode and are out of scope for this change (c7n-left has a different resource model and is a separate effort).

~16 of the 208 Rego policies check live runtime state that cannot be inferred from Terraform source (instance stopped state, key rotation age, EIP association, last-accessed timestamps). These are excluded.

## Goals / Non-Goals

- Goals:
  - Bundle ~190 rewritten shift-left Rego policies inside the terrifying package
  - Provide a TUI CLI to let users pick policies by compliance tag and add them to their project
  - Detect configurable params and inject them into terrifying.yml with user confirmation
  - Keep the source repo (spire-controls-staging) unmodified

- Non-Goals:
  - Bundling c7n policies (separate effort; c7n-left resource model differs significantly)
  - Auto-updating bundled policies when spire-controls-staging changes (manual re-sync for now)
  - Executing or testing policies at TUI time (add only; validation happens on next `pytest` run)

## Decisions

### Policy rewrite schema

**Decision**: Rewrite each policy to use `input.resources[_]` with the TerraformContext schema rather than Steampipe row fields.

The TerraformContext input document passed to OPA looks like:

```json
{
  "resources": [
    {
      "type": "aws_s3_bucket",
      "name": "my_bucket",
      "file": "infra/main.tf",
      "attributes": {
        "server_side_encryption_configuration": [...]
      }
    }
  ],
  "params": { ... }
}
```

Rewritten policies iterate `input.resources[_]` and filter by `resource.type`, then check `resource.attributes.*`. Example:

```rego
# Before (Steampipe):
violation contains msg if {
    input.storage_encrypted == false
    msg := sprintf("RDS instance '%v' lacks encryption", [input.db_instance_identifier])
}

# After (TerraformContext):
deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    not resource.attributes.storage_encrypted
    msg := sprintf("Resource %v.%v: storage encryption is disabled", [resource.type, resource.name])
}
```

Note the rule changes from `violation` to `deny` to match the terrifying OPA convention.

### Package naming

**Decision**: Rewritten policies use `package terrifying` (not `package spire.controls.*`) so they work with the existing `data.terrifying.deny` evaluation path in terrifying's OPA adapter.

### Manifest format

**Decision**: `manifest.yaml` in the library root. One entry per policy:

```yaml
policies:
  - id: s3-bucket-server-side-encryption-enabled
    service: s3
    file: s3/s3-bucket-server-side-encryption-enabled.rego
    description: S3 buckets must have default server-side encryption configured
    severity: medium
    terraform_resources: [aws_s3_bucket]
    tags: [fsbp, cis-benchmark, pci-dss, nist-800-53, control-tower-elective, s3, encryption-at-rest]
    params: []
  - id: required-tags
    ...
    params:
      - name: required_tags
        type: list[string]
        description: Tag keys that every resource must carry
        default: [Environment, Team]
```

Tags are normalized to kebab-case. Service tags are added automatically from the directory name.

### TUI library

**Decision**: `textual>=0.60`. It provides a full-screen terminal UI with composable widgets, keyboard navigation, and is well-maintained. `questionary` was considered but only supports linear prompts — not a browsable tree + checkbox list.

### TUI layout

```
┌─ terrifying add ──────────────────────────────────────┐
│ Filter by tag: [___________]                          │
├──────────────────┬────────────────────────────────────┤
│ Tags             │ Policies (12 selected)             │
│ > fsbp (87)      │ [x] s3-bucket-server-side-enc...  │
│   cis (64)       │ [x] rds-storage-encrypted          │
│   pci (41)       │ [ ] ec2-imdsv2-check               │
│   high (52)      │ [ ] eks-endpoint-no-public-access  │
│   s3 (16)        │                                    │
│   rds (21)       │ Description:                       │
│                  │ S3 buckets must have default SSE   │
│                  │ Severity: medium                   │
│                  │ Resources: aws_s3_bucket           │
├──────────────────┴────────────────────────────────────┤
│ [A] Select all visible  [Space] Toggle  [Enter] Add   │
└───────────────────────────────────────────────────────┘
```

On Enter, the TUI exits and the CLI enters the confirmation flow.

### Param injection flow

1. For each selected policy that declares params, collect unique param names.
2. For each param not already present in `terrifying.yml`, prompt the user: `required_tags [default: Environment, Team]:`.
3. Print a unified diff of the terrifying.yml changes + list of `.rego` files to be written.
4. Prompt `Apply? [y/N]`.
5. On confirm: write files, update YAML in-place preserving comments where possible (use ruamel.yaml).

### Output directory

Policies are written to the OPA path configured in `terrifying.yml` (`policies.opa.path`). If not configured, default to `./policies/opa/` and add the section to `terrifying.yml`.

## Risks / Trade-offs

- **Rewrite accuracy**: ~190 manual rewrites risk introducing subtle bugs. Each rewritten policy must include a comment block documenting the Terraform resource type(s) it targets and the attribute path checked, making review practical.
- **HCL attribute shape**: python-hcl2 parses nested blocks as lists of dicts. Attribute paths in rewritten policies must match the parsed shape, not the HCL source shape. A reference mapping of common attribute paths will be maintained in `design.md`.
- **textual dependency**: Adds ~2MB to the installed package. Acceptable given it's a dev/authoring tool, not a CI dependency. `textual` is optional — if not installed the CLI prints an error suggesting `pip install terrifying[tui]`.

## Common HCL Attribute Paths (python-hcl2)

| Terraform attribute | Parsed path in `resource.attributes` |
|---|---|
| `storage_encrypted = true` | `attributes["storage_encrypted"] == True` |
| `server_side_encryption_configuration { rule { ... } }` | `attributes["server_side_encryption_configuration"][0]["rule"]` |
| `tags = { Environment = "prod" }` | `attributes["tags"]["Environment"]` |
| `logging { target_bucket = "..." }` | `attributes["logging"][0]["target_bucket"]` |
| `vpc_config { subnet_ids = [...] }` | `attributes["vpc_config"][0]["subnet_ids"]` |

## Open Questions

- Should policies be organized in subdirectories by service (`s3/`, `rds/`) or flat? — **Decision: subdirectories by service** to mirror the source and make bulk service-level selection natural in the TUI.
- Should `terrifying add` also support adding individual policies by ID non-interactively (e.g. `terrifying add s3-bucket-server-side-encryption-enabled`)? — Yes, support both modes: with no args → TUI; with policy IDs as positional args → non-interactive add.
