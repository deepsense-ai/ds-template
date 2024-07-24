.ONESHELL:

PYTHON_VERSION := 3.11
WHEEL_VERSION := 0.43.0

.DEFAULT_GOAL := venv/bin/activate

venv/bin/activate: requirements-dev.txt
		python$(PYTHON_VERSION) -m venv venv
		. venv/bin/activate
		pip install --upgrade pip
		pip install wheel==$(WHEEL_VERSION)
		pip install -r requirements-dev.txt
		pre-commit install

activate: venv/bin/activate
		. venv/bin/activate

lint: activate
		pre-commit run --all-files

clean:
		find . -type f -name "*.pyc" -delete
		find . -type d -name "__pycache__" -delete
		rm -rf venv
		rm -rf .pytest_cache
		rm -rf .coverage
		rm -rf build/
		rm -rf dist/
		rm -rf *.egg-info/

.PHONY: update, lint, clean, activate