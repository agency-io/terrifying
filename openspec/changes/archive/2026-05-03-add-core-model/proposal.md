# Change: Add Core Model — Parser, Context, Rule Protocol, Violation

## Why

Everything else in terrifying depends on a shared foundation: a way to parse Terraform HCL into typed Python objects, a protocol for rules to implement, and a model for reporting violations. Without this, no rules or policy adapters can be written.

## What Changes

- Introduce `TerraformContext` — aggregates all parsed files for a directory
- Introduce `TerraformFile` — one parsed `.tf` file with its resources, variables, outputs, locals, and module calls
- Introduce `Resource`, `Variable`, `Output`, `Local`, `ModuleCall` value objects
- Introduce `Rule` base class — `rule_id` derived from class name (snake_cased), never hardcoded
- Introduce `Violation` dataclass — common result type for all rules and policy adapters
- Introduce `Runner` — discovers rule instances, executes `check()` on context, collects violations
- Introduce `Parser` — wraps python-hcl2 to produce `TerraformFile` objects from `.tf` files

## Impact

- Affected specs: `core-model` (new)
- Affected code: new package `terrifying/core/`
- This is the foundational change — all other proposals depend on it
