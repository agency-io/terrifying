.PHONY: install lint fmt test ci

install:
	uv sync

fmt:
	uv run black .

lint:
	uv run black --check .
	uv run ruff check .
	uv run pylint terrifying/

test:
	uv run pytest --cov=terrifying --cov-branch --cov-fail-under=95

ci: lint test
