## 1. Implementation

- [ ] 1.1 Create `terrifying/rules/best_practices/` package with `__init__.py`
- [ ] 1.2 Implement `NoHardcodedValues(allowed_attributes: list[str] | None = None)` in `no_hardcoded_values.py`
  - A value is a reference if it is a string containing `${var.`, `${local.`, `${data.` or starts with `var.`, `local.`, `data.`
  - Plain strings and numbers not matching reference patterns are flagged
  - Attributes in `allowed_attributes` are skipped unconditionally
- [ ] 1.3 Implement `VariablesHaveDescriptions` in `variables_have_descriptions.py`
- [ ] 1.4 Implement `OutputsHaveDescriptions` in `outputs_have_descriptions.py`
- [ ] 1.5 Implement `RequiredTags(tags: list[str])` in `required_tags.py`
  - Checks the `tags` attribute on each resource; flags resources missing any required key
  - Resources with no `tags` attribute at all are also flagged
- [ ] 1.6 Verify each rule file does not exceed 500 lines

## 2. Tests (`tests/rules/best_practices/`)

- [ ] 2.1 `test_no_hardcoded_values.py`:
  - Attribute referencing `var.*` → no violation
  - Attribute referencing `local.*` → no violation
  - Attribute referencing `data.*` → no violation
  - Attribute with `${var.foo}` interpolation → no violation
  - Attribute with plain string literal → violation naming resource, attribute, value
  - Attribute with numeric literal → violation
  - Attribute in `allowed_attributes` list → no violation regardless of value
  - Multiple resources: mixed → only literal-valued attributes flagged
  - `allowed_attributes=None` default does not crash
  - `rule_id` == `"no_hardcoded_values"`

- [ ] 2.2 `test_variables_have_descriptions.py`:
  - Variable with non-empty description → no violation
  - Variable with no description field → violation naming variable and file
  - Variable with empty string description → violation
  - Multiple variables: mixed → only undescribed ones flagged
  - `rule_id` == `"variables_have_descriptions"`

- [ ] 2.3 `test_outputs_have_descriptions.py`:
  - Output with non-empty description → no violation
  - Output with no description field → violation naming output and file
  - Output with empty string description → violation
  - Multiple outputs: mixed → only undescribed ones flagged
  - `rule_id` == `"outputs_have_descriptions"`

- [ ] 2.4 `test_required_tags.py`:
  - Resource with all required tags present → no violation
  - Resource missing one required tag → violation naming resource and missing key
  - Resource missing multiple required tags → violation lists all missing keys
  - Resource with no `tags` attribute → violation
  - Resource with empty `tags` dict → violation for each required key
  - Multiple resources: mixed → only non-compliant ones flagged
  - `rule_id` == `"required_tags"`

## 3. Coverage Gate

- [ ] 3.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
