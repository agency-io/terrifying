# Change: Add c7n_left Policy Engine Integration

## Why

Cloud Custodian's `c7n-left` tool performs static analysis of Terraform files against c7n YAML policies — the same policy language used for live cloud resource governance. Integrating it means teams can reuse their existing c7n policies for shift-left validation at the Terraform source level.

## What Changes

- Implement `C7nAdapter` — invokes `c7n-left run` as a subprocess against the Terraform directory, parses its JSON output, and normalises results into `Violation` objects
- c7n policies are YAML files in a configured directory; the adapter passes them to `c7n-left` directly
- Produces a clear error if `c7n-left` is not available

## Impact

- Affected specs: `c7n-integration` (new)
- Affected code: new module `terrifying/policies/c7n.py`
- Depends on: `add-core-model`
- Requires: `c7n-left` binary available on PATH (not bundled; install via `pip install c7n-left`)
