# Design: Core Model

## Context

terrifying is a framework — its value is in how easy it is to write rules against it. The core model must be rich enough that rule authors never touch raw HCL dicts, but simple enough that the abstractions don't obscure what Terraform actually contains.

All other proposals (structural rules, best practice rules, OPA adapter, c7n adapter, CLI) depend on this foundation being stable before they are implemented.

## Goals / Non-Goals

- Goals:
  - Parse `.tf` files into typed Python objects
  - Provide a `Rule` base class with automatic `rule_id` derivation
  - Provide a `Violation` dataclass as the universal result type
  - Provide a `Runner` that executes rules against a context
  - Expose source file and line information on all model objects where python-hcl2 makes it available
- Non-Goals:
  - Parsing `.tfvars`, `.tfstate`, or plan JSON (later)
  - Module resolution or cross-directory analysis (later)
  - Evaluating Terraform expressions (not required for structural/content rules)

## Decisions

### Decision: Use python-hcl2 for parsing

python-hcl2 is the established pure-Python HCL2 parser. It returns a dict representation. The parser layer wraps this into typed objects so rule authors never deal with raw dicts.

Alternatives considered:
- Invoking `terraform show -json`: requires Terraform CLI + init, too heavy for static analysis
- Writing a custom parser: unnecessary given python-hcl2 coverage

### Decision: Rule ID derived from class name

```python
class Rule:
    @property
    def rule_id(self) -> str:
        import re
        name = type(self).__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
```

`MaxResourcesPerFile` → `max_resources_per_file`

This means the config key is always predictable from the class name. No registration step needed.

Alternatives considered:
- Hardcoded string attribute: requires discipline to keep unique and consistent; discarded
- Metaclass registration: unnecessary complexity

### Decision: TerraformContext as the unit of analysis

Rules receive the full `TerraformContext` (all files in the checked directory), not individual files. This allows cross-file rules (e.g. detecting duplicate resource names across files) while simple per-file rules just iterate `context.files`.

### Decision: Violation is a flat dataclass, not a class hierarchy

A single `Violation` dataclass with a `severity` field covers all use cases. Rule authors don't subclass Violation.

## Risks / Trade-offs

- python-hcl2 line number support is limited — `line` may be `None` for many violations initially. Acceptable for v1.
- TerraformContext is scoped to a single directory. Multi-module analysis is explicitly out of scope.

## Open Questions

- None — scope is well-defined for v1.
