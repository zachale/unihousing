# Install dependencies with uv
install:
	uv sync --dev

# Lock dependencies with uv
lock:
	uv lock

# Check code without making changes
check:
	uv run ruff check .
	uv run ty check .

# Fix all auto-fixable issues
lint:
	uv run ruff check --fix .
	uv run ruff format .
