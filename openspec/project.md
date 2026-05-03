# terrifying

A Python framework for architecture testing of Terraform code. Teams write rules that verify Terraform follows structural conventions, best practices, and organisational policies — the equivalent of ArchUnit or Checkstyle but for infrastructure code.

## Problem

Existing Terraform linting tools (tflint, checkov, terrascan) are opinionated security scanners. There is no general-purpose framework for writing custom architecture rules against Terraform — verifying conventions like file size, resource count, parameterisation patterns, or team-specific structural decisions.

## Solution

A Python library that provides:
- A parsed Terraform context model (HCL → typed Python objects)
- A simple Rule base class — rule ID derived from class name, never hardcoded
- Built-in rules for common structural and best-practice concerns
- Adapters for OPA and c7n_left that normalise their output into the same Violation model
- A CLI and YAML config for enabling/parameterising rules per project

## Architecture

### Library (`terrifying` package)

- `core/parser.py` — HCL parsing via python-hcl2
- `core/context.py` — TerraformContext, TerraformFile, Resource, Variable, Output models
- `core/rule.py` — Rule base class (rule_id = snake_cased class name), Violation dataclass
- `core/runner.py` — discovers rules, executes them, collects violations
- `core/config.py` — loads terrifying.yml, wires rules to parameters
- `rules/structural/` — built-in file-level rules
- `rules/best_practices/` — built-in content rules
- `policies/opa.py` — OPA adapter
- `policies/c7n.py` — c7n_left adapter
- `cli.py` — CLI entry point (`terrifying check ./infra`)

### Consuming Project

- `terrifying.yml` — which rules, what parameters
- `rules/` — custom Python rule classes implementing the Rule protocol
- `policies/opa/` — .rego policy files
- `policies/c7n/` — c7n YAML policy files

## Key Conventions

### Rule IDs

Rule IDs are derived automatically from the class name — never hardcoded:

```python
class Rule:
    @property
    def rule_id(self) -> str:
        import re
        name = type(self).__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
```

`MaxResourcesPerFile` → `max_resources_per_file`

### Rule Protocol

```python
class SomeRule(Rule):
    def check(self, context: TerraformContext) -> list[Violation]: ...
```

Rules receive a rich context object, not raw HCL dicts.

### Violation Model

```python
@dataclass
class Violation:
    rule: str        # from rule.rule_id
    file: Path
    line: int | None
    message: str
    severity: str = "error"
```

### Config File

```yaml
rules:
  max_resources_per_file:
    max: 8
  required_tags:
    tags: [team, env, cost-center]
  custom:
    path: ./rules/

policies:
  opa:
    enabled: true
    policy_dir: ./policies/opa
  c7n:
    enabled: true
    policy_dir: ./policies/c7n
```

### Policy Engine Integration

OPA and c7n_left are invoked as subprocesses. Their output is normalised to `Violation` objects by adapters. Users write OPA `.rego` files and c7n YAML policies — the library handles invocation and translation.

## Coding Standards

### File Size
- No Python source file may exceed 500 lines. If a module grows beyond this, split it by responsibility (e.g. `parser.py` → `parser/hcl.py` + `parser/builder.py`).

### Design Patterns
- **Dataclass** for all value objects (`Resource`, `Variable`, `Violation`, etc.)
- **Template Method / base class** for `Rule` — subclasses override `check()` only
- **Adapter** for policy engine integrations (OPA, c7n) — same interface, different backends
- **Factory** in `ConfigLoader` for instantiating rules from YAML config
- **Strategy** pattern implicit in the rule list — runner is agnostic to rule internals
- One class per file for rules; shared abstractions in `core/`

### Test Coverage
- Minimum **95% unit test coverage** enforced via `pytest --cov=terrifying --cov-fail-under=95`
- Every task list ends with a coverage gate task
- Tests use `pytest` with `unittest.mock` for subprocess and filesystem isolation
- Fixture `.tf` files live in `tests/fixtures/`

## Capability Map

| Capability | Description |
|---|---|
| `core-model` | HCL parser, context model, Rule base class, Violation |
| `structural-rules` | Built-in file-level rules (resource count, line count, naming) |
| `best-practice-rules` | Built-in content rules (parameterisation, tags, descriptions) |
| `opa-integration` | OPA policy engine adapter |
| `c7n-integration` | c7n_left policy engine adapter |
| `cli-and-config` | CLI entry point and YAML configuration |
