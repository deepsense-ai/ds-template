# Library Package Rules

This package provides a **reusable Python library** that can be shared across multiple components or published to PyPI.

## Package Structure Rules

- Main code in `src/<package_name>/` directory
- Public API must be exported via `__init__.py` using `__all__`
- Keep functions focused and single-purpose
- Group related functionality in modules
- Use descriptive module and function names

## Export Rules

- **ALWAYS** update `__init__.py` when adding new public functions/classes
- Only export public API functions/classes in `__init__.py`
- Use `__all__` to explicitly define public exports
- Private/internal functions should not be exported

## Dependency Rules

- Keep dependencies minimal for better compatibility
- Use optional dependencies for features that not all users need
- Add new dependencies to the package's `pyproject.toml` (not monorepo root)

## Version Management Rules

- Update version in `pyproject.toml` under `[project]` section before publishing
- Tag releases in git matching the version number after publishing

## Distribution Rules

- Use `MANIFEST.in` to include additional files (README.md, LICENSE, etc.)
- When building for PyPI, use `uv run python -m build`
- For development, packages can be installed in editable mode: `uv pip install -e packages/<lib_package>`
