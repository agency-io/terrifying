## 1. Setup

- [x] 1.1 Initialise Python package structure: `terrifying/`, `terrifying/core/`, `tests/`, `tests/fixtures/`
- [x] 1.2 Add `python-hcl2` and `pytest`, `pytest-cov` as dependencies

## 2. Value Objects (`terrifying/core/context.py`)

- [x] 2.1 Implement `Resource` dataclass: `type`, `name`, `attributes`, `file`, `line`
- [x] 2.2 Implement `Variable` dataclass: `name`, `description`, `default`, `type`, `file`, `line`
- [x] 2.3 Implement `Output` dataclass: `name`, `description`, `value`, `file`, `line`
- [x] 2.4 Implement `Local` dataclass: `name`, `value`, `file`, `line`
- [x] 2.5 Implement `ModuleCall` dataclass: `name`, `source`, `arguments`, `file`, `line`
- [x] 2.6 Implement `TerraformFile` dataclass with all collections and `line_count`
- [x] 2.7 Implement `TerraformContext` dataclass with `files` list and `resources` property (flat view across all files)
- [x] 2.8 Implement `TerraformContext.to_json() -> dict` for policy adapter use
- [x] 2.9 Verify `context.py` does not exceed 500 lines; split if needed

## 3. Rule and Violation (`terrifying/core/rule.py`)

- [x] 3.1 Implement `Violation` dataclass: `rule`, `file`, `line`, `message`, `severity="error"`
- [x] 3.2 Implement `Rule` base class with `rule_id` property (regex snake_case from `type(self).__name__`)
- [x] 3.3 Verify `rule.py` does not exceed 500 lines

## 4. Parser (`terrifying/core/parser.py`)

- [x] 4.1 Implement `Parser.parse_directory(path: Path) -> TerraformContext`
- [x] 4.2 Iterate `.tf` files only; skip non-`.tf` files silently
- [x] 4.3 On HCL parse error produce `Violation(rule="parse_error", severity="error")` and continue
- [x] 4.4 Populate `line_count` by reading raw file line count
- [x] 4.5 Map HCL dict structures to typed value objects (Resource, Variable, Output, Local, ModuleCall)
- [x] 4.6 Verify `parser.py` does not exceed 500 lines

## 5. Runner (`terrifying/core/runner.py`)

- [x] 5.1 Implement `Runner.run(rules: list[Rule], context: TerraformContext) -> list[Violation]`
- [x] 5.2 Collect and flatten violations from all rules
- [x] 5.3 Verify `runner.py` does not exceed 500 lines

## 6. Tests (`tests/core/`)

- [x] 6.1 Fixture `.tf` files: valid multi-resource file, invalid HCL file, file with variables/outputs/locals/modules
- [x] 6.2 Test `rule_id` derivation: single word, two words, three words, all-caps acronym prefix
- [x] 6.3 Test `Rule` cannot be used without implementing `check()` (raises `NotImplementedError`)
- [x] 6.4 Test `Violation` defaults: `severity` defaults to `"error"`, `line` defaults to `None`
- [x] 6.5 Test `Parser.parse_directory`: valid dir → correct resource/variable/output counts
- [x] 6.6 Test `Parser.parse_directory`: invalid HCL file → parse_error violation, other files still parsed
- [x] 6.7 Test `Parser.parse_directory`: empty directory → empty context
- [x] 6.8 Test `Parser.parse_directory`: directory with no `.tf` files → empty context
- [x] 6.9 Test `TerraformContext.resources`: flat list across multiple files
- [x] 6.10 Test `TerraformContext.to_json()`: all fields present, correct types
- [x] 6.11 Test `TerraformFile.line_count`: matches actual file line count
- [x] 6.12 Test `Runner.run`: two rules each producing one violation → two violations returned
- [x] 6.13 Test `Runner.run`: no violations → empty list
- [x] 6.14 Test `Runner.run`: empty rule list → empty list

## 7. Coverage Gate

- [x] 7.1 Run `pytest --cov=terrifying --cov-fail-under=95` and confirm it passes
