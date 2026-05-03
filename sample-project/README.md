# terrifying sample project

Demonstrates terrifying against a small Terraform codebase using built-in rules, OPA policies, c7n policies, and a custom rule.

## Structure

```
sample-project/
├── terrifying.yml          # rule configuration
├── terraform/              # Terraform code under test
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── policies/
│   ├── opa/                # Rego policies (requires opa on PATH)
│   │   └── require_tags.rego
│   └── c7n/                # Cloud Custodian policies (requires c7n-left on PATH)
│       └── require_tags.yml
└── custom_rules/
    └── no_count.py         # Example custom rule
```

## Running

```bash
make install     # install terrifying from the parent directory
make check       # run all checks, text output
make check-json  # run all checks, JSON output
make check-rules # run built-in and custom rules only (no policy engines)
```

## What the sample checks

| Rule | What it catches |
|------|----------------|
| `max_resources_per_file` | Files with more than 5 resources |
| `max_lines_per_file` | Files longer than 50 lines |
| `resource_file_naming` | File names not matching `^[a-z_]+\.tf$` |
| `no_hardcoded_values` | Attribute values that are literals rather than `var.*` / `local.*` references |
| `variables_have_descriptions` | Variables missing a `description` field |
| `outputs_have_descriptions` | Outputs missing a `description` field |
| `required_tags` | Resources missing `Environment` or `Team` tags |
| OPA `require_tags.rego` | Resources missing tags (Rego policy) |
| c7n `require_tags.yml` | S3 buckets missing tags (Cloud Custodian policy) |
| custom `no_count.py` | Resources using `count` instead of `for_each` |

The sample Terraform intentionally contains violations so you can see terrifying in action.

## Optional dependencies

- **OPA** — install from https://www.openpolicyagent.org/docs/latest/#1-download-opa
- **c7n-left** — `pip install c7n-left`

If either binary is absent, terrifying reports an `opa_unavailable` / `c7n_unavailable` violation rather than crashing.
