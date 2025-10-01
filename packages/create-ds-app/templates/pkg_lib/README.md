# {{ pkg_name }}

A Python library package for reusable functionality.

## Installation

### For development:
```bash
pip install -e .
```

### For production:
```bash
pip install {{ pkg_name }}
```

## Usage

```python
from {{ pkg_name }} import hello_world

message = hello_world("Developer")
print(message)
```

## Building for PyPI

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (test)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Development

This package is part of a monorepo. Make sure you're in the root directory with `pyproject.toml` before generating this template.

{% if add_to_requirements %}
This package has been configured to be added to `{{ requirements_file }}`.
{% endif %}