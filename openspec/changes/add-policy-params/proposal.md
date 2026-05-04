# Change: Add Policy Parameters

## Why

Policy engines (OPA, c7n) need to accept parameters from `terrifying.yml` so that
values like required tags, allowed regions, or retention thresholds are defined once
and flow into all policies that reference them. Without this, policy authors hardcode
values or maintain separate config files, creating drift between policy intent and
project configuration.

## What Changes

### terrifying.yml schema
Both `opa` and `c7n` sections gain a two-level parameter model:
- `params` — global defaults applied to every policy in that section
- `policies.<name>.params` — per-policy overrides merged on top of globals

```yaml
policies:
  opa:
    path: ./policies/opa
    params:
      required_tags: [Environment, Team]   # global
    policies:
      require_encryption:
        params:
          algorithm: AES256                # policy-specific, merged over global

  c7n:
    path: ./policies/c7n
    params:
      required_tags: [Environment, Team]
    policies:
      require-retention:
        params:
          min_retention_days: 90
```

Merge rule: `{**global_params, **policy_params}` — policy-level wins on conflict.

### OPA adapter
Merged params are injected into the OPA input document alongside the Terraform
context, accessible in Rego as `input.params`:

```rego
deny contains msg if {
    tag := input.params.required_tags[_]
    resource := input.resources[_]
    not resource.attributes.tags[tag]
    msg := sprintf("Resource %v.%v missing tag '%v'", [resource.type, resource.name, tag])
}
```

### c7n adapter
c7n YAML policy files are treated as Jinja2 templates. Before passing to `c7n-left`,
terrifying renders each file with the merged params:

```yaml
# require_tags.yml.j2  (or .yml — extension is flexible)
policies:
  {% for tag in required_tags %}
  - name: require-{{ tag | lower }}-tag
    resource: terraform.aws_s3_bucket
    filters:
      - "tag:{{ tag }}": absent
  {% endfor %}
```

The rendered YAML is written to a temporary file and passed to `c7n-left`. The
original template file is never modified.

### Dependencies
- Add `jinja2>=3` to `[project]` dependencies in `pyproject.toml`

## Impact

- Affected specs: `policy-params` (new), `opa-integration` (modified), `c7n-integration` (modified)
- Affected code: `terrifying/core/config.py`, `terrifying/policies/opa.py`, `terrifying/policies/c7n.py`
- Depends on: `add-core-model`, `add-opa-integration`, `add-c7n-integration`, `add-cli-and-config`
