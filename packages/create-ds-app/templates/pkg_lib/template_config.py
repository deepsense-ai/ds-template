import tomllib
from pathlib import Path
from typing import Any

from ds_templater import TemplateConfig, TextQuestion


def validate_monorepo() -> bool:
    """Check if we're inside a monorepo by looking for pyproject.toml at root."""
    current_dir = Path.cwd()
    pyproject_path = current_dir / "pyproject.toml"

    if not pyproject_path.exists():
        raise ValueError("pyproject.toml not found in current directory. Make sure you're in a monorepo root.")

    return True


def get_pyproject_data() -> dict:
    """Fetch data from pyproject.toml."""
    validate_monorepo()

    pyproject_path = Path.cwd() / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data


class PkgLibTemplateConfig(TemplateConfig):
    """Python package / Library code template configuration"""

    name: str = "Library"
    description: str = "Shared library that may be used between one or more components, packaged as a Python module"
    template_group: str = "package"
    instructions: str = """# Library Package Usage

This package provides a **basic Python library template** that can be extended with reusable functionality for sharing across multiple components.

## Key Features

- **Simple Structure**: Basic library template with core module
- **Type Safety**: Type hints for all functions
- **Documentation**: Comprehensive docstrings
- **Testing Ready**: Pre-configured for pytest
- **PyPI Ready**: Configured for publishing to PyPI

## Current Implementation

### Core Module
```python
# packages/<lib_package>/src/<package_name>/core.py
def hello_world(name: str = "World") -> str:
    \"\"\"Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message.
    \"\"\"
    return f"Hello, {name}! Welcome to {package_name}."
```

### Package Exports
```python
# packages/<lib_package>/src/<package_name>/__init__.py
from .core import hello_world

__all__ = ["hello_world"]
```

## Usage in Other Packages

### Importing Library Functions
```python
# In any other package
from packages.<lib_package> import hello_world

# Use the library
message = hello_world("Developer")
print(message)  # "Hello, Developer! Welcome to my-lib-package."
```

### Installation
```bash
# Install the library package in development mode
uv pip install -e packages/<lib_package>

# Or install from PyPI (when published)
uv pip install <lib_package>
```

## Extending the Library

### Adding New Functions
```python
# Add to core.py or create new modules
def process_data(data: list[dict]) -> list[dict]:
    \"\"\"Process a list of data records.\"\"\"
    # Your processing logic here
    return processed_data

def validate_input(value: str) -> bool:
    \"\"\"Validate input value.\"\"\"
    return isinstance(value, str) and len(value) > 0
```

### Adding New Modules
```python
# Create new files like utils.py, validators.py, etc.
# packages/<lib_package>/src/<package_name>/utils.py
def format_output(data: dict) -> str:
    \"\"\"Format data for output.\"\"\"
    return f"Processed: {data.get('id', 'unknown')}"
```

### Update Exports
```python
# Update __init__.py to export new functions
from .core import hello_world, process_data
from .utils import format_output

__all__ = ["hello_world", "process_data", "format_output"]
```

## Development

### Testing
```bash
# Run tests
uv run pytest packages/<lib_package>

# Run with coverage
uv run pytest packages/<lib_package> --cov
```

### Building for PyPI

The package uses **hatchling** as the build backend, which supports multiple build methods:

#### Build Tools Explained
- **`build`**: Modern Python package building tool that works with any build backend
- **`twine`**: Secure package uploader for PyPI (replaces deprecated `setup.py upload`)
- **`hatchling`**: Fast, modern build backend (already configured in pyproject.toml)
- **`hatch`**: Complete project management tool that includes building and publishing

#### Method 1: Using build + twine (Recommended)
```bash
# Install build tools
uv add build twine

# Build the package
uv run python -m build

# Upload to PyPI (test)
uv run twine upload --repository testpypi dist/*

# Upload to PyPI (production)
uv run twine upload dist/*
```

#### Method 2: Using hatchling directly
```bash
# Install hatchling
uv add hatchling

# Build the package
uv run python -m hatchling build

# Upload using twine
uv add twine
uv run twine upload dist/*
```

#### Method 3: Using hatch (if available)
```bash
# Install hatch
uv add hatch

# Build and publish
uv run hatch build
uv run hatch publish
```

## Best Practices

### Code Organization
- Keep functions focused and single-purpose
- Use descriptive names and docstrings
- Add type hints for all parameters and return values
- Group related functionality in modules

### Documentation
- Write clear docstrings for all public functions
- Include usage examples in docstrings
- Keep README.md updated with new features
- Document breaking changes in version notes

### Versioning
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in pyproject.toml
- Tag releases in git
- Maintain backwards compatibility when possible

## File Structure
- `core.py` - Main library functionality
- `__init__.py` - Package exports
- `pyproject.toml` - Package configuration
- `README.md` - Documentation
- `MANIFEST.in` - Additional files to include

## Dependencies
- **No external dependencies** by default
- Add dependencies to `pyproject.toml` as needed
- Keep dependencies minimal for better compatibility
"""

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="my-lib-package"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", ">=3.10")
        # Extract just the version number without the >= prefix
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update({"python_version": self.python_version, "pyproject_data": self.pyproject_data})
        return additional_context

# Create instance of the config to be imported
config = PkgLibTemplateConfig()

