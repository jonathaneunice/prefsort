PYTHON ?= python3

.PHONY: help install format lint test build check

help:
	@echo "install  Install the project and development tools"
	@echo "format   Apply Ruff lint fixes and formatting"
	@echo "lint     Check lint, formatting, and types"
	@echo "test     Run the test suite with coverage"
	@echo "build    Build the wheel and source distribution"
	@echo "check    Run lint and test"

install:
	$(PYTHON) -m pip install --upgrade "pip>=25.1"
	$(PYTHON) -m pip install --group dev -e .

format:
	$(PYTHON) -m ruff check --fix .
	$(PYTHON) -m ruff format .

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m mypy

test:
	$(PYTHON) -m pytest --cov=prefsort --cov-report=term-missing

build:
	$(PYTHON) -m build

check: lint test
