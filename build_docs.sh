#!/bin/bash

# Force Sphinx to rebuild documentation - otherwise it generates incosistencies.
rm -rf public/ docs/_build

# Exit on error for the next commands
set -e -x

# Build sphinx docs to public/ directory
sphinx-build -d docs/_build/doctrees docs/ public/
