# Project Information

## Development Environment

This project uses **uv** as the package manager and build tool. All dependencies and project configuration are managed through `uv`.

## Project Structure and Guidelines

**IMPORTANT**: All the rules and guidelines described in this file apply to the **entire project** and all packages within it.

Additionally, each package in `packages/` contains its own `CLAUDE.md` file with specific guidelines tailored to that particular package. 

**Before making any changes to a specific package, you MUST:**
1. Read the package-specific `CLAUDE.md` file in `packages/<pkg_name>/CLAUDE.md`
2. Follow the specific guidelines for that package
3. **Simultaneously maintain** all the general principles from this main `CLAUDE.md` file

The package-specific guidelines complement and extend the general project rules - they never override the fundamental security and quality standards outlined here.

## Coding Standards

All coding standards and rules are defined in the `pyproject.toml` file. Please refer to this file for:
- Code formatting rules
- Linting configuration
- Type checking settings
- Import organization
- Documentation standards

## Security - Credentials

**IMPORTANT**: When generating code that includes any credentials, API keys, passwords, or sensitive configuration:

1. **NEVER** commit credentials directly to the code
2. **ALWAYS** add them to the `.env` file
3. Store configuration variables in the main package (core) config
4. Use environment variables in the code to reference these credentials

Example:
```python
# ❌ WRONG - Don't do this
api_key = "sk-1234567890abcdef"

# ✅ CORRECT - Do this instead
import os
api_key = os.getenv("API_KEY")
```

## Code Quality Principles

When writing code, follow these principles:

1. **Type Hints**: Always use type hints for function parameters and return values
2. **Documentation**: Add docstrings to all functions and classes
3. **Error Handling**: Implement proper error handling and logging
4. **Modularity**: Write small, focused functions and classes
5. **Testing**: Write minimal tests for new functionality - focus on essential test cases, not comprehensive test coverage
6. **Consistency**: Follow the existing code style and patterns
7. **Dependencies**: After editing a package, remember to add new requirements to the package's `pyproject.toml` (each package has its own)
8. **Documentation**: After adding functionality, briefly update the package's `README.md` with the most important features. If the functionality is a main feature, also update the project `README.md`

## Code Validation

Before considering any code complete, **ALWAYS** run these validation commands:

```bash
# Fix formatting and linting issues
uv run ruff check . --fix

# Check type annotations
uv run mypy .
```

These commands will:
- Fix code formatting issues automatically
- Check for linting violations and fix what can be auto-fixed
- Validate type annotations and catch type-related errors

**Never skip these validation steps** - they ensure code quality and consistency across the project.
