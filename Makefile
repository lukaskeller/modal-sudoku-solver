.PHONY: init test test-all lint format typecheck clean check

init:
	uv sync

test:
	uv run python -m pytest -m "not slow" -vvv

test-all:
	uv run python -m pytest -vvv

serve:
	modal serve -m src.sudoku

deploy:
	modal deploy -m src.sudoku

lint:
	uvx ruff check .

format:
	uvx ruff format .

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +

check: lint test
