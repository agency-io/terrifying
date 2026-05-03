# Change: Add Built-in Best Practice Rules

## Why

Beyond structure, teams need to verify content quality: that resources are parameterised rather than hardcoded, that variables and outputs are documented, and that required tags are always present. These rules encode common Terraform best practices that apply to most organisations.

## What Changes

- Implement `NoHardcodedValues` — flags resource attribute values that appear to be literals rather than references to variables, locals, or data sources
- Implement `VariablesHaveDescriptions` — flags any variable block missing a `description`
- Implement `OutputsHaveDescriptions` — flags any output block missing a `description`
- Implement `RequiredTags` — flags any resource missing one or more configured required tags

All rules extend the `Rule` base class from `core-model`.

## Impact

- Affected specs: `best-practice-rules` (new)
- Affected code: new module `terrifying/rules/best_practices/`
- Depends on: `add-core-model`
