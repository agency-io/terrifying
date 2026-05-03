# Change: Add Built-in Structural Rules

## Why

Structural rules catch file-level problems: files that are too large, contain too many resources, or violate naming conventions. These are the most common architecture guardrails teams want to enforce on Terraform codebases.

## What Changes

- Implement `MaxResourcesPerFile` — fails if a file defines more than N resources
- Implement `MaxLinesPerFile` — fails if a file exceeds N lines
- Implement `ResourceFileNaming` — fails if a file name does not match a configured pattern

All rules extend the `Rule` base class from `core-model`. Rule IDs are derived from class names automatically.

## Impact

- Affected specs: `structural-rules` (new)
- Affected code: new module `terrifying/rules/structural/`
- Depends on: `add-core-model`
