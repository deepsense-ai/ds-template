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


class PkgCoreTemplateConfig(TemplateConfig):
    """Core package template configuration"""

    name: str = "Core package"
    description: str = "Core logic, configuration and utilities used by every component in the project"
    template_group: str = "package"
    instructions: str = """# Core Package Usage

This package provides **centralized configuration management** and **structured logging** used across all project components.

## Key Features

- **Configuration Management**: Centralized settings with Pydantic
- **Structured Logging**: Consistent logging across all packages using Structlog
- **Environment Support**: Development, staging, and production configurations
- **Type Safety**: Full type hints and validation

## Configuration Management

### Settings Class
```python
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    environment: Literal["development", "staging", "production"] = "development"
    api_key: str | None = None
    database_url: str = "sqlite:///./app.db"
    data_dir: Path = Path("data")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    debug_mode: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### Environment Variables
```bash
# Environment
ENVIRONMENT=development
DEBUG_MODE=false
LOG_LEVEL=INFO

# API Configuration
API_KEY=your-api-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Paths
DATA_DIR=./data
```

## Structured Logging

### Using the Logger
```python
from .logging import get_logger

logger = get_logger(__name__)

def my_function():
    logger.info("Starting data processing")
    try:
        # Your logic here
        logger.info("Processing completed", status="success")
    except Exception as e:
        logger.error("Processing failed", error=str(e), exc_info=True)
```

### Logger Features
- **Structured Output**: JSON in production, colored console in development
- **Context Binding**: Add context to all log messages
- **Call Site Info**: Automatic filename, line number, and function name
- **Environment Aware**: Different output formats for dev/prod

### Advanced Logging
```python
# Bind context to logger
logger = get_logger(__name__, user_id=123, request_id="abc-123")

# Log with additional context
logger.info("User action", action="login", ip="192.168.1.1")

# Log exceptions with stack trace
try:
    risky_operation()
except Exception:
    logger.error("Operation failed", exc_info=True)
```

## Usage Across Packages

### Importing Core Functionality
```python
# In any other package
from packages.core.config import settings
from packages.core.logging import get_logger

# Use settings
if settings.debug_mode:
    print("Debug mode enabled")

# Use logger
logger = get_logger(__name__)
logger.info(f"Using database: {settings.database_url}")
```

### Configuration Access
```python
# Access configuration values
api_key = settings.api_key
data_path = settings.data_dir / "processed"
log_level = settings.log_level

# Check environment
if settings.environment == "production":
    # Production-specific logic
    pass
```

## Development

### Adding New Settings
1. Add field to `Settings` class in `config.py`
2. Add corresponding environment variable
3. Update documentation

### Logging Best Practices
- Use structured logging with context
- Include relevant data in log messages
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Avoid logging sensitive information

### File Structure
- `config.py` - Pydantic settings configuration
- `logging.py` - Structlog setup and logger factory
- `__init__.py` - Exports settings and get_logger

## Dependencies
- **pydantic**: Data validation and settings management
- **pydantic-settings**: Environment variable integration
- **structlog**: Structured logging
- **python-dotenv**: .env file support
"""

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="core"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", "3.13")
        # Extract just the version number without the >= prefix
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update({"python_version": self.python_version, "pyproject_data": self.pyproject_data})
        return additional_context

# Create instance of the config to be imported
config = PkgCoreTemplateConfig()
