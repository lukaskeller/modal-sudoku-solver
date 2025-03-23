.PHONY: init test test-all lint clean check

test:
	uv run python -m pytest -m "not slow" -vvv

test-all:
	uv run python -m pytest -vvv

serve:
	uv run modal serve -m src.sudoku

deploy:
	uv run modal deploy -m src.sudoku

lint:
	uvx ruff check . --fix && uvx ruff format .

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	rm -rf .venv

check: lint test
