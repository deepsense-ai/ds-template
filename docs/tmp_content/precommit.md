# Code Quality and Linting

The ds-template provides comprehensive code quality tools using **Ruff** as the primary linter and formatter, along with **mypy** for type checking and **pytest** for testing.

## What's Included

### Ruff - Fast Python Linter & Formatter
- **Code formatting** with Black-compatible output
- **Import sorting** and organization
- **Comprehensive linting** covering style, logic, and security
- **10-100x faster** than traditional Python linters
- **Built-in security scanning** with bandit-compatible rules

### mypy - Type Checking
- **Static type checking** for better code reliability
- **Type annotation** requirements and validation
- **Integration** with Ruff for comprehensive code quality

### pytest - Testing Framework
- **Modern testing** with async support and fixtures
- **Coverage reporting** for test completeness
- **Doctest integration** for documentation testing

## Configuration

All tools are pre-configured in `pyproject.toml` with sensible defaults for data science projects:

- **Line length**: 120 characters
- **Docstring style**: Google convention
- **Import organization**: Data science packages properly categorized
- **Per-file rules**: Different rules for notebooks and tests
- **Ignored rules**: Practical exceptions for data science workflows

## Usage

### Basic Commands

```bash
# Check code quality
uv run ruff check .

# Format code
uv run ruff format .

# Fix issues automatically
uv run ruff check . --fix

# Run type checking
uv run mypy .

# Run tests
uv run pytest
```

### Pre-commit Hooks

The generated projects include pre-commit configuration that automatically runs:
- **Ruff linting** and formatting
- **mypy type checking**
- **Security scanning**

To set up pre-commit hooks:
```bash
uv run pre-commit install
```

## CI/CD Integration

All tools are integrated into CI/CD pipelines:
- **GitHub Actions** workflows include all quality checks
- **GitLab CI** pipelines run comprehensive testing
- **Automated formatting** checks ensure consistency
- **Security scanning** prevents vulnerabilities

## Customization

The configuration can be customized by editing `pyproject.toml`:
- **Add or remove rules** as needed
- **Adjust line length** and formatting preferences
- **Configure per-file exceptions** for specific patterns
- **Add custom third-party packages** to import sorting

For detailed configuration options, see the `[tool.ruff]`, `[tool.mypy]`, and `[tool.pytest]` sections in your project's `pyproject.toml` file.