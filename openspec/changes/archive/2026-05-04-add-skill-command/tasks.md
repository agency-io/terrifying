## 1. Implementation

- [x] 1.1 Create `terrifying/skill.py` with the claude-code skill markdown as a module-level string constant
- [x] 1.2 Add `_cmd_skill(args)` in `terrifying/cli.py` that:
  - Prints the skill to stdout when `args.format == "claude-code"`
  - Prints an unsupported-format message with the GitHub issues URL otherwise
- [x] 1.3 Register `skill` subparser in `main()` with `--format` argument (default: `claude-code`), wired to `_cmd_skill`

## 2. Tests

- [x] 2.1 Add `tests/cli/test_cmd_skill.py` covering:
  - claude-code format output contains expected content
  - unsupported format prints "not yet supported" and issues URL
  - CLI integration via subprocess
- [x] 2.2 Confirm coverage ≥ 95%: `uv run pytest --cov=terrifying --cov-fail-under=95`

## 3. Quality

- [x] 3.1 Run `make ci` (black + ruff + pylint + pytest) — all green
