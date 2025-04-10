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

lint: venv/bin/activate
		. venv/bin/activate
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

build: venv/bin/activate
		. venv/bin/activate
		python -m pip install -U build
		python -m build

lic-check: venv/bin/activate
		. venv/bin/activate
		pip-licenses --from=mixed  --ignore-packages `cat .libraries-whitelist.txt`> licenses.txt --allow-only="$(paste -sd ";" .license-whitelist.txt)"

docs: venv/bin/activate
		. venv/bin/activate
		pip-licenses --from=mixed --format rst --with-urls --with-description --output-file=docs/licenses_table.rst
		sphinx-build -d docs/_build/doctrees docs/ public/

bump-version: venv/bin/activate
		. venv/bin/activate
		bump2version --verbose --commit $(args)

freeze: venv/bin/activate
		. venv/bin/activate
		pip freeze > requirements-freeze.txt

coverage: venv/bin/activate
		. venv/bin/activate
		coverage run -m pytest -v -p no:warnings --junitxml=report.xml tests/
		coverage report
		coverage xml

.PHONY: lint, clean, build, lic-check, docs, bump-version, freeze, coverage