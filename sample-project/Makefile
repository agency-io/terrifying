.PHONY: install test check-json

install:
	uv sync --all-groups

test: install
	uv run pytest -v

check-json: install
	uv run terrifying check ./terraform --format json
