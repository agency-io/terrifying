# Design: OPA Integration

## Context

OPA (Open Policy Agent) evaluates Rego policies against JSON input. terrifying feeds the parsed Terraform context as JSON to OPA and expects violations back in a defined format. The adapter is a thin subprocess wrapper — it does not embed OPA.

## Goals / Non-Goals

- Goals:
  - Invoke `opa eval` with Terraform JSON as input
  - Discover `.rego` files from a configured directory
  - Normalise OPA output into `Violation` objects
  - Produce a clear error if `opa` is not on PATH
- Non-Goals:
  - Bundling the OPA binary
  - Supporting OPA bundles or remote policies (future)
  - Evaluating against Terraform plan JSON (future; current scope is parsed HCL)

## Decisions

### Decision: Input format is TerraformContext serialised as JSON

The adapter serialises `TerraformContext` to a JSON structure mirroring the Python model:

```json
{
  "files": [
    {
      "path": "main.tf",
      "resources": [
        {"type": "aws_s3_bucket", "name": "my_bucket", "attributes": {...}}
      ],
      "variables": [...],
      "outputs": [...]
    }
  ],
  "resources": [...]
}
```

This gives Rego authors a consistent, documented input shape.

### Decision: Violation convention via `deny` set

Rego policies return violations as a `deny` set. Each element is an object:

```rego
deny[msg] {
  resource := input.resources[_]
  resource.type == "aws_s3_bucket"
  not resource.attributes.server_side_encryption_configuration
  msg := sprintf("S3 bucket %s missing encryption", [resource.name])
}
```

Or with file info:

```rego
deny[{"msg": msg, "file": file}] {
  ...
}
```

The adapter maps each element to a `Violation(rule="opa:<policy_filename>", ...)`.

Alternatives considered:
- Custom entrypoint name per policy file: more flexible but harder to document and discover
- Returning structured objects with severity: added complexity with unclear benefit for v1

## Risks / Trade-offs

- Requires `opa` on PATH — fails clearly with an actionable error message if missing
- Serialising TerraformContext to JSON adds a step, but keeps Rego authors decoupled from Python internals

## Open Questions

- None for v1 scope.
