define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
sources = opendatasets

.PHONY: test format lint unittest coverage pre-commit clean
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test: lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests
	# mypy $(sources) tests

unittest: clean
	pytest

cov:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

pre-commit:
	pre-commit run --all-files

clean-cache:
	rm -rf .mypy_cache .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage
	rm -rf output/*.*

clean: clean-build clean-pyc clean-cache

dist: clean
	poetry build

release: dist ## package and upload a release
	twine upload dist/*
