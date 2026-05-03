# terrifying

Architecture testing framework for Terraform. Write rules in Python that verify your Terraform code follows structural conventions, best practices, and organisational policies — the equivalent of ArchUnit or Checkstyle but for infrastructure code.

## Why

Existing tools like tflint, checkov, and terrascan are opinionated security scanners. terrifying is a general-purpose framework for writing your own architecture rules: enforce file size limits, resource count limits, parameterisation patterns, required tags, naming conventions, and anything else your team cares about. OPA and c7n_left policy engines are also supported as first-class integrations.

## Installation

```bash
pip install terrifying
```

## Writing a rule

Rules are plain Python classes. The rule ID is derived automatically from the class name.

```python
from terrifying.core import Rule, Violation, TerraformContext

class MaxResourcesPerFile(Rule):
    def __init__(self, max_resources: int = 10):
        self.max_resources = max_resources

    def check(self, context: TerraformContext) -> list[Violation]:
        violations = []
        for tf_file in context.files:
            count = len(tf_file.resources)
            if count > self.max_resources:
                violations.append(Violation(
                    rule=self.rule_id,
                    file=tf_file.path,
                    message=f"{count} resources exceeds max of {self.max_resources}",
                ))
        return violations
```

`MaxResourcesPerFile` → `rule_id = "max_resources_per_file"`

## Running rules

```python
from pathlib import Path
from terrifying.core import Parser, Runner

context = Parser().parse_directory(Path("./infra"))
violations = Runner().run([MaxResourcesPerFile(max_resources=8)], context)

for v in violations:
    print(f"{v.file}: [{v.rule}] {v.message}")
```

## Context model

Rules receive a `TerraformContext` containing all parsed `.tf` files:

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

Files that cannot be parsed produce a `Violation` with `rule="parse_error"` on `context.parse_violations`. Parsing continues for all other files.

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
