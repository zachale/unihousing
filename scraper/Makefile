# Makefile for Python linting with uv
.PHONY: lint check install

# Install dependencies with uv
install:
	uv sync --dev

# Lock dependencies with uv
lock:
	uv lock

# Check code without making changes
check:
	ruff check .
	ty check .

# Fix all auto-fixable issues
lint:
	ruff check --fix .
	ruff format .
