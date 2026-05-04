"""Claude Code skill document for terrifying-powered projects."""

CLAUDE_CODE_SKILL = """\
# terrifying

You are working in a project that uses **terrifying** — an architecture testing framework for Terraform.

## What terrifying does

terrifying runs policy checks against Terraform source code (parsed by python-hcl2). Policies are written in Rego (OPA) or Cloud Custodian (c7n-left) and executed before `terraform plan`.

## Project layout

```
terrifying.yml          # Engine config and policy parameters
policies/
  opa/                  # Rego policies (default path)
  c7n/                  # c7n-left YAML policies (default path)
```

## terrifying.yml format

```yaml
policies:
  opa:
    path: ./policies/opa
    params:
      min_password_length: 14
  c7n:
    path: ./policies/c7n
```

## Writing a Rego policy

Policies use `package terrifying` and populate the `deny` set.
Input is `{"resources": [{"type": "...", "name": "...", "attributes": {...}}]}`.

```rego
# METADATA
# title: S3 bucket versioning must be enabled
# severity: High
package terrifying

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_s3_bucket_versioning"
    not versioning_enabled(resource.attributes)
    msg := sprintf("Resource %v.%v: versioning must be enabled", [resource.type, resource.name])
}

versioning_enabled(attrs) if {
    attrs.versioning_configuration[_].status == "Enabled"
}
```

Key rules:
- Always use a helper function with `not foo(attrs)` — never `not X[_].field` (unsafe in Rego v1)
- Filter on `resource.type` matching the Terraform resource type (e.g. `aws_s3_bucket`)
- Access parsed HCL attributes via `resource.attributes.*`

## Writing a c7n policy

```yaml
policies:
  - name: rds-storage-encrypted
    description: RDS instances must have storage encryption enabled
    resource: terraform.aws_db_instance
    filters:
      - storage_encrypted: false
```

## Adding bundled policies

```bash
terrifying add                          # TUI browser (requires pip install terrifying[tui])
terrifying add rds-storage-encrypted    # Add specific policy
terrifying add --engine rego            # Rego only
terrifying add --dry-run                # Preview changes
terrifying list                         # Browse available policies
terrifying list --tag s3 --engine rego  # Filter by tag and engine
```

## Running checks

```bash
terrifying check ./terraform            # Text output
terrifying check ./terraform --format json
uv run pytest                           # Run as pytest tests (via pytest11 plugin)
```

## pytest plugin

The `terrifying` pytest11 plugin auto-discovers policies from `terrifying.yml` and runs them as individual test cases. No extra config needed — just run `pytest`.

## Common patterns

**Check a nested attribute exists and has a value:**
```rego
has_encryption(attrs) if {
    attrs.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default[_].sse_algorithm == "aws:kms"
}
```

**Check a boolean flag:**
```rego
deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_db_instance"
    resource.attributes.storage_encrypted == false
    msg := sprintf("Resource %v.%v: storage must be encrypted", [resource.type, resource.name])
}
```

**Use a param:**
```rego
deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_iam_account_password_policy"
    resource.attributes.minimum_password_length < data.params.min_password_length
    msg := sprintf("Password length must be at least %v", [data.params.min_password_length])
}
```
"""

ISSUES_URL = "https://github.com/agency-io/terrifying/issues"
