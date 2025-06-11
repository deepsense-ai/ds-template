#!/bin/bash

# Force Sphinx to rebuild documentation - otherwise it generates inconsistencies.
rm -rf public/ docs/_build

# Exit on error for the next commands
set -e -x

# Generate a table with all installed libraries, licenses etc
uv run pip-licenses --from=mixed --format rst --with-urls --with-description --output-file=docs/licenses_table.rst

# Build sphinx docs to public/ directory
uv run sphinx-build -d docs/_build/doctrees docs/ public/
