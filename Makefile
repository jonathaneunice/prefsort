PYTHON ?= python3
TWINE_USERNAME ?= __token__
export TWINE_USERNAME

.PHONY: help install format lint test build check publish publish-test require-clean-tree

help:
	@echo "install       Install the project and development tools"
	@echo "format        Apply Ruff lint fixes and formatting"
	@echo "lint          Check lint, formatting, and types"
	@echo "test          Run the test suite with coverage"
	@echo "build         Build the wheel and source distribution"
	@echo "check         Run lint and test"
	@echo "publish-test  Release the current version to TestPyPI"
	@echo "publish       Release the current version to PyPI"

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
	check-yaml .github/workflows/*.yml
	check-toml pyproject.toml
	validate-pyproject pyproject.toml
	actionlint -verbose

test:
	$(PYTHON) -m pytest --cov=prefsort --cov-report=term-missing

build:
	rm -rf dist
	$(PYTHON) -m build
	$(PYTHON) -m twine check --strict dist/*

check: lint test

require-clean-tree:
	@test -z "$$(git status --porcelain)" || \
		{ echo "Working tree is not clean; commit, stash, or ignore the changes below."; \
		  git status --short; exit 1; }

publish-test: check require-clean-tree build
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: check require-clean-tree build
	$(PYTHON) -m twine upload dist/*
