# terrifying

Architecture testing framework for Terraform. Write rules in Python that verify your Terraform code follows structural conventions, best practices, and organisational policies — the equivalent of ArchUnit or Checkstyle but for infrastructure code.

## Why

Existing tools like tflint, checkov, and terrascan are opinionated security scanners. terrifying is a general-purpose framework for writing your own architecture rules: enforce file size limits, resource count limits, parameterisation patterns, required tags, naming conventions, and anything else your team cares about. OPA and c7n_left policy engines are also supported as first-class integrations.

## Installation

```bash
pip install terrifying
```

## Quickstart

Create `terrifying.yml` in your project root:

```yaml
terraform:
  path: ./infra

rules:
  max_resources_per_file:
    max_resources: 10
  required_tags:
    tags:
      - Environment
      - Team
  variables_have_descriptions: {}
  outputs_have_descriptions: {}
```

Run `pytest` — terrifying is discovered automatically as a pytest plugin:

```
$ pytest -v
terrifying::max_resources_per_file PASSED
terrifying::required_tags          FAILED
  infra/main.tf [required_tags] Resource aws_s3_bucket.data is missing required tag 'Team'
terrifying::variables_have_descriptions PASSED
terrifying::outputs_have_descriptions   PASSED
```

Each rule becomes a named test item. Violations are shown as test failures. No test files to write.

## Configuration (`terrifying.yml`)

```yaml
# Directory containing .tf files to check (relative to terrifying.yml)
terraform:
  path: ./infra

# Built-in rules — omit a rule to disable it
rules:
  max_resources_per_file:
    max_resources: 10
  max_lines_per_file:
    max_lines: 150
  resource_file_naming:
    pattern: "^[a-z_]+\\.tf$"
  no_hardcoded_values:
    allowed_attributes:
      - ami
  variables_have_descriptions: {}
  outputs_have_descriptions: {}
  required_tags:
    tags:
      - Environment
      - Team

# Custom rules — Python files in this directory are loaded automatically
custom:
  path: ./rules

# Policy engine integrations (binaries must be on PATH)
# Plain path — no parameters
policies:
  opa: ./policies/opa
  c7n: ./policies/c7n

# Or nested format with global and per-policy parameters
policies:
  opa:
    path: ./policies/opa
    params:
      required_tags: [Environment, Team]    # available as input.params in Rego
    policies:
      require_encryption:
        params:
          algorithm: AES256                 # overrides global for this policy only
  c7n:
    path: ./policies/c7n
    params:
      required_tags: [Environment, Team]    # injected as Jinja2 variables
    policies:
      require-retention:
        params:
          min_retention_days: 90
```

## Built-in rules

| Rule | Default | What it checks |
|------|---------|----------------|
| `max_resources_per_file` | 10 | Resources per `.tf` file |
| `max_lines_per_file` | 150 | Lines per `.tf` file |
| `resource_file_naming` | — | File name matches a regex pattern |
| `no_hardcoded_values` | — | Attribute values are references, not literals |
| `variables_have_descriptions` | — | All variables have a `description` |
| `outputs_have_descriptions` | — | All outputs have a `description` |
| `required_tags` | — | All resources carry required tag keys |

## Writing a custom rule

Rules are plain Python classes. The rule ID is derived automatically from the class name.

```python
# rules/no_count.py
from terrifying.core import Rule, Violation, TerraformContext

class NoCount(Rule):
    """Flags resources using count; prefer for_each."""

    def check(self, context: TerraformContext) -> list[Violation]:
        violations = []
        for resource in context.resources:
            if "count" in resource.attributes:
                violations.append(Violation(
                    rule=self.rule_id,
                    file=resource.file,
                    message=f"{resource.type}.{resource.name} uses count; prefer for_each",
                ))
        return violations
```

`NoCount` → `rule_id = "no_count"` — shown as `terrifying::no_count` in pytest output.

## OPA integration

Place `.rego` files in the directory configured under `policies.opa`. Policies use `data.terrifying.deny` and receive the Terraform context plus any configured params as `input.params`:

```rego
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    tag := input.params.required_tags[_]
    not resource.attributes.tags[tag]
    msg := sprintf("Resource %v.%v is missing required tag '%v'", [resource.type, resource.name, tag])
}
```

Parameters are set in `terrifying.yml` and merged per-policy — global params apply to all policies, per-policy params override them for a specific policy.

Requires `opa` on PATH. If absent, a single `opa_unavailable` test item is reported.

## c7n integration

Place c7n YAML files in the directory configured under `policies.c7n`. Files are treated as Jinja2 templates — configured params are available as template variables:

```yaml
policies:
{% for tag in required_tags %}
  - name: require-{{ tag | lower }}-tag
    resource: terraform.aws_s3_bucket
    filters:
      - "tag:{{ tag }}": absent
{% endfor %}
```

Files with no Jinja2 syntax pass through unchanged. Rendered YAML is passed to `c7n-left` via a temporary file — the original is never modified.

Requires `c7n-left` on PATH (`pip install c7n-left`). If absent, a `c7n_unavailable` test item is reported.

## CLI

For use in scripts or CI pipelines without pytest:

```bash
terrifying check ./infra                # text output, exit 1 on errors
terrifying check ./infra --format json  # JSON array of violations
```

## Context model

Custom rules receive a `TerraformContext`:

| Attribute | Type | Description |
|---|---|---|
| `context.files` | `list[TerraformFile]` | One entry per `.tf` file |
| `context.resources` | `list[Resource]` | All resources across all files |
| `file.path` | `Path` | Absolute path to the file |
| `file.resources` | `list[Resource]` | Resources defined in this file |
| `file.variables` | `list[Variable]` | Variable blocks |
| `file.outputs` | `list[Output]` | Output blocks |
| `file.locals` | `list[Local]` | Local values |
| `file.module_calls` | `list[ModuleCall]` | Module calls |
| `file.line_count` | `int` | Total lines in the file |

## Parse errors

Files that cannot be parsed produce a `terrifying::parse_errors` test item listing the affected files. Parsing continues for all other files.

## Development

```bash
make install   # install dependencies with uv
make fmt       # auto-format with black
make lint      # black --check, ruff, pylint
make test      # pytest with branch coverage (95% minimum)
make ci        # lint + test
```

## Licence

MIT — see [LICENSE](LICENSE).
