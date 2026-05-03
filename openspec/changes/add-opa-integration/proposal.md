# Change: Add OPA Policy Engine Integration

## Why

Some policy concerns — encryption at rest, IAM constraints, network exposure — are better expressed as Rego policies than Python rule classes. Integrating OPA lets teams reuse existing policy libraries and express complex cross-resource policies in a language designed for it.

## What Changes

- Implement `OpaAdapter` — invokes `opa eval` as a subprocess, feeds parsed Terraform as JSON input, and normalises the output into `Violation` objects
- OPA policies are `.rego` files in a configured directory; the adapter discovers and loads them automatically
- Users write standard Rego; the adapter defines a convention for how violations are returned from Rego (a `deny` or `violations` set with `msg` and optional `file`/`line` fields)

## Impact

- Affected specs: `opa-integration` (new)
- Affected code: new module `terrifying/policies/opa.py`
- Depends on: `add-core-model`
- Requires: `opa` binary available on PATH (not bundled)
