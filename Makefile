.PHONY: help install install-dev test test-cov lint format clean build publish docs

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=penpoint --cov-report=html --cov-report=term-missing

lint:  ## Run linting checks
	flake8 penpoint/ tests/
	mypy penpoint/

format:  ## Format code with black
	black penpoint/ tests/
	isort penpoint/ tests/

format-check:  ## Check code formatting
	black --check penpoint/ tests/
	isort --check-only penpoint/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean  ## Build the package
	python setup.py sdist bdist_wheel

publish: build  ## Build and publish to PyPI (requires twine)
	twine upload dist/*

docs:  ## Build documentation
	cd docs && make html

docs-serve:  ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

check: format-check lint test  ## Run all checks

pre-commit:  ## Install pre-commit hooks
	pre-commit install

pre-commit-run:  ## Run pre-commit on all files
	pre-commit run --all-files
