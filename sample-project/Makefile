.PHONY: install check check-json check-rules

install:
	uv sync

# Run all checks (rules + custom rules + OPA + c7n) with text output
check: install
	uv run terrifying check ./terraform

# Same checks with JSON output
check-json: install
	uv run terrifying check ./terraform --format json

# Run only the built-in and custom Python rules (no policy engines)
check-rules: install
	uv run python -c "\
from pathlib import Path; \
from terrifying.core import Parser, Runner; \
from terrifying.core.config import ConfigLoader; \
loader = ConfigLoader(); \
config = loader.load(Path('.')); \
rules = loader.build_rules(config); \
ctx = Parser().parse_directory(Path('./terraform')); \
violations = Runner().run(rules, ctx); \
[print(f'{v.file} [{v.rule}] {v.severity}: {v.message}') for v in violations]; \
exit(1 if any(v.severity == 'error' for v in violations) else 0)"
