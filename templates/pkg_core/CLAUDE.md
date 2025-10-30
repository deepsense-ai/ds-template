# Core Package Rules

This package provides **centralized configuration management** and **structured logging** used across all project components.

## Configuration Rules

- **ALL** settings must use Pydantic Settings in `config.py`
- **ALL** settings must load from `.env` file via `env_file = ".env"`
- **MUST** provide sensible defaults for all settings
- Use `Literal` types for constrained string values (e.g., environment, log_level)
- Settings class must be named `Settings` and instance `settings`

## Adding New Settings Rules

- Add field to `Settings` class in `config.py` with type hint and default
- Add corresponding environment variable to `.env` file documentation
- Use appropriate Pydantic field types (str, int, bool, Path, Literal, etc.)

## Logging Rules

- **ALL** logging must use Structlog via `get_logger(__name__)`
- **NEVER** use Python's standard `logging` module directly
- **ALWAYS** use structured logging with context: `logger.info("message", key=value)`
- **MUST** use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **NEVER** log sensitive information (passwords, API keys, tokens)
- Use `exc_info=True` when logging exceptions

## Logger Usage Rules

- Import: `from packages.core.logging import get_logger`
- Create logger: `logger = get_logger(__name__)`
- Can bind context at creation: `logger = get_logger(__name__, user_id=123)`
- Include relevant data in log messages as key-value pairs

## File Structure Rules

- `config.py` - Pydantic settings configuration
- `logging.py` - Structlog setup and logger factory
- `__init__.py` - Exports `settings` and `get_logger`

## Import Rules

- Other packages import: `from packages.core.config import settings`
- Other packages import: `from packages.core.logging import get_logger`
