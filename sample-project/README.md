# terrifying sample project

Demonstrates terrifying against a small Terraform codebase. Run `make test` and see architecture violations reported as pytest failures.

## Quickstart

```bash
make test
```

That's it. `uv sync` installs terrifying from the parent directory, then `pytest` picks up `terrifying.yml` automatically and runs all checks.

## Structure

```
sample-project/
├── terrifying.yml          # rule and policy configuration
├── terraform/              # Terraform code under test (intentional violations)
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── policies/
│   ├── opa/                # Rego policies  (requires opa on PATH)
│   │   └── require_tags.rego
│   └── c7n/                # Cloud Custodian policies (requires c7n-left on PATH)
│       └── require_tags.yml
└── custom_rules/
    └── no_count.py         # Example custom rule
```

## Expected output

The sample Terraform intentionally violates several rules — this is what terrifying catching real problems looks like:

```
terrifying::max_resources_per_file      PASSED
terrifying::max_lines_per_file          PASSED
terrifying::resource_file_naming        PASSED
terrifying::no_hardcoded_values         FAILED
  terraform/main.tf [no_hardcoded_values] Resource aws_s3_bucket.data attribute 'bucket' has a hardcoded value
terrifying::variables_have_descriptions FAILED
  terraform/variables.tf [variables_have_descriptions] Variable 'instance_type' is missing a description
terrifying::outputs_have_descriptions   FAILED
  terraform/outputs.tf [outputs_have_descriptions] Output 'bucket_name' is missing a description
terrifying::required_tags               FAILED
  terraform/main.tf [required_tags] Resource aws_s3_bucket.data is missing required tag 'Team'
terrifying::opa                         FAILED  (if opa installed)
terrifying::c7n                         FAILED  (if c7n-left installed)
```

## Make targets

| Target | What it does |
|--------|-------------|
| `make install` | Install terrifying from parent directory via uv |
| `make test` | Run all architecture checks via pytest |
| `make check-json` | Run CLI checks, JSON output |

## terrifying.yml

The configuration enables all built-in rules, a custom rule directory, and both policy engines:

```yaml
terraform:
  path: ./terraform

rules:
  max_resources_per_file:
    max_resources: 5
  max_lines_per_file:
    max_lines: 50
  resource_file_naming:
    pattern: "^[a-z_]+\\.tf$"
  no_hardcoded_values:
    allowed_attributes: [ami, __is_block__]
  variables_have_descriptions: {}
  outputs_have_descriptions: {}
  required_tags:
    tags: [Environment, Team]

custom:
  path: ./custom_rules

policies:
  opa: ./policies/opa
  c7n: ./policies/c7n
```

## Optional dependencies

- **OPA** — `brew install opa` or download from openpolicyagent.org
- **c7n-left** — `pip install c7n-left`

If either binary is absent, terrifying reports an `opa_unavailable` / `c7n_unavailable` failure rather than crashing.
